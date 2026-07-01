import { api } from './helper'

const BASE_URL = import.meta.env.VITE_API_URL

// Lance le flux d'autorisation Google
export const connecterGoogle = async () => {
  try {
    const reponse = await api.get('/calendrier/auth')
    window.location.href = reponse.auth_url
  } catch (erreur) {
    alert('Erreur lors de la connexion à Google Calendar')
  }
}

// Appel POST avec le token Google en header (le helper ne gère pas les headers custom)
async function postAvecTokenGoogle(chemin, corps) {
  const tokenApp = localStorage.getItem('token')
  const tokenGoogle = localStorage.getItem('google_token')
  const reponse = await fetch(`${BASE_URL}${chemin}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${tokenApp}`,
      'X-Google-Token': tokenGoogle,
    },
    body: JSON.stringify(corps),
  })
  const donnees = await reponse.json()
  if (!reponse.ok) {
    throw new Error(donnees.error || 'Erreur serveur')
  }
  return donnees
}

// Exporte des créneaux vers Google Calendar
export const exporterVersGoogle = async (creneauIds) => {
  if (!localStorage.getItem('google_token')) {
    alert("Veuillez d'abord connecter Google Calendar")
    return
  }
  try {
    await postAvecTokenGoogle('/calendrier/export', { creneau_ids: creneauIds })
    alert('Créneaux exportés vers Google Calendar !')
  } catch (erreur) {
    alert("Erreur lors de l'export : " + erreur.message)
  }
}

// Importe les événements Google Calendar comme créneaux perso
export const importerDepuisGoogle = async (dateDebut, dateFin) => {
  if (!localStorage.getItem('google_token')) {
    alert("Veuillez d'abord connecter Google Calendar")
    return
  }
  try {
    const reponse = await postAvecTokenGoogle('/creneaux/perso/import', {
      date_debut: dateDebut,
      date_fin: dateFin,
    })
    alert(reponse.message)
  } catch (erreur) {
    alert("Erreur lors de l'import : " + erreur.message)
  }
}
