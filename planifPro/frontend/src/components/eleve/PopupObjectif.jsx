import FicheObjectif from './FicheObjectif'

function PopupObjectif({ objectif, professeurs, onFermer }) {
  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(evenement) => evenement.stopPropagation()}
        className="max-w-3xl w-full mx-4"
      >
        {objectif ? (
          <FicheObjectif objectif={objectif} professeurs={professeurs} />
        ) : (
          <div className="bg-bleu-nuit border-2 border-or rounded-2xl p-6 text-white">
            Aucun objectif pour ce cours.
          </div>
        )}
      </div>
    </div>
  )
}

export default PopupObjectif
