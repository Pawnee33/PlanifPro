import { useState, useEffect } from 'react'
import { api } from '../services/helper'
import CalendrierProposition from './CalendrierProposition'
import PopupSupprimerCreneau from './PopupSupprimerCreneau'
import PopupDeplacerCreneau from './PopupDeplacerCreneau'
import PopupEchangerCreneaux from './PopupEchangerCreneaux'

function PanneauPlanning({ classe, eleves, signal }) {
    const [plannings, setPlannings] = useState([])
    const [creneauxParPlanning, setCreneauxParPlanning] = useState({})
    const [popupSupprimerOuverte, setPopupSupprimerOuverte] = useState(false)
    const [popupDeplacerOuverte, setPopupDeplacerOuverte] = useState(false)
    const [popupEchangerOuverte, setPopupEchangerOuverte] = useState(false)

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

    const deplacerCreneau = (creneau, nouveauJour, nouvelleHeure) => {
        // calcule l'heure de fin = heure de début + durée du créneau
        const [heure, minutes] = nouvelleHeure.split(':').map(Number)   // "10:00" -> [10, 0]
        const totalMinutes = heure * 60 + minutes + creneau.duree_minutes
        const finH = String(Math.floor(totalMinutes / 60)).padStart(2, '0')
        const finM = String(totalMinutes % 60).padStart(2, '0')
        const heureFin = `${finH}:${finM}`

        api.put(`/creneaux/${creneau.id}`, {
          jour: nouveauJour,
          heure_debut: nouvelleHeure,
          heure_fin: heureFin,
        })
          .then(() => api.get(`/plannings/classe/${classe.id}`))
          .then((liste) => setPlannings(trierParNumero(liste)))
          .catch(() => setPlannings([]))
      }

      const echangerCreneaux = (creneauId1, creneauId2) => {
        api.put('/creneaux/echanger', {
          creneau_id_1: creneauId1,
          creneau_id_2: creneauId2,
        })
          .then(() => api.get(`/plannings/classe/${classe.id}`))
          .then((liste) => setPlannings(trierParNumero(liste)))
          .catch(() => setPlannings([]))
      }

    const supprimerCreneau = (creneauId) => {
      api.delete(`/creneaux/${creneauId}`)
        .then(() => {
          return api.get(`/plannings/classe/${classe.id}`)
        })
        .then((liste) => setPlannings(trierParNumero(liste)))
        .catch(() => setPlannings([]))
    }

    const validerPlanning = (planningId) => {
      api.put('/plannings/valider', { planning_id: planningId })
        .then(() => {
          return api.get(`/plannings/classe/${classe.id}`)
        })
        .then((liste) => setPlannings(trierParNumero(liste)))
        .catch(() => setPlannings([]))
    }

    const planningSelectionne = plannings.find(
      (p) => p.statut === 'selectionne' || p.statut === 'modifie'
    )

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
                      className="rounded-full bg-red-600 border-2 border-red-50 px-4 py-2 text-white text-sm hover:scale-105 transition"
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

        {/* Modifications manuelles */}
        {planningSelectionne && (
          <div className="bg-bleu-nuit border-2 border-or rounded-3xl p-6">
            <h3 className="text-white text-lg mb-4">
              Modifications manuelles : Proposition {planningSelectionne.numero_proposition}
            </h3>
            <div className="flex flex-wrap gap-3">

              {/* Bouton déplacer un créneau */}
              <button
                onClick={() => setPopupDeplacerOuverte(true)}
                className="rounded-full bg-or border-2 border-or-tres-clair px-4 py-2 text-white text-sm hover:scale-105 transition"
              >
                Déplacer un créneau
              </button>

              {/* Bouton Échanger deux élèves */}
              <button
                onClick={() => setPopupEchangerOuverte(true)}
                className="rounded-full bg-or border-2 border-or-tres-clair px-4 py-2 text-white text-sm hover:scale-105 transition"
              >
                Échanger deux élèves
              </button>

              {/* Bouton Suppression de créneau */}
              <button 
                onClick={() => setPopupSupprimerOuverte(true)}
                className="rounded-full bg-or border-2 border-or-tres-clair px-4 py-2 text-white text-sm hover:scale-105 transition"
              >
                Supprimer un créneau
              </button>
            </div>
          </div>
        )}

        {/* Valider le planning */}
        {planningSelectionne && (
          <div className="bg-linear-to-br from-green-300/70 to-green-800/50 border-2 border-dashed border-green-400 rounded-3xl p-6 text-center">
            <h3 className="text-green-400 text-2xl font-titre mb-2">Prêt à valider le planning final</h3>
            <p className="text-white/80 mb-4">Le créneau de chaque élève sera envoyé et les élèves seront notifiés</p>
            <button
              onClick={() => validerPlanning(planningSelectionne.id)}
              className="bg-linear-to-br from-green-300/90 to-green-800/70 border-3 border-green-300 rounded-full px-10 py-2 text-white hover:scale-105 transition"
            >
              Valider le planning
            </button>
          </div>
        )}

        {/* Popup Déplacer Créneau */}
        <PopupDeplacerCreneau
          ouvert={popupDeplacerOuverte}
          onFermer={() => setPopupDeplacerOuverte(false)}
          creneaux={planningSelectionne ? (creneauxParPlanning[planningSelectionne.id] || []) : []}
          eleves={eleves}
          classe={classe}
          onDeplacer={(creneau, nouveauJour, nouvelleHeure) => {
            deplacerCreneau(creneau, nouveauJour, nouvelleHeure)
            setPopupDeplacerOuverte(false)
          }}
        />

        {/* Popup Échanger Créneaux */}
        <PopupEchangerCreneaux
          ouvert={popupEchangerOuverte}
          onFermer={() => setPopupEchangerOuverte(false)}
          creneaux={planningSelectionne ? (creneauxParPlanning[planningSelectionne.id] || []) : []}
          eleves={eleves}
          onEchanger={(id1, id2) => {
            echangerCreneaux(id1, id2)
            setPopupEchangerOuverte(false)
          }}
        />

        {/* Popup Supprimer Créneau */}
        <PopupSupprimerCreneau
          ouvert={popupSupprimerOuverte}
          onFermer={() => setPopupSupprimerOuverte(false)}
          creneaux={planningSelectionne ? (creneauxParPlanning[planningSelectionne.id] || []) : []}
          eleves={eleves}
          onSupprimer={(creneauId) => {
            supprimerCreneau(creneauId)
            setPopupSupprimerOuverte(false)
          }}
        />
      </div>
    )
}

export default PanneauPlanning
