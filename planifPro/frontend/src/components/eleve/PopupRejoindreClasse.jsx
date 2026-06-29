import { useState } from 'react'
import { X } from 'lucide-react'
import { api } from '../../services/helper'


function PopupRejoindreClasse({ ouvert, onFermer, onRejoint }) {
  const [code, setCode] = useState('')

  const rejoindreClasse = async () => {
    try {
      await api.post('/classes/rejoindre', { code_unique: code })
      onRejoint() // demande au dashboard de recharger la liste
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

        {/* Code */}
        <label className="block text-white mb-1">Code de la classe</label>
        <input
          type="text"
          placeholder="Ex : ESD235BH"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className={`${styleChamp} placeholder:text-white/60 mb-4`}
        />

        {/* Boutons */}
        <div className="flex justify-end gap-3 mt-4">
          <button
            onClick={onFermer}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Annuler
          </button>
          <button
            onClick={rejoindreClasse}
            className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Rejoindre la classe
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupRejoindreClasse
