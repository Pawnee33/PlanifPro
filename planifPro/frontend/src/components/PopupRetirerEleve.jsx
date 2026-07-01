import { X } from 'lucide-react'

function PopupRetirerEleve({ ouvert, onFermer, eleve, onConfirmer }) {
  if (!ouvert) return null

  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-md"
      >
        {/* Bouton fermer (croix) en haut à droite */}
        <button
          onClick={onFermer}
          className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition"
        >
          <X size={18} />
        </button>

        {/* Message de confirmation */}
        <h2 className="text-or text-lg mb-2">Retirer l'élève</h2>
        <p className="text-white mb-6">
          Voulez-vous vraiment retirer{' '}
          <strong>{eleve.prenom} {eleve.nom}</strong> de la classe ?
          Cette action est irréversible.
        </p>

        {/* Boutons */}
        <div className="flex justify-end gap-3">
          <button
            onClick={onFermer}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Annuler
          </button>
          <button
            onClick={onConfirmer}
            className="rounded-[16px] bg-red-900 px-4 py-2 border border-red-300 text-red-300 hover:scale-105"
          >
            Retirer
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupRetirerEleve
