import { useState } from 'react'
import { X } from 'lucide-react'

function PopupModifierEvenement({ ouvert, onFermer, evenement, onModifier }) {
  // pré-remplissage depuis l'événement existant
  const [titre, setTitre] = useState(evenement?.titre || '')
  const [date, setDate] = useState(evenement?.date_heure?.split('T')[0] || '')
  const [heure, setHeure] = useState(evenement?.date_heure?.split('T')[1]?.slice(0, 5) || '12:00')
  const [description, setDescription] = useState(evenement?.description || '')

  if (!ouvert) return null

  const valider = () => {
    if (!titre.trim() || !date) {
      alert('Veuillez saisir un titre et une date')
      return
    }
    onModifier(evenement.id, {
      titre,
      description,
      date_heure: `${date}T${heure}`,
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

        <h3 className="text-white text-2xl font-titre mb-4">Modifier l'événement</h3>

        <label className="block text-white mb-1">Titre de l'événement</label>
        <input
          type="text"
          value={titre}
          onChange={(e) => setTitre(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <div className="flex gap-3 mb-4">
          <div className="flex-1">
            <label className="block text-white mb-1">Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet"
            />
          </div>
          <div className="flex-1">
            <label className="block text-white mb-1">Heure</label>
            <input
              type="time"
              value={heure}
              onChange={(e) => setHeure(e.target.value)}
              className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet"
            />
          </div>
        </div>

        <label className="block text-white mb-1">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <div className="flex justify-end gap-3">
          <button onClick={onFermer} className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Annuler
          </button>
          <button onClick={valider} className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Enregistrer
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupModifierEvenement
