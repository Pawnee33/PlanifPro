import { useState } from 'react'
import logo from '../assets/logo.png'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../services/helper'
// Page d'inscription — version statique pour l'instant (pas encore d'interactivité).

function Inscription() {
  const [prenom, setPrenom] = useState('')
  const [nom, setNom] = useState('')
  const [email, setEmail] = useState('')
  const [motDePasse, setMotDePasse] = useState('')
  const [confirmation, setConfirmation] = useState('')
  const [erreur, setErreur] = useState('')
  const [role, setRole] = useState('eleve')
  const navigate = useNavigate()

  const sInscrire = async () => {
    setErreur('')
    //Vérification côté front : les deux mots de passe doivent être identiques
    if (motDePasse !== confirmation) {
      setErreur('Les mots de passe ne correspondent pas')
      return
    }
    try {
      await api.post('/authentification/inscription', {
        role,
        prenom,
        nom,
        email,
        mot_de_passe: motDePasse,
      })
      // Succès : on redirige vers la connexion
      navigate('/connexion')
    } catch (e) {
      setErreur(e.message) // ex: "Adresse e_mail déjà utilisé"
    }
  }
  return (
    // Conteneur plein écran, fond dégradé bleu, contenu centré
    <div className="min-h-screen flex flex-col items-center justify-center gap-8 bg-linear-to-br from-bleu-roi via-bleu-clair to-bleu-roi p-4">

      {/* Logo */}
      <div className="flex items-center gap-3">
        <img src={logo} alt="Logo PlanifPro" className="h-14 w-auto mb-3" />
        <span className="text-black font-logo text-5xl">PlanifPro</span>
      </div>

      {/* Carte d'inscription */}
      <div className="w-full max-w-sm rounded-3xl  bg-linear-to-bl from-bleu-roi from-10% to-bleu-clair-ciel to-90% backdrop-blur-sm p-12 flex flex-col gap-5 shadow-[10px_10px_25px_0px_#0C2863]">

        <h1 className="text-center text-4xl text-white font-titre">Inscription</h1>

        {/* Sélecteur de rôle */}
        <div className="flex gap-3">
          <button type="button"
          onClick={() => setRole('professeur')}
          className={`flex-1 rounded-full py-2 text-white hover:scale-105 shadow-[0px_10px_10px_-06px_#0C2863] ${
            role === 'professeur' ? 'bg-or' : 'bg-bleu-nuit'}`}
          >
            Professeur/Coach
          </button>

          <button
            type="button"
            onClick={() => setRole('eleve')}
            className={`flex-1 rounded-full py-2 text-white hover:scale-105 shadow-[0px_10px_10px_-06px_#0C2863] ${
              role === 'eleve' ? 'bg-or' : 'bg-bleu-nuit'
            }`}
          >
            Élèves/Parent
          </button>
        </div>

        <input
          type="text"
          placeholder="Prénom"
          value={prenom}
          onChange={(e) => setPrenom(e.target.value)}
          className="rounded-[20px] bg-bleu-nuit border border-tracer-violet text-center text-white font-base placeholder-white/70 py-3 px-6 outline-none"
        />

        <input
          type="text"
          placeholder="Nom"
          value={nom}
          onChange={(e) => setNom(e.target.value)}
          className="rounded-[20px] bg-bleu-nuit border border-tracer-violet text-center text-white font-base placeholder-white/70 py-3 px-6 outline-none"
        />

        <input
          type="email"
          placeholder="Adresse e-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="rounded-[20px] bg-bleu-nuit border border-tracer-violet text-center text-white font-base placeholder-white/70 py-3 px-6 outline-none"
        />

        <input
          type="password"
          placeholder="Mot de passe"
          value={motDePasse}
          onChange={(e) => setMotDePasse(e.target.value)}
          className="rounded-[20px] bg-bleu-nuit border border-tracer-violet text-center text-white font-base placeholder-white/70 py-3 px-6 outline-none"
        />

        <input
          type="password"
          placeholder="Confirmer le mot de passe"
          value={confirmation}
          onChange={(e) => setConfirmation(e.target.value)}
          className="rounded-[20px] bg-bleu-nuit border border-tracer-violet text-center text-white font-base placeholder-white/70 py-3 px-6 outline-none"
        />

        {erreur && <p className='text-center text-sm text-red-300'>{erreur}</p>}

        <button
          onClick={sInscrire}
          className="self-center px-10 rounded-full bg-or py-3 text-white font-base text-lg hover:brightness-110 transition backdrop-blur-sm shadow-[00px_10px_10px_-08px_#0C2863]"
        >
          Créer mon compte
        </button>

        {/* Lien connexion */}
        <div className="text-center">
          <span className="inline-block rounded-full bg-bleu-nuit px-5 py-3 mt-3 text-sm text-white font-base ">
            Déjà un compte ? <Link to="/connexion" className="text-or hover:underline">Se connecter</Link>
          </span>
        </div>

      </div>
    </div>
  )
}

export default Inscription
