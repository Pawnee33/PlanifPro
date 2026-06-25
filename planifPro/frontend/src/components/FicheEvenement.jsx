import { api } from '../services/helper'

function FicheEvenement({ evenement, onSupprime }) {
  const formatDateHeure = (iso) => {
    if (!iso) return ''
    const [datePart, heurePart] = iso.split('T')
    const [annee, mois, jour] = datePart.split('-')
    return `${jour}/${mois}/${annee} à ${heurePart?.slice(0, 5)}`
  }

  // libellé lisible du type de destinataires
  const libelleDestinataires = (dest) => {
    if (!dest) return ''
    if (dest.type === 'toutes_classes') return 'Toutes les classes'
    if (dest.type === 'classes') return 'Classes spécifiques'
    if (dest.type === 'eleves') return 'Élèves spécifiques'
    return ''
  }

  const supprimer = () => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cet événement ?')) return
    api.delete(`/evenements/${evenement.id}`)
      .then(() => onSupprime())
      .catch(() => alert('Erreur lors de la suppression'))
  }

  return (
    <div className="flex flex-col gap-4 max-w-4xl mx-auto">
      <div className="bg-bleu-nuit border-3 border-or rounded-2xl p-5">
        <h2 className="text-2xl text-white font-titre mb-2">{evenement.titre}</h2>
        <p className="text-white/80 text-sm mb-1">{formatDateHeure(evenement.date_heure)}</p>
        <p className="text-white/80 text-sm mb-3">Notifié à : {libelleDestinataires(evenement.destinataires)}</p>
        {evenement.description && (
          <div className="bg-bleu-marine border-2 border-tracer-violet rounded-xl px-4 py-3 text-white">
            {evenement.description}
          </div>
        )}
      <button
          onClick={supprimer}
          className="mt-4 rounded-full bg-[#5C1A1A] px-4 py-2 border-2 border-or-tres-clair text-or text-sm hover:scale-105 transition"
        >
          Supprimer
        </button>
      </div>
    </div>
  )
}

export default FicheEvenement
