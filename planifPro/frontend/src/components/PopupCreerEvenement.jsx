import { useState } from 'react'
import { X } from 'lucide-react'

function PopupCreerEvenement({ ouvert, onFermer, onCreer, classes, eleves }) {
  const [titre, setTitre] = useState('')
  const [date, setDate] = useState('')
  const [heure, setHeure] = useState('12:00')
  const [description, setDescription] = useState('')
  const [mode, setMode] = useState('toutes_classes')
  const [selection, setSelection] = useState([])

  if (!ouvert) return null

  // styles des boutons de mode
  const boutonMode = (valeur, label) => (
    <button
      onClick={() => { setMode(valeur); setSelection([]) }}
      className={`rounded-full px-4 py-2 text-sm border border-tracer-violet transition ${
        mode === valeur ? 'bg-or text-white' : 'bg-bleu-roi text-white'
      }`}
    >
      {label}
    </button>
  )

  // Une fonction pour cocher/décocher 
  const basculer = (id) => {
    setSelection((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    )
  }

  //Adapter valider pour construire destinataires selon le mode
  const valider = () => {
    if (!titre.trim() || !date) {
      alert('Veuillez saisir un titre et une date')
      return
    }
    if ((mode === 'classes' || mode === 'eleves') && selection.length === 0) {
      alert('Veuillez sélectionner au moins un destinataire')
      return
    }
    const destinataires =
      mode === 'toutes_classes'
        ? { type: 'toutes_classes' }
        : { type: mode, ids: selection }

    onCreer({
      titre,
      description,
      date_heure: `${date}T${heure}`,
      destinataires,
    })
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

        <h3 className="text-white text-2xl font-titre mb-4">Créer un événement</h3>

        <label className="block text-white mb-1">Titre de l'événement</label>
        <input
          type="text"
          placeholder="Ex : Audition de piano, Concert de fin d'année..."
          value={titre}
          onChange={(e) => setTitre(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet placeholder:text-white/60 mb-4"
        />

        <div className="flex gap-3 mb-4">
          <div className="flex-1">
            <label className="block text-white mb-1">Date</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet"
            />
          </div>
          <div className="flex-1">
            <label className="block text-white mb-1">Heure</label>
            <input
              type="time"
              value={heure}
              onChange={(e) => setHeure(e.target.value)}
              className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet"
            />
          </div>
        </div>

        <label className="block text-white mb-1">Description</label>
        <textarea
          placeholder="Information complémentaires..."
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet placeholder:text-white/60 mb-4"
        />

        <p className="text-white mb-2">NOTIFIER :</p>
        <div className="flex flex-wrap gap-2 mb-2">
          {boutonMode('toutes_classes', 'Toutes mes classes')}
          {boutonMode('classes', 'Classes spécifiques')}
          {boutonMode('eleves', 'Élèves spécifiques')}
        </div>
        {mode === 'toutes_classes' && (
          <p className="text-white/70 text-sm mb-4">Tous les élèves de toutes vos classes seront notifiés.</p>
        )}

        {mode === 'classes' && (
          <div className="flex flex-col gap-2 mb-4 mt-2">
            {classes.map((classe) => (
              <label key={classe.id} className="flex items-center gap-2 text-white">
                <input
                  type="checkbox"
                  checked={selection.includes(classe.id)}
                  onChange={() => basculer(classe.id)}
                />
                <span
                  className="w-3 h-3 rounded-full inline-block"
                  style={{ backgroundColor: classe.couleur || '#D59813' }}
                />
                {classe.nom}
              </label>
            ))}
          </div>
        )}

        {mode === 'eleves' && (
          <div className="flex flex-col gap-2 mb-4 mt-2">
            {eleves.map((eleve) => (
              <label key={eleve.id} className="flex items-center gap-2 text-white">
                <input
                  type="checkbox"
                  checked={selection.includes(eleve.utilisateur_id)}
                  onChange={() => basculer(eleve.utilisateur_id)}
                />
                <span
                  className="w-3 h-3 rounded-full inline-block"
                  style={{ backgroundColor: eleve.classe_couleur || '#D59813' }}
                />
                {eleve.prenom} {eleve.nom}
              </label>
            ))}
          </div>
        )}

        <div className="flex justify-end gap-3 mt-4">
          <button onClick={onFermer} className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Fermer
          </button>
          <button onClick={valider} className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Envoyer l'invitation
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupCreerEvenement
