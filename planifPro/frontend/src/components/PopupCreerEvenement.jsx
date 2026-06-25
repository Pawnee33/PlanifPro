import { useState } from 'react'
import { X } from 'lucide-react'

function PopupCreerEvenement({ ouvert, onFermer, onCreer }) {
  const [titre, setTitre] = useState('')
  const [date, setDate] = useState('')
  const [heure, setHeure] = useState('12:00')
  const [description, setDescription] = useState('')
  const [mode, setMode] = useState('toutes_classes')

  if (!ouvert) return null

  const valider = () => {
    if (!titre.trim() || !date) {
      alert('Veuillez saisir un titre et une date')
      return
    }
    // date + heure combinées en ISO 8601 : "2026-09-18T14:00"
    const dateHeure = `${date}T${heure}`
    onCreer({
      titre,
      description,
      date_heure: dateHeure,
      destinataires: { type: mode },
    })
  }

  // styles des boutons de mode
  const boutonMode = (valeur, label) => (
    <button
      onClick={() => setMode(valeur)}
      className={`rounded-full px-4 py-2 text-sm border border-tracer-violet transition ${
        mode === valeur ? 'bg-or text-white' : 'bg-bleu-roi text-white'
      }`}
    >
      {label}
    </button>
  )

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

        <h3 className="text-white text-2xl font-titre mb-4">Créer un événement</h3>

        <label className="block text-white mb-1">Titre de l'événement</label>
        <input
          type="text"
          placeholder="Ex : Audition de piano, Concert de fin d'année..."
          value={titre}
          onChange={(e) => setTitre(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet placeholder:text-white/60 mb-4"
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
          placeholder="Information complémentaires..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet placeholder:text-white/60 mb-4"
        />

        <p className="text-white mb-2">NOTIFIER :</p>
        <div className="flex flex-wrap gap-2 mb-2">
          {boutonMode('toutes_classes', 'Toutes mes classes')}
          {boutonMode('classes', 'Classes spécifiques')}
          {boutonMode('eleves', 'Élèves spécifiques')}
        </div>
        {mode === 'toutes_classes' && (
          <p className="text-white/70 text-sm mb-4">Tous les élèves de toutes vos classes seront notifiés.</p>
        )}

        <div className="flex justify-end gap-3 mt-4">
          <button onClick={onFermer} className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Fermer
          </button>
          <button onClick={valider} className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Envoyer l'invitation
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupCreerEvenement
