// On déclare une fois ici, pour ne pas le répéter dans chaque page
const BASE_URL = import.meta.env.VITE_API_URL

async function requete(chemin, options = {}) {
    // On prépare les en-têtes en JSON
    const headers = { 'Content-Type': 'application/json', ...options.headers }
    // Si un token existe, on l'ajoute (nécessaire pour les routes protégées)
    const token = localStorage.getItem('token')
    if (token) {
        headers.Authorization = `Bearer ${token}`
    }
    // L'appel HTTP : on fusionne les options (methode, body) avec nos en-têtes
    const reponse = await fetch(`${BASE_URL}${chemin}`, { ...options, headers})
    // On lit la réponse JSON
    const donnees = await reponse.json()
    // Si statut non 2xx, on lève l'erreur
    if (!reponse.ok) {
        throw new Error(donnees.error || 'Erreur serveur')
    }
    return donnees
}

export const api = {
    get: (chemin) => requete(chemin),
    post: (chemin, corps) => requete(chemin, { method: 'POST', body: JSON.stringify(corps) }),
    put: (chemin, corps) => requete(chemin, { method: 'PUT', body: JSON.stringify(corps) }),
    delete: (chemin) => requete(chemin, { method: 'DELETE' }),
}
