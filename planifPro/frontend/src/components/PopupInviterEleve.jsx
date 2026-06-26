import { useState } from 'react'
import { X } from 'lucide-react'

function PopupInviterEleve({ ouvert, onFermer, onInviter }) {
  const [email, setEmail] = useState('')

  if (!ouvert) return null

  const valider = () => {
    if (!email || !email.includes('@')) {
      alert('Veuillez saisir un email valide')
      return
    }
    onInviter(email)
    setEmail('')
  }

  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-md"
      >
        <button
          onClick={onFermer}
          className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition"
        >
          <X size={18} />
        </button>

        <h3 className="text-white text-xl mb-4">Inviter un élève</h3>
        <p className="text-white/70 text-sm mb-4">
          L'élève recevra un email avec le code pour rejoindre la classe.
        </p>

        <label className="block text-white mb-1">Email de l'élève</label>
        <input
          type="email"
          placeholder="eleve@exemple.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet placeholder:text-white/60 mb-4"
        />

        <div className="flex justify-end gap-3">
          <button
            onClick={onFermer}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Annuler
          </button>
          <button
            onClick={valider}
            className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Envoyer l'invitation
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupInviterEleve
