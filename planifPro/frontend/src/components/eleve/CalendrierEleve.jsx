import { useState, useEffect } from 'react'
import FullCalendar from '@fullcalendar/react'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import dayGridPlugin from '@fullcalendar/daygrid'
import frLocale from '@fullcalendar/core/locales/fr'
import { api } from '../../services/helper'
import { creneauVersEventRecurrent, creneauPersoVersEvent } from '../../utils/creneaux'
import PopupGererCreneauPerso from '../PopupGererCreneauPerso'
import PopupCreerCreneauPerso from '../PopupCreerCreneauPerso'
import PopupObjectif from './PopupObjectif'

function CalendrierEleve({ refresh, objectifs, professeurs }) {
  const [events, setEvents] = useState([])
  const [creneauxPerso, setCreneauxPerso] = useState([])
  const [persoAGerer, setPersoAGerer] = useState(null)
  const [nouveauCreneau, setNouveauCreneau] = useState(null)
  const [estMobile, setEstMobile] = useState(window.innerWidth < 768 || window.innerHeight < 500)
  const [objectifAffiche, setObjectifAffiche] = useState(null)
  // null = fermé, {} = ouvert

  const charger = () => {
    Promise.all([
      api.get('/creneaux/').catch(() => []),
      api.get('/creneaux/perso/').catch(() => []),
    ]).then(([creneaux, perso]) => {
      setCreneauxPerso(perso)
      const creneauxConfirmes = creneaux.filter((creneau) => creneau.statut === 'confirme')
      const evsCours = creneauxConfirmes.map((creneau) =>
        creneauVersEventRecurrent(creneau, [], creneau.classe_couleur, creneau.professeur_nom)
      )
      const evsPerso = perso.map((creneauPerso) => creneauPersoVersEvent(creneauPerso))
      setEvents([...evsCours, ...evsPerso])
    })
  }

  useEffect(() => {
    charger()
  }, [refresh])

  useEffect(() => {
    const gererRedimensionnement = () => {
      setEstMobile(window.innerWidth < 768 || window.innerHeight < 500)
    }
    window.addEventListener('resize', gererRedimensionnement)
    return () => window.removeEventListener('resize', gererRedimensionnement)
  }, [])

  // Clic sur un créneau : seuls les perso sont gérables (les cours sont en lecture seule)
  const onEventClick = (info) => {
    if (info.event.extendedProps.type === 'perso') {
      const creneauPerso = creneauxPerso.find((c) => c.id === info.event.extendedProps.persoId)
      setPersoAGerer(creneauPerso)
      return
    }
    // Créneau de cours → chercher l'objectif de ce créneau
    const creneauId = info.event.extendedProps.creneauId
    const dateCliquee = info.event.startStr.split('T')[0]  // "AAAA-MM-JJ" de l'occurrence cliquée
    const objectif = objectifs?.find(
      (obj) => obj.creneau_id === creneauId && obj.date_cours === dateCliquee
    )
    setObjectifAffiche({ objectif }) // objectif peut être undefined → « aucun objectif »
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

  const onDateClick = (info) => {
    const date = info.date
    const dateStr = date.toISOString().split('T')[0]
    const heureStr = date.toTimeString().slice(0, 5)
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

  return (
    <>
      <FullCalendar
        key={estMobile ? 'mois' : 'semaine'}
        plugins={[timeGridPlugin, dayGridPlugin, interactionPlugin]}
        initialView={estMobile ? 'dayGridMonth' : 'timeGridWeek'}
        height={estMobile ? `calc(100vh - ${window.innerHeight < 500 ? 30 : 180}px)` : 'auto'}
        events={events}
        locale={frLocale}
        eventClick={onEventClick}
        dateClick={onDateClick}
        headerToolbar={{
          left: 'prev next',
          center: 'title',
          right: estMobile ? 'dayGridMonth' : 'timeGridWeek dayGridMonth',
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

      {nouveauCreneau && (
        <PopupCreerCreneauPerso
          ouvert={true}
          onFermer={() => setNouveauCreneau(null)}
          dateInitiale={nouveauCreneau.date}
          heureInitiale={nouveauCreneau.heure}
          onCreer={creerCreneauPerso}
        />
      )}

      {objectifAffiche && (
        <PopupObjectif
          objectif={objectifAffiche.objectif}
          professeurs={professeurs}
          onFermer={() => setObjectifAffiche(null)}
        />
      )}
    </>
  )
}

export default CalendrierEleve
