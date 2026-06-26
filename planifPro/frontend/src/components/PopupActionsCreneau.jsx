import { X } from 'lucide-react'

function PopupActionsCreneau({ ouvert, onFermer, creneau, onObjectif, onModifier, onSupprimer }) {
  if (!ouvert) return null

  // date lisible de l'occurrence cliquée
  const dateLisible = creneau?.date
    ? new Date(creneau.date).toLocaleDateString('fr-FR', { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' })
    : ''

  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-sm"
      >
        <button
          onClick={onFermer}
          className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition"
        >
          <X size={18} />
        </button>

        <h3 className="text-white text-xl font-titre mb-1">{creneau?.titre}</h3>
        <p className="text-white/70 text-sm mb-4 capitalize">{dateLisible}</p>

        <div className="flex flex-col gap-2">
          <button
            onClick={onObjectif}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105 transition"
          >
            Donner un objectif
          </button>
          <button
            onClick={onModifier}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105 transition"
          >
            Modifier le cours
          </button>
          <button
            onClick={onSupprimer}
            className="rounded-[16px] bg-[#5C1A1A] px-4 py-2 border-2 border-or-tres-clair text-or hover:scale-105 transition"
          >
            Supprimer le cours
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupActionsCreneau
