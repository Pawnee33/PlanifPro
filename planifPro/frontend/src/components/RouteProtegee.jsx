import { useState, useEffect } from 'react'
import { Navigate } from 'react-router-dom'
import { api } from '../services/helper'

function RouteProtegee({ children }) {
  // null = vérification en cours, true = connecté, false = pas connecté
  const [estConnecte, setEstConnecte] = useState(null)

  useEffect(() => {
    // On demande au serveur si le cookie envoyé est valide.
    // S'il l'est, l'API répond 200 ; sinon 401/422 → le helper lève une erreur.
    api.get('/authentification/protected')
      .then(() => setEstConnecte(true))
      .catch(() => setEstConnecte(false))
  }, [])

  // Tant qu'on ne sait pas, on affiche un état de chargement (évite un flash de redirection)
  if (estConnecte === null) {
    return <p className="text-white text-center mt-10">Chargement...</p>
  }

  if (!estConnecte) {
    return <Navigate to="/connexion" replace />   // pas connecté → redirige
  }

  return children   // connecté → affiche la page
}

export default RouteProtegee
