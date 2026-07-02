import { useState, useEffect } from 'react'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import frLocale from '@fullcalendar/core/locales/fr'

function CalendrierProposition({ events = [] }) {
  // Format cout quand la fenêtre est étroite, long sinon
  const [jourCourt, setJourCourt] = useState(window.innerWidth < 1024)

  useEffect(() => {
    const gererRedimensionnement = () => {
      setJourCourt(window.innerWidth < 1024)
    }
    window.addEventListener('resize', gererRedimensionnement)
    return () => window.removeEventListener('resize', gererRedimensionnement)
  }, [])

  return (
    <FullCalendar
      key={jourCourt ? 'court' : 'long'}
      plugins={[timeGridPlugin, dayGridPlugin]}
      initialView="timeGridWeek"
      events={events}
      locale={frLocale}
      dayHeaderFormat={{ weekday: jourCourt ? 'short' : 'long' }}
      headerToolbar={false}
        slotDuration="00:30:00"
        snapDuration="00:05:00"
        slotLabelInterval="00:30:00"
        slotMinTime="08:00:00"
        slotMaxTime="22:00:00"
        slotLabelFormat={{
            hour: '2-digit',
            minute: '2-digit',
            hour12: false,
        }}
    />
  )
}

export default CalendrierProposition
