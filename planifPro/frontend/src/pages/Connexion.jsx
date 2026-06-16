import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import logo from '../assets/logo.png'
// Page de connexion — version d'interactivité.

function Connexion() {
  const [email, setEmail] = useState('')
  const [motDePasse, setMotDePasse] = useState('')
  const [erreur, setErreur] = useState('')
  const navigate = useNavigate()

  const seConnecter = async () => {
    setErreur('')
    try {
      const reponse = await fetch(`${import.meta.env.VITE_API_URL}/authentification/connexion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, mot_de_passe: motDePasse }),
      })
      const donnees = await reponse.json()

      if (!reponse.ok) {
        setErreur(donnees.error || 'Erreur de connexion')
        return
      }

      localStorage.setItem('token', donnees.access_token) // on stocke le jeton
      navigate('/') // redirection provisoire (on ira vers le dashboard plus tard)
    } catch (e) {
      setErreur('Impossible de joindre le serveur')
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

      {/* Carte de connexion */}
      <div className="w-full max-w-sm rounded-3xl  bg-linear-to-bl from-bleu-roi from-10% to-bleu-clair-ciel to-90% backdrop-blur-sm p-12 flex flex-col gap-5 shadow-[10px_10px_25px_0px_#0C2863]">

        <h1 className="text-center text-4xl text-white font-titre">Connexion</h1>

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

        {/* Ligne options */}
        <div className="flex items-center justify-between text-sm text-white/90 font-base">
          <label className="flex items-center gap-2">
            <input type="checkbox" />
            Se souvenir de moi
          </label>
          <a href="#" className="hover:underline">Mot de passe oublié ?</a>
        </div>

        {erreur && <p className="text-center text-sm text-red-300">{erreur}</p>}

        <button
          onClick={seConnecter}  
          className="rounded-full bg-or py-3 text-white font-base text-lg hover:brightness-110 transition backdrop-blur-sm shadow-[0px_10px_10px_-08px_#0C2863]"
        >
          Se connecter
        </button>

        {/* Lien inscription */}
        <div className="text-center">
          <span className="inline-block rounded-full bg-bleu-nuit px-5 py-3 mt-3 text-sm text-white font-base">
            Pas encore de compte ? <Link to="/inscription" className="text-or hover:underline">S'inscrire</Link>
          </span>
        </div>

      </div>
    </div>
  )
}

export default Connexion
