import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import dayGridPlugin from '@fullcalendar/daygrid'
import frLocale from '@fullcalendar/core/locales/fr'

function Calendrier() {
  return (
    <FullCalendar
      plugins={[timeGridPlugin, dayGridPlugin]}
      initialView="timeGridWeek"
      locale={frLocale}
      headerToolbar={{
        left: 'prev,next',
        center: 'title',
        right: 'timeGridWeek,dayGridMonth',
      }}
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

export default Calendrier
