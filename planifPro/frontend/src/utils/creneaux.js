// Convertit les créneaux du back en events FullCalendar.
// Logique partagée entre PanneauPlanning et Calendrier.

// Table : décalage en jours depuis le lundi
const decalageJour = {
  lundi: 0, mardi: 1, mercredi: 2, jeudi: 3,
  vendredi: 4, samedi: 5, dimanche: 6,
}

// Renvoie l'objet Date du lundi de la semaine en cours
const lundiDeLaSemaine = () => {
  const aujourdhui = new Date()
  const recul = (aujourdhui.getDay() + 6) % 7
  aujourdhui.setDate(aujourdhui.getDate() - recul)
  return aujourdhui
}

// Convertit UN créneau en event FullCalendar.
// `eleves` sert à retrouver le nom, `couleur` la couleur du bloc.
export const creneauVersEvent = (creneau, eleves, couleur) => {
  const eleve = eleves.find((e) => e.id === creneau.eleve_id)
  const titre = eleve ? `${eleve.prenom} ${eleve.nom}` : 'Élève inconnu'

  const date = lundiDeLaSemaine()
  date.setDate(date.getDate() + decalageJour[creneau.jour])
  date.setHours(12, 0, 0, 0)

  const partieDate = date.toISOString().split('T')[0]
  const start = `${partieDate}T${creneau.heure_debut}`
  const end = `${partieDate}T${creneau.heure_fin}`

  return { title: titre, start, end, backgroundColor: couleur, borderColor: couleur }
}

// Correspondance jour -> numéro FullCalendar (dimanche = 0, lundi = 1, ...)
const jourVersNumero = {
  dimanche: 0, lundi: 1, mardi: 2, mercredi: 3,
  jeudi: 4, vendredi: 5, samedi: 6,
}

// Convertit UN créneau en event RÉCURRENT (pour le calendrier global, sur toute la période).
export const creneauVersEventRecurrent = (creneau, eleves, couleur) => {
  const eleve = eleves.find((e) => e.id === creneau.eleve_id)
  const titre = eleve ? `${eleve.prenom} ${eleve.nom}` : 'Élève inconnu'

  return {
    title: titre,
    daysOfWeek: [jourVersNumero[creneau.jour]],   // ex. [1] pour lundi
    startTime: creneau.heure_debut,                // "10:00:00"
    endTime: creneau.heure_fin,                    // "10:45:00"
    startRecur: creneau.date_debut,                // début de la période
    endRecur: creneau.date_fin,                    // fin de la période
    backgroundColor: couleur,
    borderColor: couleur,
  }
}
