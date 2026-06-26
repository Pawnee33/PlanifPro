import { useState } from 'react'
import { X } from 'lucide-react'

function PopupConfigurerDuree({ ouvert, onFermer, eleve, onConfigurer }) {
  // durée pré-remplie avec la valeur actuelle, ou 60 par défaut
  const [duree, setDuree] = useState(eleve?.duree_minutes || 60)

  if (!ouvert) return null

  const valider = () => {
    onConfigurer(eleve.id, Number(duree))
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

        <h3 className="text-white text-xl mb-4">
          Durée du cours de {eleve.prenom} {eleve.nom}
        </h3>

        <label className="block text-white mb-1">Durée (en minutes)</label>
        <input
          type="number"
          min="1"
          value={duree}
          onChange={(e) => setDuree(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <div className="flex justify-end gap-3">
          <button
            onClick={onFermer}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Annuler
          </button>
          <button
            onClick={valider}
            className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupConfigurerDuree
