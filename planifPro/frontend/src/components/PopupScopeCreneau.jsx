import { useState } from 'react'
import { X } from 'lucide-react'

function PopupScopeCreneau({ ouvert, onFermer, dateInitiale, titre, onValider }) {
  const [scope, setScope] = useState('ce_jour')
  const [debut, setDebut] = useState(dateInitiale || '')
  const [fin, setFin] = useState(dateInitiale || '')

  if (!ouvert) return null

  const valider = () => {
    if (scope === 'plusieurs_jours' && (!debut || !fin)) {
      alert('Veuillez choisir les dates de début et de fin')
      return
    }
    if (scope === 'ce_jour') {
      onValider({ scope: 'ce_jour', debut_jour: dateInitiale, fin_jour: dateInitiale })
    } else if (scope === 'plusieurs_jours') {
      onValider({ scope: 'plusieurs_jours', debut_jour: debut, fin_jour: fin })
    } else {
      onValider({ scope: 'toute_la_periode' })
    }
  }

  return (
    <div onClick={onFermer} className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div onClick={(e) => e.stopPropagation()} className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-md">
        <button onClick={onFermer} className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition">
          <X size={18} />
        </button>

        <h3 className="text-white text-xl font-titre mb-4">{titre}</h3>

        <div className="flex flex-col gap-2 mb-4">
          <label className="flex items-center gap-2 text-white">
            <input type="radio" checked={scope === 'ce_jour'} onChange={() => setScope('ce_jour')} />
            Ce jour seulement
          </label>
          <label className="flex items-center gap-2 text-white">
            <input type="radio" checked={scope === 'plusieurs_jours'} onChange={() => setScope('plusieurs_jours')} />
            Plusieurs jours
          </label>
          <label className="flex items-center gap-2 text-white">
            <input type="radio" checked={scope === 'toute_la_periode'} onChange={() => setScope('toute_la_periode')} />
            Toute la période
          </label>
        </div>

        {scope === 'plusieurs_jours' && (
          <div className="flex gap-3 mb-4">
            <div className="flex-1">
              <label className="block text-white mb-1 text-sm">Du</label>
              <input type="date" value={debut} onChange={(e) => setDebut(e.target.value)}
                className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet" />
            </div>
            <div className="flex-1">
              <label className="block text-white mb-1 text-sm">Au</label>
              <input type="date" value={fin} onChange={(e) => setFin(e.target.value)}
                className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet" />
            </div>
          </div>
        )}

        <div className="flex justify-end gap-3">
          <button onClick={onFermer} className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Annuler
          </button>
          <button onClick={valider} className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Confirmer
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupScopeCreneau
