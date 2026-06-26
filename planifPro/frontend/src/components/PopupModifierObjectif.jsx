import { useState } from 'react'
import { X } from 'lucide-react'

function PopupModifierObjectif({ ouvert, onFermer, objectif, onModifier }) {
  const [contenu, setContenu] = useState(objectif?.contenu || '')
  const [conseils, setConseils] = useState(objectif?.conseils || '')

  if (!ouvert) return null

  const valider = () => {
    if (!contenu.trim()) {
      alert("Veuillez saisir un objectif")
      return
    }
    onModifier(objectif.id, contenu, conseils)
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

        <h3 className="text-white text-xl mb-4">Modifier l'objectif</h3>

        <label className="block text-white mb-1">Objectif</label>
        <textarea
          value={contenu}
          onChange={(e) => setContenu(e.target.value)}
          rows={3}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <label className="block text-white mb-1">Conseils (facultatif)</label>
        <textarea
          value={conseils}
          onChange={(e) => setConseils(e.target.value)}
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

export default PopupModifierObjectif
