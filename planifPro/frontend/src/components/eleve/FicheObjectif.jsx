import { Target } from 'lucide-react'

function FicheObjectif({ objectif, professeurs }) {
  // Retrouve le professeur de l'objectif pour afficher son nom
  const professeur = professeurs?.find(
    (prof) => prof.utilisateur_id === objectif.professeur_id
  )
  const nomProfesseur = professeur
    ? `${professeur.prenom} ${professeur.nom}`
    : null

  // Formate la date "AAAA-MM-JJ" en "JJ/MM/AAAA"
  const dateFormatee = objectif.date_cours
    ? objectif.date_cours.split('-').reverse().join('/')
    : null

  return (
    <div className="bg-bleu-nuit border-2 border-or rounded-2xl p-6 max-w-3xl">
      {/* En-tête : logo + titre + nom du prof */}
      <div className="flex items-center gap-3 mb-4">
        <div className="rounded-full bg-or w-12 h-12 flex items-center justify-center shrink-0">
          <Target className="text-white" />
        </div>
        <h2 className="text-or text-2xl flex-1">Objectif</h2>
        {nomProfesseur && (
          <span className="text-or text-xl">{nomProfesseur}</span>
        )}
      </div>

      {/* Carte imbriquée */}
      <div className="bg-bleu-marine border-2 border-tracer-violet rounded-xl p-4">
        {dateFormatee && (
          <p className="text-or text-sm mb-1">Cours du {dateFormatee}</p>
        )}
        <p className="text-white text-lg mb-2">{objectif.contenu}</p>
        {objectif.conseils && (
          <p className="text-white/70 text-sm">Conseils : {objectif.conseils}</p>
        )}
      </div>
    </div>
  )
}

export default FicheObjectif
