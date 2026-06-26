import { jwtDecode } from 'jwt-decode'
import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../services/helper'
import logo from '../assets/logo.png'
// Page de connexion — version d'interactivité.

function Connexion() {
    // --- LE STATE : la mémoire du composant ---

  // L'e-mail saisi par l'utilisateur (vide au départ)
  const [email, setEmail] = useState('')

  // Le mot de passe saisi (vide au départ)
  const [motDePasse, setMotDePasse] = useState('')

  // Le message d'erreur à afficher (vide = pas d'erreur)
  const [erreur, setErreur] = useState('')

  // La fonction qui permet de rediriger vers une autre page en JS
  const navigate = useNavigate()

  // --- LA FONCTION DE CONNEXION : la liaison avec le backend ---

  // async : la fonction va attendre une réponse réseau
  const seConnecter = async () => {

    // On efface une éventuelle erreur précédente avant de réessayer
    setErreur('')

    // try : on tente l'appel ; si le réseau plante, on ira dans le "catch"
    try {
      // On envoie les identifiants au backend
      // api.post s'occupe de tout (URL complète, en-tête JSON, token, lecture de la réponse)
      const donnees = await api.post('/authentification/connexion', {
          email,
          mot_de_passe: motDePasse,                       // clé attendue par ton backend
        })

      // Succès : on range le jeton JWT dans le navigateur
      localStorage.setItem('token', donnees.access_token)

      // Redirection vers les dashboards
      const { role } = jwtDecode(donnees.access_token)   // on lit le rôle dans le token

      if (role === 'professeur') {
        navigate('/dashboard-prof')
      } else {
        navigate('/dashboard-eleve')   // (n'existe pas encore — on le créera)
      }

    } catch (e) {
      // Le helper a levé une erreur et e.message contient le texte d'erreur
      setErreur(e.message)
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
          onKeyDown={(e) => { if (e.key === 'Enter') seConnecter() }}
          className="rounded-[20px] bg-bleu-nuit border border-tracer-violet text-center text-white font-base placeholder-white/70 py-3 px-6 outline-none"
        />

        <input
          type="password"
          placeholder="Mot de passe"
          value={motDePasse}
          onChange={(e) => setMotDePasse(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') seConnecter() }}
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
