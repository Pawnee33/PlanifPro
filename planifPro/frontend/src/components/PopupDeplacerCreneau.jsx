import { useState } from 'react'
import { X } from 'lucide-react'

function PopupDeplacerCreneau({ ouvert, onFermer, creneaux, eleves, classe, onDeplacer }) {
  const [creneauChoisi, setCreneauChoisi] = useState(null)
  const [nouveauJour, setNouveauJour] = useState('')
  const [nouvelleHeure, setNouvelleHeure] = useState('')

  if (!ouvert) return null

  const nomEleve = (eleveId) => {
    const eleve = eleves.find((e) => e.id === eleveId)
    return eleve ? `${eleve.prenom} ${eleve.nom}` : 'Élève inconnu'
  }

  // les jours possibles = ceux de la classe
  const joursClasse = Object.keys(classe.jours_horaires || {})

  // quand on choisit un créneau, on pré-remplit le formulaire avec ses valeurs actuelles
  const choisirCreneau = (creneau) => {
    setCreneauChoisi(creneau)
    setNouveauJour(creneau.jour)
    setNouvelleHeure(creneau.heure_debut.slice(0, 5)) // "16:15:00" -> "16:15"
  }

  const valider = () => {
    onDeplacer(creneauChoisi, nouveauJour, nouvelleHeure)
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

        <h3 className="text-white text-xl mb-4">Déplacer un créneau</h3>

        {creneauChoisi === null ? (
          // ÉTAPE 1 : choisir le créneau
          <div className="flex flex-col gap-2">
            {creneaux.map((creneau) => (
              <button
                key={creneau.id}
                onClick={() => choisirCreneau(creneau)}
                className="text-left bg-bleu-nuit rounded-lg px-3 py-2 border border-tracer-violet text-white text-sm hover:scale-105 transition"
              >
                {nomEleve(creneau.eleve_id)} : {creneau.jour} {creneau.heure_debut.slice(0, 5)}
              </button>
            ))}
          </div>
        ) : (
          // ÉTAPE 2 : nouvelles valeurs
          <div className="flex flex-col gap-4">
            <p className="text-white/80 text-sm">
              Déplacer le cours de {nomEleve(creneauChoisi.eleve_id)}
            </p>

            <div>
              <label className="block text-white mb-1">Nouveau jour</label>
              <select
                value={nouveauJour}
                onChange={(e) => setNouveauJour(e.target.value)}
                className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet"
              >
                {joursClasse.map((jour) => (
                  <option key={jour} value={jour}>{jour}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-white mb-1">Nouvelle heure de début</label>
              <input
                type="time"
                value={nouvelleHeure}
                onChange={(e) => setNouvelleHeure(e.target.value)}
                className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet"
              />
            </div>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => setCreneauChoisi(null)}
                className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105"
              >
                Retour
              </button>
              <button
                onClick={valider}
                className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105"
              >
                Déplacer
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default PopupDeplacerCreneau
