import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

function GoogleCallback() {
  const naviguer = useNavigate()

  useEffect(() => {
    // Lit l'access_token dans l'URL (?access_token=...)
    const parametres = new URLSearchParams(window.location.search)
    const token = parametres.get('access_token')

    if (token) {
      // Stocke le token pour l'export/import
      localStorage.setItem('google_token', token)
    }

    // Redirige vers le dashboard
    naviguer('/dashboard-eleve')
  }, [])

  return (
    <div className="flex items-center justify-center min-h-screen bg-bleu-nuit">
      <p className="text-white text-lg">Connexion à Google Calendar…</p>
    </div>
  )
}

export default GoogleCallback
