import { useState, useEffect } from 'react'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import dayGridPlugin from '@fullcalendar/daygrid'
import frLocale from '@fullcalendar/core/locales/fr'
import { api } from '../../services/helper'
import { creneauVersEventRecurrent, creneauPersoVersEvent } from '../../utils/creneaux'
import PopupGererCreneauPerso from '../PopupGererCreneauPerso'

function CalendrierEleve() {
  const [events, setEvents] = useState([])
  const [creneauxPerso, setCreneauxPerso] = useState([])
  const [persoAGerer, setPersoAGerer] = useState(null)

  const charger = () => {
    Promise.all([
      api.get('/creneaux/').catch(() => []),
      api.get('/creneaux/perso/').catch(() => []),
    ]).then(([creneaux, perso]) => {
      setCreneauxPerso(perso)
      const evsCours = creneaux.map((creneau) =>
        creneauVersEventRecurrent(creneau, [], creneau.classe_couleur, creneau.type)
      )
      const evsPerso = perso.map((creneauPerso) => creneauPersoVersEvent(creneauPerso))
      setEvents([...evsCours, ...evsPerso])
    })
  }

  useEffect(() => {
    charger()
  }, [])

  // Clic sur un créneau : seuls les perso sont gérables (les cours sont en lecture seule)
  const onEventClick = (info) => {
    if (info.event.extendedProps.type === 'perso') {
      const creneauPerso = creneauxPerso.find((c) => c.id === info.event.extendedProps.persoId)
      setPersoAGerer(creneauPerso)
    }
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

export default CalendrierEleve
