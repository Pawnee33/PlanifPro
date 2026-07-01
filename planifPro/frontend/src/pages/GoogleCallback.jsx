import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { jwtDecode } from 'jwt-decode'

function GoogleCallback() {
  const naviguer = useNavigate()

  useEffect(() => {
    // Lit l'access_token Google dans l'URL (?access_token=...)
    const parametres = new URLSearchParams(window.location.search)
    const token = parametres.get('access_token')

    if (token) {
      localStorage.setItem('google_token', token)
    }

    // Redirige vers le bon dashboard selon le rôle
    const tokenApp = localStorage.getItem('token')
    if (tokenApp) {
      const { role } = jwtDecode(tokenApp)
      if (role === 'professeur') {
        naviguer('/dashboard-prof')
      } else {
        naviguer('/dashboard-eleve')
      }
    } else {
      naviguer('/connexion')
    }
  }, [])

  return (
    <div className="flex items-center justify-center min-h-screen bg-bleu-nuit">
      <p className="text-white text-lg">Connexion à Google Calendar…</p>
    </div>
  )
}

export default GoogleCallback
