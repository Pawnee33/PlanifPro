import { useState } from 'react'
import { X } from 'lucide-react'

function PopupEchangerCreneaux({ ouvert, onFermer, creneaux, eleves, onEchanger }) {
  const [premierChoisi, setPremierChoisi] = useState(null)

  if (!ouvert) return null

  const nomEleve = (eleveId) => {
    const eleve = eleves.find((e) => e.id === eleveId)
    return eleve ? `${eleve.prenom} ${eleve.nom}` : 'Élève inconnu'
  }

  const choisir = (creneau) => {
    if (premierChoisi === null) {
      // on choisit le premier
      setPremierChoisi(creneau)
    } else {
      // on choisit le second → on échange
      onEchanger(premierChoisi.id, creneau.id)
    }
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
        <button
          onClick={onFermer}
          className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition"
        >
          <X size={18} />
        </button>

        <h3 className="text-white text-xl mb-2">Échanger deux élèves</h3>
        <p className="text-white/70 text-sm mb-4">
          {premierChoisi === null
            ? 'Choisissez le premier créneau'
            : `Choisissez le créneau à échanger avec ${nomEleve(premierChoisi.eleve_id)}`}
        </p>

        <div className="flex flex-col gap-2">
          {creneaux.map((creneau) => {
            const estLePremier = premierChoisi && premierChoisi.id === creneau.id
            return (
              <button
                key={creneau.id}
                onClick={() => choisir(creneau)}
                disabled={estLePremier}
                className={`text-left rounded-lg px-3 py-2 border text-white text-sm transition ${
                  estLePremier
                    ? 'bg-or border-or'
                    : 'bg-bleu-nuit border-tracer-violet hover:scale-105'
                }`}
              >
                {nomEleve(creneau.eleve_id)} : {creneau.jour} {creneau.heure_debut.slice(0, 5)}
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}

export default PopupEchangerCreneaux
