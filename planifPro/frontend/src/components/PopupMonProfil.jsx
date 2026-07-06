import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { X, Trash2 } from 'lucide-react'
import { api } from '../services/helper'

/**
 * Popup de gestion du profil de l'utilisateur connecté.
 *
 * Permet de :
 *  - consulter et modifier ses informations (prénom, nom, email) ;
 *  - changer son mot de passe ;
 *  - supprimer définitivement son compte.
 *
 * Arguments :
 *     onFermer (fonction) : ferme la popup.
 */
function PopupMonProfil({ onFermer }) {
  const navigate = useNavigate()

  const [prenom, setPrenom] = useState('')
  const [nom, setNom] = useState('')
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('')
  const [motDePasse, setMotDePasse] = useState('')
  const [confirmationMotDePasse, setConfirmationMotDePasse] = useState('')
  const [message, setMessage] = useState(null)
  // message = { type: 'succes' | 'erreur', texte: '...' }

  // Charge les informations du profil à l'ouverture
  useEffect(() => {
    api.get('/utilisateurs/profil')
      .then((utilisateur) => {
        setPrenom(utilisateur.prenom || '')
        setNom(utilisateur.nom || '')
        setEmail(utilisateur.email || '')
        setRole(utilisateur.role || '')
      })
      .catch(() => setMessage({ type: 'erreur', texte: 'Impossible de charger le profil' }))
  }, [])

  // Enregistre les modifications (infos + éventuel nouveau mot de passe)
  const enregistrer = () => {
    setMessage(null)

    if (!prenom.trim() || !nom.trim() || !email.trim()) {
      setMessage({ type: 'erreur', texte: 'Le prénom, le nom et l\'email sont obligatoires' })
      return
    }

    if (motDePasse && motDePasse !== confirmationMotDePasse) {
      setMessage({ type: 'erreur', texte: 'Les deux mots de passe ne correspondent pas' })
      return
    }

    const donnees = { prenom, nom, email }
    // On n'envoie le mot de passe que si l'utilisateur en a saisi un nouveau
    if (motDePasse) {
      donnees.mot_de_passe = motDePasse
    }

    const changementMotDePasse = Boolean(motDePasse)

    api.put('/utilisateurs/profil', donnees)
      .then(() => {
        setMessage({
          type: 'succes',
          texte: changementMotDePasse
            ? 'Profil et mot de passe mis à jour'
            : 'Profil mis à jour',
        })
        setMotDePasse('')
        setConfirmationMotDePasse('')
      })
      .catch((erreur) => setMessage({ type: 'erreur', texte: erreur.message }))
  }

  // Supprime définitivement le compte, puis déconnecte l'utilisateur
  const supprimerCompte = () => {
    const confirmation = window.confirm(
      'Supprimer définitivement votre compte ? Cette action est irréversible.'
    )
    if (!confirmation) return

    api.delete('/utilisateurs/profil')
      .then(() => {
        localStorage.removeItem('token')
        navigate('/connexion')
      })
      .catch((erreur) => setMessage({ type: 'erreur', texte: erreur.message }))
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

        <h3 className="text-white text-2xl font-titre mb-4">Mon profil</h3>

        {/* Message de retour (succès / erreur) */}
        {message && (
          <p
            className={`mb-4 rounded-lg px-3 py-2 text-sm ${
              message.type === 'succes'
                ? 'bg-green-900 text-white'
                : 'bg-red-900 text-white'
            }`}
          >
            {message.texte}
          </p>
        )}

        {/* ---- Informations ---- */}
        <label className="block text-white mb-1">Prénom :</label>
        <input
          type="text"
          value={prenom}
          onChange={(e) => setPrenom(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <label className="block text-white mb-1">Nom :</label>
        <input
          type="text"
          value={nom}
          onChange={(e) => setNom(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        <label className="block text-white mb-1">Email :</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        />

        {role && (
          <p className="text-white/70 text-sm mb-4 capitalize">Rôle : {role}</p>
        )}

        {/* ---- Mot de passe ---- */}
        <hr className="border-tracer-violet/40 my-4" />
        <p className="text-white mb-2">Changer le mot de passe :</p>

        <label className="block text-white mb-1">Nouveau mot de passe :</label>
        <input
          type="password"
          placeholder="Laisser vide pour ne pas changer"
          value={motDePasse}
          onChange={(e) => setMotDePasse(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet placeholder:text-white/60 mb-4"
        />

        <label className="block text-white mb-1">Confirmer le mot de passe :</label>
        <input
          type="password"
          placeholder="Retapez le nouveau mot de passe"
          value={confirmationMotDePasse}
          onChange={(e) => setConfirmationMotDePasse(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet placeholder:text-white/60 mb-4"
        />

        {/* ---- Boutons principaux ---- */}
        <div className="flex justify-end gap-3 mt-2">
          <button
            onClick={onFermer}
            className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Fermer
          </button>
          <button
            onClick={enregistrer}
            className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105"
          >
            Enregistrer
          </button>
        </div>

        {/* ---- Zone dangereuse ---- */}
        <hr className="border-tracer-violet/40 my-6" />
        <p className="text-white/70 text-sm mb-2">Zone dangereuse</p>
        <button
          onClick={supprimerCompte}
          className="flex items-center justify-center gap-2 rounded-[16px] bg-red-900 w-full px-4 py-3 text-white hover:brightness-110 transition"
        >
          <Trash2 size={18} />
          Supprimer mon compte
        </button>
      </div>
    </div>
  )
}

export default PopupMonProfil
