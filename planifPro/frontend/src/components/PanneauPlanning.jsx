import { useState, useEffect } from 'react'
import { api } from '../services/helper'
import CalendrierProposition from './CalendrierProposition'

function PanneauPlanning({classe, eleves}) {
    const [plannings, setPlannings] = useState([])
    const [creneauxParPlanning, setCreneauxParPlanning] = useState({})

  // Recharge les planning quand on change de classe
  useEffect(() => {
    api
      .get(`/plannings/classe/${classe.id}`)
      .then(setPlannings)
      .catch(() => setPlannings([]))
  }, [classe.id])

  // affiche les créneaux par planning
  useEffect(() => {
    // si pas de propositions, rien à charger
    if (plannings.length === 0) return
    // une promesse par proposition : aller chercher ses créneaux
    const promesses = plannings.map((planning) =>
      api.get(`/plannings/${planning.id}/creneaux`)
        .then((creneaux) => ({ id: planning.id, creneaux }))
        .catch(() => ({ id: planning.id, creneaux: [] }))
    )
    // Promise.all pour attendre les 3
    Promise.all(promesses).then((resultats) => {
      const parPlanning = {}
      resultats.forEach((resultat) => {
        parPlanning[resultat.id] = resultat.creneaux
      })
      setCreneauxParPlanning(parPlanning)
    })
  }, [plannings])

  // Table : à quel décalage (en jours) correspond chaque jour, à partir du lundi
  const decalageJour = {
    lundi: 0, mardi: 1, mercredi: 2, jeudi: 3,
    vendredi: 4, samedi: 5, dimanche: 6,
  }

  // Renvoie l'objet Date du lundi de la semaine en cours
  const lundiDeLaSemaine = () => {
    const aujourdhui = new Date()
    const recul = (aujourdhui.getDay() + 6) % 7  // nb de jours depuis lundi
    aujourdhui.setDate(aujourdhui.getDate() - recul)
    return aujourdhui
  }

    // Convertit un créneau (back) en event (FullCalendar)
    const creneauVersEvent = (creneau) => {
      const eleve = eleves.find((e) => e.id === creneau.eleve_id)
      const titre = eleve ? `${eleve.prenom} ${eleve.nom}` : 'Élève inconnu'

      // On part du Lundi, on avance jusqu'au bon jour
      const date = lundiDeLaSemaine()
      date.setDate(date.getDate() + decalageJour[creneau.jour])
      date.setHours(12, 0, 0, 0) // midi : évite le décalage de date en UTC

      // On extrait la date au format "AAAA-MM-JJ"
      const partieDate = date.toISOString().split('T')[0]

      const couleur = classe.couleur || '#D59813'
      // On colle l'heure de créneau
      const start = `${partieDate}T${creneau.heure_debut}`
      const end   = `${partieDate}T${creneau.heure_fin}`
      return { title: titre, start, end, backgroundColor: classe.couleur, borderColor: couleur }
    }
  
    return (
      <div>
        {plannings.map((planning) => {
          const events = (creneauxParPlanning[planning.id] || []).map(creneauVersEvent)
          return (
            <div key={planning.id}>
              {/* en-tête : Proposition X */}
              <h3 className="text-white text-xl mb-2">Proposition {planning.numero_proposition}</h3>
              {/* le calendrier de CETTE proposition */}
              <CalendrierProposition events={events} />
            </div>
          )
        })}
      </div>
    )
}

export default PanneauPlanning
