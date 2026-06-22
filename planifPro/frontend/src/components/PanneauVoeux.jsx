import { useState, useEffect } from 'react'
import { api } from '../services/helper'
import CarteStat from './ui/CarteStat'
import { Bell, SquareCheckBig, TriangleAlert } from 'lucide-react'

function PanneauVoeux({ eleves, classe }) {
  const [voeux, setVoeux] = useState([])

  // Recharge les voeux quand on change de classe
  useEffect(() => {
    api
      .get(`/voeux/statut/${classe.id}`)
      .then(setVoeux)
      .catch(() => setVoeux([]))
  }, [classe.id])

  // --- Helpers d'affichage ---
  const joursAbrege = {
    lundi: 'Lun', mardi: 'Mar', mercredi: 'Mer', jeudi: 'Jeu',
    vendredi: 'Ven', samedi: 'Sam', dimanche: 'Dim',
  }

  const formatCreneaux = (creneaux) => {
    return Object.values(creneaux)
      .map((creneau) => `${joursAbrege[creneau.jour]} ${creneau.heure.replace(':', 'h')}`)
      .join(' - ')
  }

  const voeuDeleve = (eleveID) => voeux.find((v) => v.eleve_id === eleveID)

  const relancer = (eleveID) => {
    api
      .post('/voeux/relancer', { classe_id: classe.id, eleve_ids: [eleveID] })
      .then(() => alert('Relancer envoyée !'))
      .catch(() => alert('Erreur lors de la relance'))
  }

  const relancerTous = () => {
    const enAttente = eleves
      .filter((eleve) => !voeuDeleve(eleve.id))   // garde ceux SANS vœu
      .map((eleve) => eleve.id)                    // ne garde que leurs ids
    api.post('/voeux/relancer', { classe_id: classe.id, eleve_ids: enAttente })
  }

    const generePlanning = async () => {
    try {
      await api.post('/plannings/generer', { classe_id: classe.id })
      alert('Plannings générés !')
    } catch (err) {
      alert(err.message)
    }
  }

  // --- Statistiques ---
  const nombreSoumis = voeux.length

  const nombreAttente = eleves.length - voeux.length

  const tousSoumis = eleves.length > 0 && nombreAttente === 0

  return (
    <div className="flex flex-col gap-4">

      {/* Cartes de statistiques */}
      <div className="flex flex-wrap gap-8">
        <CarteStat titre="Voeux soumis" valeur={nombreSoumis} vert />
        <CarteStat titre="En attente" valeur={nombreAttente} vert />
        <CarteStat titre="Total élèves" valeur={eleves.length} vert />
      </div>

      {tousSoumis ? (
        <div className="flex items-center gap-2">
          <h3 className="text-green-400 text-xl">Tous les voeux ont été soumis</h3>
          <SquareCheckBig size={16} className="text-green-400 mt-1" />
        </div>
      ) : (
        <div className="flex items-center justify-between">
          <h3 className="text-white text-xl">Statut des voeux par élèves</h3>
          <button
            onClick={relancerTous}
            className="flex items-center gap-2 rounded-[12px] px-3 py-2 text-sm bg-bleu-roi border border-tracer-violet text-white hover:scale-105 transition"
          >
            <Bell size={16} className="fill-yellow-400 text-black" /> Relancer les retardataires
          </button>
        </div>
      )}
      {/* Liste des élèves et leurs vœux */}
      <div className="flex flex-col gap-3">
        {/* on boucle sur chaque élève */}
        {eleves.map((eleve) => {
          {/* on cherche le voeu de l'élève */ }
          const voeu = voeuDeleve(eleve.id)
          return (
            //la carte d'un élève côté gauche
            <div
              key={eleve.id}
              className="bg-bleu-nuit rounded-2xl border-2 border-or p-4 flex items-center justify-between gap-4"
            >
              <div className="flex items-center gap-3">
                {/* initiales : 1re lettre du prénom + 1re du nom */}
                <div className="rounded-full bg-or w-10 h-10 flex items-center justify-center text-white font-bold">
                  {eleve.prenom?.[0]}{eleve.nom?.[0]}
                </div>
                {/* bloc texte : nom + ligne vœux empilés */}
                <div>
                  <p className="text-or text-lg">{eleve.prenom} {eleve.nom}</p>
                  {/* SI un vœu existe affiche les créneaux sinon le text */}
                  <p className="text-white/70 text-sm">
                    {voeu ? `Voeux : ${formatCreneaux(voeu.creneaux_souhaites)}` : 'Aucun voeu soumis'}
                  </p>
                </div>
              </div>
              {/* La carte d'un élève côté droit */}
              {voeu ? (
                //badge vert
                <span className="rounded-full px-3 py-1 text-sm bg-green-500/20 text-green-400 border border-green-300">✓ Soumis</span>
              ) : (
                // badge rouge
                <div className="flex items-center gap-2">
                  <span className="rounded-full px-3 py-1 text-sm bg-red-500/20 text-red-400 border border-red-300">En attente</span>
                  <button
                    onClick={() => relancer(eleve.id)}
                    className="flex items-center gap-2 rounded-[12px] px-3 py-3 text-sm bg-bleu-roi border border-tracer-violet text-white hover:scale-105 transition"
                  >
                    <Bell size={16} className="fill-yellow-400 text-black" /> Relancer
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>
      {tousSoumis ? (
        //Encadré doré : génération avec tous les voeux soumis
        <div className="bg-linear-to-br from-green-300/70 to-green-800/50 border-2 border-dashed border-green-400 rounded-3xl p-6 text-center mt-2">
          <p className="text-green-400 text-lg mb-1">Tous les voeux sont collecté !</p>
          <p className="text-white/70 text-sm mb-3">Prêt à générer les 3 propositions de planning</p>
          <button
            onClick={generePlanning}
            className="bg-linear-to-br from-green-300/90 to-green-800/70 border-3 border-green-300 rounded-full py-2 text-white hover:scale-105 transition px-13"
          >
            Générer les plannings
          </button>
        </div>
      ) : (
        <div className="bg-linear-to-br bg-bleu-nuit border-2 border-tracer-violet rounded-3xl p-6 mt-2">
          {/* ligne : bloc gauche (titre + chips) | bouton à droite */}
          <div className="flex items-center justify-between gap-4">

            {/* colonne gauche : titre au-dessus, chips en dessous */}
            <div className="flex flex-col gap-3">
              <h3 className="text-white text-xl">Générer les propositions de planning</h3>
              {/* chips : une pastille par élève */}
              <div className="flex flex-wrap gap-2">
                {eleves.map((eleve) => {
                  const voeu = voeuDeleve(eleve.id)
                  return (
                    <span
                      key={eleve.id}
                      className={`flex items-center gap-1 rounded-full px-3 py-1 text-sm border ${
                        voeu
                          ? 'bg-green-500/20 text-green-400 border-green-300'
                          : 'bg-gray-500/20 text-gray-400 border-gray-400 line-through'
                      }`}
                    >
                      {voeu && <SquareCheckBig size={14} className="text-green-400" />}
                      {eleve.prenom} {eleve.nom?.[0]}.
                    </span>
                  )
                })}
              </div>
                {/* avertissement : liste des élèves sans vœu */}
                <p className="flex items-center gap-2 text-yellow-400 text-sm mt-4">
                  <TriangleAlert size={16} className="fill-yellow-400 text-black shrink-0" />
                  {eleves.filter((eleve) => !voeuDeleve(eleve.id)).length} élève(s) n'ont pas soumis leurs vœux, ils seront exclus si vous générez maintenant.
                </p>
            </div>

            {/* bouton à droite */}
            <button
              onClick={generePlanning}
              className="bg-linear-to-b from-or-clair to-or border-2 border-or-clear rounded-full px-10 py-2 text-white hover:scale-105 transition"
            >
              Générer ({nombreSoumis}/{eleves.length})
            </button>

          </div>
        </div>
      )}
    </div>
  )
}

export default PanneauVoeux
