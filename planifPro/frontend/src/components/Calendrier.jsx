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
import PopupActionsCreneau from './PopupActionsCreneau'
import PopupScopeCreneau from './PopupScopeCreneau'
import PopupModifierCreneau from './PopupModifierCreneau'
import PopupChoixAjout from './PopupChoixAjout'
import PopupAjouterCours from './PopupAjouterCours'

function Calendrier() {
  const [events, setEvents] = useState([])
  const [creneauObjectif, setCreneauObjectif] = useState(null)
  const [nouveauCreneau, setNouveauCreneau] = useState(null)
  const [creneauxPerso, setCreneauxPerso] = useState([])
  const [persoAGerer, setPersoAGerer] = useState(null)
  const [creneauActions, setCreneauActions] = useState(null)
  const [suppressionScope, setSuppressionScope] = useState(null)
  const [eleves, setEleves] = useState([])
  const [classes, setClasses] = useState([])
  const [creneauxBruts, setCreneauxBruts] = useState([])
  const [modificationCreneau, setModificationCreneau] = useState(null)
  const [choixAjout, setChoixAjout] = useState(null)
  const [ajoutCours, setAjoutCours] = useState(null)

const charger = () => {
    Promise.all([
      api.get('/plannings/global').catch(() => []),
      api.get('/eleves/').catch(() => []),
      api.get('/classes/').catch(() => []),
      api.get('/creneaux/perso/').catch(() => []),
    ]).then(([creneaux, eleves, classes, perso]) => {
      setEleves(eleves)
      setClasses(classes)
      setCreneauxBruts(creneaux)
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
    // Créneau de cours → popup multi-actions
    setCreneauActions({
      creneauId: info.event.extendedProps.creneauId,
      eleveId: info.event.extendedProps.eleveId,
      titre: info.event.title,
      date: info.event.start,
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
    setChoixAjout({ date: dateStr, heure: heureStr })
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

  const ajouterCours = ({ classeId, eleveId, heureDebut, heureFin, scope, date }) => {
    // On retrouve la classe (pour son nom, ses dates) et un créneau existant (pour le planning_id)
    const classe = classes.find((c) => c.id === classeId)
    const creneauDeLaClasse = creneauxBruts.find((c) => c.classe_id === classeId)

    if (!creneauDeLaClasse) {
      alert("Cette classe n'a pas encore de planning validé.")
      return
    }

    // Durée en minutes
    const [hDebut, mDebut] = heureDebut.split(':').map(Number)
    const [hFin, mFin] = heureFin.split(':').map(Number)
    const dureeMinutes = (hFin * 60 + mFin) - (hDebut * 60 + mDebut)

    // Jour de la semaine en français à partir de la date cliquée
    const jours = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']
    const jour = jours[new Date(date).getDay()]

    // Dates de période selon le scope
    const dateDebut = scope === 'ce_jour' ? date : classe.date_debut
    const dateFin = scope === 'ce_jour' ? date : classe.date_fin

    api.post('/creneaux/', {
      planning_id: creneauDeLaClasse.planning_id,
      eleve_id: eleveId,
      classe_id: classeId,
      type: classe.nom,
      jour,
      heure_debut: heureDebut,
      heure_fin: heureFin,
      duree_minutes: dureeMinutes,
      date_debut: dateDebut,
      date_fin: dateFin,
      statut: 'valide',
    })
      .then(() => {
        alert('Cours ajouté !')
        setAjoutCours(null)
        charger()
      })
      .catch(() => alert("Erreur lors de l'ajout du cours"))
  }

  const modifierCreneau = (donnees, scopeInfo) => {
    const payload = { ...donnees, ...scopeInfo }
    api.put(`/creneaux/${modificationCreneau.creneauId}`, payload)
      .then(() => {
        alert('Cours modifié !')
        setModificationCreneau(null)
        charger()
      })
      .catch(() => alert('Erreur lors de la modification'))
  }

  const supprimerCreneau = ({ scope, debut_jour, fin_jour }) => {
    let url = `/creneaux/${suppressionScope.creneauId}?scope=${scope}`
    if (scope !== 'toute_la_periode') {
      url += `&debut_jour=${debut_jour}&fin_jour=${fin_jour}`
    }
    api.delete(url)
      .then(() => {
        alert('Cours supprimé !')
        setSuppressionScope(null)
        charger()
      })
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
      {creneauActions && (
        <PopupActionsCreneau
          ouvert={true}
          onFermer={() => setCreneauActions(null)}
          creneau={creneauActions}
          onObjectif={() => {
            setCreneauObjectif({
              creneauId: creneauActions.creneauId,
              eleveId: creneauActions.eleveId,
              date: creneauActions.date,
            })
            setCreneauActions(null)
          }}

          onModifier={() => {
            setModificationCreneau({
              creneauId: creneauActions.creneauId,
              eleveId: creneauActions.eleveId,
              date: creneauActions.date.toISOString().split('T')[0],
            })
            setCreneauActions(null)
          }}

          onSupprimer={() => {
            setSuppressionScope({
              creneauId: creneauActions.creneauId,
              date: creneauActions.date.toISOString().split('T')[0],
            })
            setCreneauActions(null)
          }}
        />
      )}

      {modificationCreneau && (
        <PopupModifierCreneau
          ouvert={true}
          onFermer={() => setModificationCreneau(null)}
          creneau={modificationCreneau}
          eleves={eleves}
          dateInitiale={modificationCreneau.date}
          onValider={modifierCreneau}
        />
      )}

      {suppressionScope && (
        <PopupScopeCreneau
          ouvert={true}
          onFermer={() => setSuppressionScope(null)}
          titre="Supprimer le cours"
          dateInitiale={suppressionScope.date}
          onValider={supprimerCreneau}
        />
      )}

      {choixAjout && (
        <PopupChoixAjout
          ouvert={true}
          onFermer={() => setChoixAjout(null)}
          onChoixPerso={() => {
            setNouveauCreneau({ date: choixAjout.date, heure: choixAjout.heure })
            setChoixAjout(null)
          }}
          onChoixCours={() => {
            setAjoutCours({ date: choixAjout.date, heure: choixAjout.heure })
            setChoixAjout(null)
          }}
        />
      )}

      {ajoutCours && (
        <PopupAjouterCours
          ouvert={true}
          onFermer={() => setAjoutCours(null)}
          classes={classes}
          dateInitiale={ajoutCours.date}
          heureInitiale={ajoutCours.heure}
          onCreer={ajouterCours}
        />
      )}
    </>
  )
}

export default Calendrier
