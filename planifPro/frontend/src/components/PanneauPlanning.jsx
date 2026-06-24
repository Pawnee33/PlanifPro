import { useState, useEffect } from 'react'
import { api } from '../services/helper'
import CalendrierProposition from './CalendrierProposition'

function PanneauPlanning({ classe, eleves, signal }) {
    const [plannings, setPlannings] = useState([])
    const [creneauxParPlanning, setCreneauxParPlanning] = useState({})

  // Recharge les planning quand on change de classe
  useEffect(() => {
    api
      .get(`/plannings/classe/${classe.id}`)
      .then((liste) => setPlannings(trierParNumero(liste)))
      .catch(() => setPlannings([]))
  }, [classe.id, signal])

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

  const trierParNumero = (liste) =>
  [...liste].sort((a, b) => a.numero_proposition - b.numero_proposition)

    // Convertit un créneau (back) en event (FullCalendar)
    const creneauVersEvent = (creneau) => {
      const couleur = classe.couleur || '#D59813'
      const eleve = eleves.find((e) => e.id === creneau.eleve_id)
      const titre = eleve ? `${eleve.prenom} ${eleve.nom}` : 'Élève inconnu'

      // On part du Lundi, on avance jusqu'au bon jour
      const date = lundiDeLaSemaine()
      date.setDate(date.getDate() + decalageJour[creneau.jour])
      date.setHours(12, 0, 0, 0) // midi : évite le décalage de date en UTC

      // On extrait la date au format "AAAA-MM-JJ"
      const partieDate = date.toISOString().split('T')[0]

      // On colle l'heure de créneau
      const start = `${partieDate}T${creneau.heure_debut}`
      const end   = `${partieDate}T${creneau.heure_fin}`
      return { title: titre, start, end, backgroundColor: couleur, borderColor: couleur }
    }

    const supprimerPlanning = (planningId) => {
      api.delete(`/plannings/${planningId}`)
        .then(() => {
          return api.get(`/plannings/classe/${classe.id}`)
        })
        .then((liste) => setPlannings(trierParNumero(liste)))
        .catch(() => setPlannings([]))
    }

    const selectionnePlanning = (planningId) => {
      api.put(`/plannings/${planningId}/selectionner`)
        .then(() => {
          return api.get(`/plannings/classe/${classe.id}`)
        })
        .then((liste) => setPlannings(trierParNumero(liste)))
        .catch(() => setPlannings([]))
    }
  
    return (
      <div className="flex flex-col gap-10 px-10">
        {/* 1. EN-TÊTE DE SECTION — une seule fois, hors du map */}
        <div className="flex items-center justify-between">
          <h2 className="text-white text-3xl font-titre">Proposition générées</h2>
          <p className="text-white/70">Cliquez sur une proposition pour la sélectionner</p>
        </div>
        {plannings.length === 0 ? (
          // 1. Aucune proposition encore généré pour le moment
          <p className="text-white/70 text-center py-8">
            Aucune proposition généré pour l'instant. Générer un planning depuis l'onglet Voeux.
          </p>
        ) : (
          // 2. LES 3 PROPOSITIONS — le map 
          plannings.map((planning) => {
            const events = (creneauxParPlanning[planning.id] || []).map(creneauVersEvent)
            const estSelectionne = planning.statut !== 'genere'
            return (
              <div key={planning.id}
                className={`bg-bleu-roi rounded-3xl border-3 border-or overflow-hidden transition ${estSelectionne ? 'scale-105 ring-4 ring-or shadow-2xl' : ''
                }`}
              >
                {/* en-tête : Proposition X */}
                <div className="p-4 flex items-center gap-3">
                  <div
                    onClick={() => selectionnePlanning(planning.id)}
                    className=" bg-bleu-nuit h-8 w-8 rounded-full border-2 border-or shrink-0 cursor-pointer flex items-center justify-center"
                  >
                    {planning.statut !== 'genere' && (
                      <div className="h-4 w-4 rounded-full bg-or"></div>
                    )}
                  </div>
                  <h3 className="text-white text-xl">Proposition {planning.numero_proposition} :</h3>
                  {planning.statut === 'valide' && (
                    <button
                      onClick={() => supprimerPlanning(planning.id)}
                      className="rounded-full bg-red-600 px-4 py-2 text-white text-sm hover:scale-105 transition"
                    >
                      Supprimer le planning
                    </button>
                  )}
                </div>
                {/* le calendrier de CETTE proposition */}
                <div className="calendrier-proposition">
                  <CalendrierProposition events={events} />
                </div>
              </div>
            )
          })
        )}
      </div>
    )
}

export default PanneauPlanning
