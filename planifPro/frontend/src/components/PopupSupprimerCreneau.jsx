import { X } from 'lucide-react'

function PopupSupprimerCreneau({ ouvert, onFermer, creneaux, eleves, onSupprimer }) {
  if (!ouvert) return null

  // Retrouve le nom d'un élève à partir de son id
  const nomEleve = (eleveId) => {
    const eleve = eleves.find((e) => e.id === eleveId)
    return eleve ? `${eleve.prenom} ${eleve.nom}` : 'Élève inconnu'
  }

  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto"
      >
        {/* Croix de fermeture */}
        <button
          onClick={onFermer}
          className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition"
        >
          <X size={18} />
        </button>

        <h3 className="text-white text-xl mb-4">Supprimer un créneau</h3>

        {/* Liste des créneaux */}
        <div className="flex flex-col gap-2">
          {creneaux.map((creneau) => (
            <div
              key={creneau.id}
              className="flex items-center justify-between bg-bleu-nuit rounded-lg px-3 py-2 border border-tracer-violet"
            >
              <span className="text-white text-sm">
                {nomEleve(creneau.eleve_id)} : {creneau.jour} {creneau.heure_debut.slice(0, 5)}
              </span>
              <button
                onClick={() => onSupprimer(creneau.id)}
                className="rounded-full bg-red-600 border-2 border-red-50 px-3 py-1 text-white text-sm hover:scale-105 transition"
              >
                Supprimer
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default PopupSupprimerCreneau
