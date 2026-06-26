import { useState } from 'react'
import { X } from 'lucide-react'

function PopupGererCreneauPerso({ ouvert, onFermer, creneau, onModifier, onSupprimer }) {
  const [titre, setTitre] = useState(creneau?.titre || '')
  const [description, setDescription] = useState(creneau?.description || '')
  const [date, setDate] = useState(creneau?.date_creneau || '')
  const [heureDebut, setHeureDebut] = useState(creneau?.heure_debut?.slice(0, 5) || '')
  const [heureFin, setHeureFin] = useState(creneau?.heure_fin?.slice(0, 5) || '')

  if (!ouvert) return null

  const valider = () => {
    if (!titre.trim() || !date || !heureDebut || !heureFin) {
      alert('Veuillez remplir le titre, la date et les heures')
      return
    }
    onModifier(creneau.id, {
      titre,
      description,
      date_creneau: date,
      heure_debut: heureDebut,
      heure_fin: heureFin,
    })
  }

  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-md"
      >
        <button
          onClick={onFermer}
          className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition"
        >
          <X size={18} />
        </button>

        <h3 className="text-white text-2xl font-titre mb-4">Modifier le rendez-vous</h3>

        <label className="block text-white mb-1">Titre</label>
        <input
          type="text"
          value={titre}
          onChange={(e) => setTitre(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <label className="block text-white mb-1">Date</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <div className="flex gap-3 mb-4">
          <div className="flex-1">
            <label className="block text-white mb-1">Heure de début</label>
            <input
              type="time"
              value={heureDebut}
              onChange={(e) => setHeureDebut(e.target.value)}
              className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet"
            />
          </div>
          <div className="flex-1">
            <label className="block text-white mb-1">Heure de fin</label>
            <input
              type="time"
              value={heureFin}
              onChange={(e) => setHeureFin(e.target.value)}
              className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet"
            />
          </div>
        </div>

        <label className="block text-white mb-1">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={2}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <div className="flex justify-between gap-3">
          <button
            onClick={() => onSupprimer(creneau.id)}
            className="rounded-full bg-[#5C1A1A] px-4 py-2 border-2 border-or-tres-clair text-or text-sm hover:scale-105 transition"
          >
            Supprimer
          </button>
          <div className="flex gap-3">
            <button onClick={onFermer} className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105">
              Annuler
            </button>
            <button onClick={valider} className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105">
              Enregistrer
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PopupGererCreneauPerso
