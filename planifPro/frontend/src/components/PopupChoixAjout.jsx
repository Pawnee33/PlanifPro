import { X } from 'lucide-react'

function PopupChoixAjout({ ouvert, onFermer, onChoixPerso, onChoixCours }) {
  if (!ouvert) return null

  return (
    <div onClick={onFermer} className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div onClick={(e) => e.stopPropagation()} className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-sm">
        <button onClick={onFermer} className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition">
          <X size={18} />
        </button>

        <h3 className="text-white text-xl font-titre mb-4">Que voulez-vous ajouter ?</h3>

        <div className="flex flex-col gap-2">
          <button
            onClick={onChoixPerso}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105 transition"
          >
            Un rendez-vous personnel
          </button>
          <button
            onClick={onChoixCours}
            className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105 transition"
          >
            Un cours
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupChoixAjout
