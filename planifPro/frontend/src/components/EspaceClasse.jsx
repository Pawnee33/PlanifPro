import { useState, useEffect, useRef } from 'react'
import CarteInfo from './ui/CarteInfo'
import PanneauEleves from './PanneauEleves'
import PanneauVoeux from './PanneauVoeux'
import PanneauPlanning from './PanneauPlanning'
import PopupModifierClasse from './PopupModifierClasse'
import { api } from '../services/helper' // adapte l'import à ton helper
import { CalendarDays, Users, Clock, Pencil, UserPlus } from 'lucide-react'

function EspaceClasse({ classe, onClasseModifiee }) {
  const [ongletActif, setOngletActif] = useState('eleves')
  const [eleves, setEleves] = useState([])
  const [signalPlanning, setSignalPlanning] = useState(0)
  const [popupModifierOuverte, setPopupModifierOuverte] = useState(false)
  const onPlanningGenere = () => setSignalPlanning((n) => n + 1)

  // Recharge les élèves quand on change de classe
  useEffect(() => {
    api
      .get(`/classes/${classe.id}/eleves`)
      .then(setEleves)
      .catch(() => setEleves([]))
  }, [classe.id])

  // --- Helpers d'affichage ---
  const formatDate = (iso) => {
    if (!iso) return ''
    const [annee, mois, jour] = iso.split('-')
    return `${jour}/${mois}/${annee}`
  }

  const formatMoisAnnee = (iso) => {
    if (!iso) return ''
    return new Date(iso).toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' })
  }

  const joursAbrege = {
    lundi: 'Lun', mardi: 'Mar', mercredi: 'Mer', jeudi: 'Jeu',
    vendredi: 'Ven', samedi: 'Sam', dimanche: 'Dim',
  }
  const joursActifs = Object.keys(classe.jours_horaires || {})
  const resumeJours = joursActifs.map((j) => joursAbrege[j]).join(', ')

  const formatDuree = (minutes) => {
    if (minutes === 60) return '1 heure'
    if (minutes % 60 === 0) return `${minutes / 60} heures`
    return `${minutes} min`
  }

  const conteneurRef = useRef(null)

  const onglets = [
    { id: 'eleves', label: `Élèves (${eleves.length})` },
    { id: 'voeux', label: 'Vœux' },
    { id: 'planning', label: 'Planning' },
  ]

  const allerVersOnglet = (index) => {
    const conteneur = conteneurRef.current
    if (conteneur) {
      conteneur.scrollTo({ left: conteneur.offsetWidth * index, behavior: 'smooth' })
    }
  }

  const onScroll = () => {
    const conteneur = conteneurRef.current
    const index = Math.round(conteneur.scrollLeft / conteneur.offsetWidth)
    setOngletActif(onglets[index].id)
  }

  return (
    <div className="flex flex-col gap-4 max-w-4xl mx-auto">
      {/* Carte identité */}
      <div className="bg-bleu-nuit border-3 border-or rounded-2xl p-5 flex items-start justify-between gap-4 flex-wrap">
        <div className="flex items-start gap-4">
          <div
            style={{ backgroundColor: classe.couleur || '#D59813' }}
            className="rounded-xl p-3"
          >
            <CalendarDays className="text-white" />
          </div>
          <div>
            <h2 className="text-2xl text-white font-titre">{classe.nom}</h2>
            <div className="flex flex-wrap gap-4 text-white/80 text-sm mt-2">
              <span className="flex items-center gap-1">
                <CalendarDays size={16} /> {formatMoisAnnee(classe.date_debut)} → {formatMoisAnnee(classe.date_fin)}
              </span>
              <span className="flex items-center gap-1">
                <Users size={16} /> {eleves.length} élèves
              </span>
              <span className="flex items-center gap-1">
                <Clock size={16} /> {resumeJours}
              </span>
            </div>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <button
            onClick={() => setPopupModifierOuverte(true)}
            className="flex items-center gap-2 rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105 transition">
            <Pencil size={16} /> Modifier
          </button>
          <button className="flex items-center gap-2 rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105 transition">
            <UserPlus size={16} /> Inviter un élève
          </button>
        </div>
      </div>

      {/* 3 cartes d'infos */}
      <div className="flex flex-wrap gap-4">
        <CarteInfo titre="Période">
          {formatDate(classe.date_debut)} à {formatDate(classe.date_fin)}
        </CarteInfo>

        <CarteInfo titre="Jours et horaires">
          {joursActifs.map((jour) => (
            <p key={jour} className="capitalize">
              {jour} {classe.jours_horaires[jour].debut} - {classe.jours_horaires[jour].fin}
            </p>
          ))}
        </CarteInfo>

        <CarteInfo titre="Contraintes vœux">
          {classe.nombre_voeux_requis} vœux min - {classe.nombre_jours_min} jours différents
        </CarteInfo>
      </div>

      {/* Code unique */}
      <div className="bg-bleu-nuit border-3 border-or rounded-2xl p-4 flex items-center justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-3">
          <span className="text-white">Code unique de la classe</span>
          <span className="text-or text-[50px] font-titre">{classe.code_classe}</span>
        </div>

        <div className="flex gap-2">
          <button className="rounded-full bg-or border-3 border-or-tres-clair px-4 py-2 text-white text-sm hover:scale-105 transition">
            Copier le code
          </button>
          <button className="rounded-full bg-or border-3 border-or-tres-clair px-4 py-2 text-white text-sm hover:scale-105 transition">
            Inviter par email
          </button>
        </div>
      </div>

      {/* Onglets */}
      <div className="flex gap-24 border-b-4 border-white/20">
        {onglets.map((onglet, index) => (
          <button
            key={onglet.id}
            onClick={() => allerVersOnglet(index)}
            className={`pb-2 text-lg transition ${
              ongletActif === onglet.id
                ? 'text-or border-b-6 border-or'
                : 'text-white/70 hover:text-white'
            }`}
          >
            {onglet.label}
          </button>
        ))}
      </div>

      {/* Contenu swipable */}
      <div
        ref={conteneurRef}
        onScroll={onScroll}
        className="flex overflow-x-auto snap-x snap-mandatory"
      >
        {/* Panneau Élèves */}
        <div className="w-full shrink-0 snap-center">
          <PanneauEleves eleves={eleves} classe={classe} />
        </div>

        {/* Panneau Vœux */}
        <div className="w-full shrink-0 snap-center">
          <PanneauVoeux eleves={eleves} classe={classe} onPlanningGenere={onPlanningGenere} />
        </div>

        {/* Panneau Planning */}
        <div className="w-full shrink-0 snap-center">
          <PanneauPlanning classe={classe} eleves={eleves} signal={signalPlanning} />
        </div>
      </div>
      <PopupModifierClasse
        ouvert={popupModifierOuverte}
        onFermer={() => setPopupModifierOuverte(false)}
        classe={classe}
        onClasseModifiee={() => {
          onClasseModifiee()              // recharge la liste du dashboard
          setPopupModifierOuverte(false)  // ferme la popup
        }}
      />
    </div>
  )
} 

export default EspaceClasse
