import { useState, useEffect } from 'react'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import dayGridPlugin from '@fullcalendar/daygrid'
import frLocale from '@fullcalendar/core/locales/fr'
import { api } from '../services/helper'
import { creneauVersEventRecurrent, creneauPersoVersEvent } from '../utils/creneaux'
import PopupAjouterObjectif from './PopupAjouterObjectif'
import PopupCreerCreneauPerso from './PopupCreerCreneauPerso'
import PopupGererCreneauPerso from './PopupGererCreneauPerso'

function Calendrier() {
  const [events, setEvents] = useState([])
  const [creneauObjectif, setCreneauObjectif] = useState(null)
  const [nouveauCreneau, setNouveauCreneau] = useState(null)
  const [creneauxPerso, setCreneauxPerso] = useState([])
  const [persoAGerer, setPersoAGerer] = useState(null)

const charger = () => {
    Promise.all([
      api.get('/plannings/global').catch(() => []),
      api.get('/eleves/').catch(() => []),
      api.get('/classes/').catch(() => []),
      api.get('/creneaux/perso/').catch(() => []),
    ]).then(([creneaux, eleves, classes, perso]) => {
      setCreneauxPerso(perso)
      const evsCours = creneaux.map((creneau) => {
        const classe = classes.find((c) => c.id === creneau.classe_id)
        const couleur = classe?.couleur || '#D59813'
        return creneauVersEventRecurrent(creneau, eleves, couleur)
      })
      const evsPerso = perso.map((cp) => creneauPersoVersEvent(cp))
      setEvents([...evsCours, ...evsPerso])
    })
  }

  useEffect(() => {
    charger()
  }, [])

  // Au clic sur un créneau : on récupère le créneau, l'élève et LA DATE cliquée
  const onEventClick = (info) => {
    if (info.event.extendedProps.type === 'perso') {
      const creneauPerso = creneauxPerso.find((c) => c.id === info.event.extendedProps.persoId)
      setPersoAGerer(creneauPerso)
      return
    }
    setCreneauObjectif({
      creneauId: info.event.extendedProps.creneauId,
      eleveId: info.event.extendedProps.eleveId,
      date: info.event.start,   // date précise de l'occurrence cliquée
    })
  }

  const ajouterObjectif = (contenu, conseils) => {
    const dateCours = creneauObjectif.date.toISOString().split('T')[0]  // "AAAA-MM-JJ"
    api.post('/objectifs/', {
      eleve_id: creneauObjectif.eleveId,
      creneau_id: creneauObjectif.creneauId,
      contenu,
      conseils,
      date_cours: dateCours,
    })
      .then(() => {
        alert('Objectif envoyé !')
        setCreneauObjectif(null)
      })
      .catch(() => alert("Erreur lors de l'ajout de l'objectif"))
  }

  const onDateClick = (info) => {
    // info.date = date+heure cliquées
    const d = info.date
    const dateStr = d.toISOString().split('T')[0]            // "AAAA-MM-JJ"
    const heureStr = d.toTimeString().slice(0, 5)            // "HH:MM"
    setNouveauCreneau({ date: dateStr, heure: heureStr })
  }

  const creerCreneauPerso = (donnees) => {
    api.post('/creneaux/perso/', donnees)
      .then(() => {
        alert('Rendez-vous ajouté !')
        setNouveauCreneau(null)
        charger()
      })
      .catch(() => alert("Erreur lors de l'ajout du rendez-vous"))
  }

  const modifierPerso = (id, donnees) => {
    api.put(`/creneaux/perso/${id}`, donnees)
      .then(() => { setPersoAGerer(null); charger() })
      .catch(() => alert('Erreur lors de la modification'))
  }

  const supprimerPerso = (id) => {
    if (!window.confirm('Supprimer ce rendez-vous ?')) return
    api.delete(`/creneaux/perso/${id}`)
      .then(() => { setPersoAGerer(null); charger() })
      .catch(() => alert('Erreur lors de la suppression'))
  }

  return (
    <>
      <FullCalendar
        plugins={[timeGridPlugin, dayGridPlugin, interactionPlugin]}
        initialView="timeGridWeek"
        events={events}
        locale={frLocale}
        eventClick={onEventClick}
        dateClick={onDateClick}
        headerToolbar={{
          left: 'prev next',
          center: 'title',
          right: 'timeGridWeek dayGridMonth',
        }}
        slotDuration="00:30:00"
        slotLabelInterval="00:30:00"
        slotMinTime="08:00:00"
        slotMaxTime="22:00:00"
        slotLabelFormat={{ hour: '2-digit', minute: '2-digit', hour12: false }}
      />

      {creneauObjectif && (
        <PopupAjouterObjectif
          ouvert={true}
          onFermer={() => setCreneauObjectif(null)}
          onAjouter={ajouterObjectif}
        />
      )}

      {nouveauCreneau && (
        <PopupCreerCreneauPerso
          ouvert={true}
          onFermer={() => setNouveauCreneau(null)}
          dateInitiale={nouveauCreneau.date}
          heureInitiale={nouveauCreneau.heure}
          onCreer={creerCreneauPerso}
        />
      )}

      {persoAGerer && (
        <PopupGererCreneauPerso
          ouvert={true}
          onFermer={() => setPersoAGerer(null)}
          creneau={persoAGerer}
          onModifier={modifierPerso}
          onSupprimer={supprimerPerso}
        />
      )}
    </>
  )
}

export default Calendrier
