import { useState } from 'react'
import { api } from '../../services/helper'
import { X, Plus, Trash2, ChevronDown } from 'lucide-react'

function FormulaireVoeux({ ouvert, classe, onFermer, onVoeuxSoumis }) {
  // Étape 2 : la liste des vœux (chaque vœu = { jour, heure })
  const [voeux, setVoeux] = useState([{ jour: '', heure: '' }])
  const [erreur, setErreur] = useState('')

  if (!ouvert) return null

  const styleChamp =
    'bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet'

  // Ajoute une ligne de vœu vide
  const ajouterVoeu = () => {
    setVoeux([...voeux, { jour: '', heure: '' }])
  }

  // Supprime une ligne de vœu par son index
  const supprimerVoeu = (index) => {
    setVoeux(voeux.filter((_, position) => position !== index))
  }

  // Met à jour un champ (jour ou heure) d'un vœu donné
  const modifierVoeu = (index, champ, valeur) => {
    const copie = [...voeux]
    copie[index][champ] = valeur
    setVoeux(copie)
  }

  // Construit le dictionnaire attendu par le back et envoie
  const soumettreVoeux = async () => {
    setErreur('')

    // On ne garde que les vœux complètement remplis
    const voeuxRemplis = voeux.filter((voeu) => voeu.jour && voeu.heure)

    // Construit { "1": {jour, heure}, "2": {...} }
    const creneauxSouhaites = {}
    voeuxRemplis.forEach((voeu, index) => {
      creneauxSouhaites[index + 1] = { jour: voeu.jour, heure: voeu.heure }
    })

    try {
      await api.post('/voeux/', {
        classe_id: classe.id,
        creneaux_souhaites: creneauxSouhaites,
      })
      alert('Vos voeux ont bien été envoyés !')
      onVoeuxSoumis() // demande au dashboard de recharger les vœux
      onFermer()
    } catch (err) {
      setErreur(err.message)
    }
  }

  // Les jours disponibles viennent des jours_horaires de la classe
  const joursDisponibles = classe ? Object.keys(classe.jours_horaires) : []

  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(evenement) => evenement.stopPropagation()}
        className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-lg max-h-[90vh] overflow-y-auto"
      >
        {/* Bouton fermer */}
        <button
          onClick={onFermer}
          className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition"
        >
          <X size={18} />
        </button>

        <h2 className="text-or text-lg mb-4">Soumettre mes vœux</h2>

          <>
            {/* Rappel des contraintes du professeur */}
            <p className="text-white/70 text-sm mb-4">
              Choisissez au moins {classe.nombre_voeux_requis} créneaux répartis
              sur au moins {classe.nombre_jours_min} jours différents.
            </p>

            {/* Récap des plages horaires par jour */}
            <div className="bg-bleu-nuit rounded-lg border border-tracer-violet p-3 mb-4">
              <p className="text-or text-sm mb-2">Créneaux possibles :</p>
              <ul className="flex flex-col gap-1">
                {joursDisponibles.map((jour) => (
                  <li key={jour} className="text-white/80 text-sm">
                    {jour} : {classe.jours_horaires[jour].debut} - {classe.jours_horaires[jour].fin}
                  </li>
                ))}
              </ul>
            </div>

            {/* Liste dynamique des vœux */}
            <div className="flex flex-col gap-3 mb-4">
              {voeux.map((voeu, index) => (
                <div key={index} className="flex items-center gap-2">
                  <div className="relative flex-1">
                    <select
                      value={voeu.jour}
                      onChange={(evenement) => modifierVoeu(index, 'jour', evenement.target.value)}
                      className={`${styleChamp} w-full appearance-none pr-9`}
                    >
                      <option value="">Jour</option>
                      {joursDisponibles.map((jour) => (
                        <option key={jour} value={jour}>{jour}</option>
                      ))}
                    </select>
                    <ChevronDown
                      size={18}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-white pointer-events-none"
                    />
                  </div>

                  <input
                    type="time"
                    value={voeu.heure}
                    min={voeu.jour ? classe.jours_horaires[voeu.jour].debut : undefined}
                    max={voeu.jour ? classe.jours_horaires[voeu.jour].fin : undefined}
                    onChange={(evenement) => modifierVoeu(index, 'heure', evenement.target.value)}
                    className={`${styleChamp} flex-1`}
                  />

                  <button
                    onClick={() => supprimerVoeu(index)}
                    className="bg-red-900 rounded-lg p-2 border border-red-300 text-red-100 hover:scale-105"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
            </div>

            {/* Ajouter un vœu */}
            <button
              onClick={ajouterVoeu}
              className="flex items-center gap-2 rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105 mb-4"
            >
              <Plus size={16} /> Ajouter un vœu
            </button>

            {/* Boutons */}
            <div className="flex justify-end gap-3">
              <button
                onClick={onFermer}
                className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105"
              >
                Annuler
              </button>
              <button
                onClick={soumettreVoeux}
                className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105"
              >
                Soumettre
              </button>
            </div>
          </>

        {/* Message d'erreur (back ou validation) */}
        {erreur && <p className="text-red-300 text-sm mt-4">{erreur}</p>}
      </div>
    </div>
  )
}

export default FormulaireVoeux
