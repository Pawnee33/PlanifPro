// On déclare une fois ici, pour ne pas le répéter dans chaque page
const BASE_URL = import.meta.env.VITE_API_URL

async function requete(chemin, options = {}) {
    // On prépare les en-têtes en JSON
    const headers = { 'Content-Type': 'application/json', ...options.headers }
    // Le JWT est dans un cookie HttpOnly : le JavaScript ne peut pas le lire,
    // c'est le navigateur qui l'envoie tout seul (credentials: 'include').
    // On ajoute seulement le jeton CSRF, exigé par le backend pour POST / PUT / DELETE
    const csrf = localStorage.getItem('csrf_token')
    if (csrf) {
        headers['X-CSRF-TOKEN'] = csrf
    }
    // L'appel HTTP : on fusionne les options (methode, body) avec nos en-têtes
    const reponse = await fetch(`${BASE_URL}${chemin}`, { ...options, headers, credentials: 'include' })
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

// Déconnexion : le cookie étant HttpOnly, seul le backend peut l'effacer.
// On nettoie ensuite les infos de session gardées côté navigateur.
export async function deconnecter() {
    try {
        await requete('/authentification/deconnexion', { method: 'POST' })
    } catch (e) {
        // Serveur injoignable : on nettoie quand même le navigateur
    }
    localStorage.removeItem('role')
    localStorage.removeItem('csrf_token')
}
