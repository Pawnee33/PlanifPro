import { useState, useEffect } from 'react'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import frLocale from '@fullcalendar/core/locales/fr'
import { api } from '../services/helper'
import { creneauVersEventRecurrent } from '../utils/creneaux'
import PopupAjouterObjectif from './PopupAjouterObjectif'

function Calendrier() {
  const [events, setEvents] = useState([])
  const [creneauObjectif, setCreneauObjectif] = useState(null)

  useEffect(() => {
    // On charge en parallèle : les créneaux validés ET les élèves (pour les noms)
    Promise.all([
      api.get('/plannings/global').catch(() => []),
      api.get('/eleves/').catch(() => []),
      api.get('/classes/').catch(() => []),
    ]).then(([creneaux, eleves, classes]) => {
      const evs = creneaux.map((creneau) => {
        // on cherche la classe du créneau pour récupérer sa couleur
        const classe = classes.find((c) => c.id === creneau.classe_id)
        const couleur = classe?.couleur || '#D59813'
        return creneauVersEventRecurrent(creneau, eleves, couleur)
      })
      setEvents(evs)
    })
  }, [])

  // Au clic sur un créneau : on récupère le créneau, l'élève et LA DATE cliquée
  const onEventClick = (info) => {
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

  return (
    <>
      <FullCalendar
        plugins={[timeGridPlugin, dayGridPlugin]}
        initialView="timeGridWeek"
        events={events}
        locale={frLocale}
        eventClick={onEventClick}
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
    </>
  )
}

export default Calendrier
