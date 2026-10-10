import { Navigate } from 'react-router-dom'

function RouteProtegee({ children }) {
  // Le JWT est dans un cookie HttpOnly, invisible pour le JavaScript.
  // On se base donc sur le rôle mémorisé à la connexion : c'est un simple
  // indicateur d'affichage, la vraie vérification reste faite par le backend.
  const role = localStorage.getItem('role')

  if (!role) {
    return <Navigate to="/connexion" replace />   // pas connecté → redirige
  }

  return children   // connecté → affiche la page
}

export default RouteProtegee
