import { useState } from 'react'
import { X } from 'lucide-react'
import { api } from '../services/helper' // adapte l'import à ton helper (comme dans Connexion.jsx)
import SectionHoraires from './ui/SectionHoraires'

function PopupCreerClasse({ ouvert, onFermer, onClasseCree }) {
  const [nom, setNom] = useState('')
  const [couleur, setCouleur] = useState('#D59813')
  const [dateDebut, setDateDebut] = useState('')
  const [dateFin, setDateFin] = useState('')
  const [nombreVoeux, setNombreVoeux] = useState(3)
  const [joursMin, setJoursMin] = useState(2)
  const [jours, setJours] = useState({
    lundi: { actif: false, debut: '09:00', fin: '12:00' },
    mardi: { actif: false, debut: '09:00', fin: '12:00' },
    mercredi: { actif: false, debut: '09:00', fin: '12:00' },
    jeudi: { actif: false, debut: '09:00', fin: '12:00' },
    vendredi: { actif: false, debut: '09:00', fin: '12:00' },
    samedi: { actif: false, debut: '09:00', fin: '12:00' },
    dimanche: { actif: false, debut: '09:00', fin: '12:00' },
  })

  const ordreJours = [
    'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche',
  ]

  // Met à jour UN champ d'UN jour, sans toucher au reste
  const majJour = (jour, champ, valeur) => {
    setJours((prev) => ({
      ...prev,
      [jour]: { ...prev[jour], [champ]: valeur },
    }))
  }

  const creerClasse = async () => {
    // On ne garde que les jours actifs, au format attendu par le backend
    const jours_horaires = {}
    ordreJours.forEach((jour) => {
      if (jours[jour].actif) {
        jours_horaires[jour] = { debut: jours[jour].debut, fin: jours[jour].fin }
      }
    })

    const donnees = {
      nom,
      couleur,
      date_debut: dateDebut,
      date_fin: dateFin,
      jours_horaires,
      nombre_propositions: 3, // pas dans le mockup : valeur par défaut
      nombre_voeux_requis: nombreVoeux,
      nombre_jours_min: joursMin,
    }

    try {
      await api.post('/classes/', donnees)
      onClasseCree() // demande au dashboard de recharger la liste
      onFermer() // ferme la modale
    } catch (err) {
      console.error(err)
    }
  }

  if (!ouvert) return null

  const styleChamp =
    'w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet font-base'

  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto"
      >
        {/* Bouton fermer (croix) en haut à droite */}
        <button
          onClick={onFermer}
          className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition"
        >
          <X size={18} />
        </button>

        {/* Nom */}
        <label className="block text-white mb-1">Nom de la classe</label>
        <input
          type="text"
          placeholder="Ex : Conservatoire, Cours privés ..."
          value={nom}
          onChange={(e) => setNom(e.target.value)}
          className={`${styleChamp} placeholder:text-white/60 mb-4`}
        />

        {/* Couleur */}
        <label className="block text-white mb-1">Choisir la couleur de la classe :</label>
        <label className="block text-white text-[13px] mb-1">Cliquer sur la couleur pour choisir.</label>
        <input
          type="color"
          value={couleur}
          onChange={(e) => setCouleur(e.target.value)}
          className="w-10 h-10 rounded-full border-2 border-tracer-violet bg-bleu-nuit mb-4 hover:scale-105 cursor-pointer"
        />

        <hr className="border-white/30 my-4" />

        {/* Période */}
        <h3 className="text-white/90 uppercase text-sm tracking-wide mb-2">
          Période des cours :
        </h3>
        <label className="block text-white text-[13px] mb-1">Configurez la période de vos cours (ex : année scolaire du 01/09/2026 au 30/06/2027). </label>
        <div className="flex gap-3 mb-4">
          <div className="flex-1">
            <label className="block text-white mb-1">Date de début</label>
            <input
              type="date"
              value={dateDebut}
              onChange={(e) => setDateDebut(e.target.value)}
              className={styleChamp}
            />
          </div>
          <div className="flex-1">
            <label className="block text-white mb-1">Date de fin</label>
            <input
              type="date"
              value={dateFin}
              onChange={(e) => setDateFin(e.target.value)}
              className={styleChamp}
            />
          </div>
        </div>

        <hr className="border-white/30 my-4" />

        {/* Jours et horaires */}
        <h3 className="text-white/90 uppercase text-sm tracking-wide mb-2">
          Jours et horaires des cours :
        </h3>
        <label className="block text-white text-[14px] mb-1">Cliquez sur le bouton pour sélectionner les jours des cours et afficher les paramètres d'horaires :</label>
        {ordreJours.map((jour, index) => (
          <SectionHoraires
            key={jour}
            jour={jour}
            info={jours[jour]}
            index={index}
            onChange={(champ, valeur) => majJour(jour, champ, valeur)}
          />
        ))}

        <hr className="border-white/30 my-4" />

        {/* Contraintes */}
        <h3 className="text-white/90 uppercase text-sm tracking-wide mb-2">
          Contraintes des vœux :
        </h3>
        <label className="block text-white text-[13px] mb-1">Définissez le nombre minimum de vœux que l'élève doit soumettre, ainsi que le nombre minimum de jours différents sur lesquels les répartir (ex : 3 vœux sur au moins 2 jours différents).</label>
        <div className="flex gap-3 mb-4">
          <div className="flex-1">
            <label className="block text-white text-[15px] mb-1">Nombre de vœux minimum</label>
            <input
              type="number"
              min="1"
              value={nombreVoeux}
              onChange={(e) => setNombreVoeux(Number(e.target.value))}
              className={styleChamp}
            />
          </div>
          <div className="flex-1">
            <label className="block text-white text-[15px] mb-1">Jours différents minimum</label>
            <input
              type="number"
              min="1"
              value={joursMin}
              onChange={(e) => setJoursMin(Number(e.target.value))}
              className={styleChamp}
            />
          </div>
        </div>

        {/* Boutons */}
        <div className="flex justify-end gap-3 mt-4">
          <button
            onClick={onFermer}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Annuler
          </button>
          <button
            onClick={creerClasse}
            className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Créer la classe
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupCreerClasse
