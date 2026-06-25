import { useState, useEffect } from 'react'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import frLocale from '@fullcalendar/core/locales/fr'
import { api } from '../services/helper'
import { creneauVersEventRecurrent } from '../utils/creneaux'

function Calendrier() {
  const [events, setEvents] = useState([])

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

  return (
    <FullCalendar
      plugins={[timeGridPlugin, dayGridPlugin]}
      initialView="timeGridWeek"
      events={events}
      locale={frLocale}
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
  )
}

export default Calendrier
