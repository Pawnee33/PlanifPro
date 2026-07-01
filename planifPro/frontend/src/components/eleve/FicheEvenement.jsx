import { Calendar } from 'lucide-react'

// Libellés lisibles pour le type de destinataires
const libellesDestinataires = {
  toutes_classes: 'Toutes les classes',
  classes: 'Classes sélectionnées',
  eleves: 'Élèves spécifiques',
  mixte: 'Classes et élèves',
}

function FicheEvenement({ evenement, professeurs }) {
  // Retrouve le professeur de l'événement pour afficher son nom
  const professeur = professeurs?.find(
    (prof) => prof.utilisateur_id === evenement.professeur_id
  )
  const nomProfesseur = professeur
    ? `${professeur.prenom} ${professeur.nom}`
    : null

  // Formate la date_heure ISO "AAAA-MM-JJTHH:MM:SS" en "JJ/MM/AAAA à HH:MM"
  let dateFormatee = null
  if (evenement.date_heure) {
    const [partieDate, partieHeure] = evenement.date_heure.split('T')
    const dateFr = partieDate.split('-').reverse().join('/')
    const heure = partieHeure ? partieHeure.slice(0, 5) : ''
    dateFormatee = `${dateFr} à ${heure}`
  }

  // Libellé du type de destinataires
  const libelleDestinataires = libellesDestinataires[evenement.destinataires?.type]

  return (
    <div className="bg-bleu-nuit border-2 border-or rounded-2xl p-6 max-w-3xl">
      {/* En-tête : logo + titre + nom du prof */}
      <div className="flex items-center gap-3 mb-4">
        <div className="rounded-full bg-or w-12 h-12 flex items-center justify-center shrink-0">
          <Calendar className="text-white" />
        </div>
        <h2 className="text-white text-2xl flex-1">{evenement.titre}</h2>
        {nomProfesseur && (
          <span className="text-or text-xl">{nomProfesseur}</span>
        )}
      </div>

      {/* Date et destinataires */}
      {dateFormatee && (
        <p className="text-white text-sm mb-4">{dateFormatee} :</p>
      )}

      {/* Description dans une carte imbriquée */}
      {evenement.description && (
        <div className="bg-bleu-marine border-2 border-tracer-violet rounded-xl p-4">
          <p className="text-white">{evenement.description}</p>
        </div>
      )}
    </div>
  )
}

export default FicheEvenement
