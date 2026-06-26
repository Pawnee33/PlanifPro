import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../services/helper'
import logo from '../assets/logo.png'
import EnTete from '../components/EnTete'
import BarreLaterale from '../components/BarreLaterale'
import PiedDePage from '../components/PiedDePage'
import Calendrier from '../components/Calendrier'
import PopupCreerClasse from '../components/PopupCreerClasse'
import EspaceClasse from '../components/EspaceClasse'
import CarteStat from '../components/ui/CarteStat'
import FicheEleve from '../components/FicheEleve'
import FicheEvenement from '../components/FicheEvenement'
// Page de connexion — version d'interactivité.

function DashboardProfesseur() {
  const [vueActive, setVueActive] = useState('planning')
  const [classes, setClasses] = useState([])
  const [eleves, setEleves] = useState([])
  const [evenements, setEvenements] = useState([])
  const [eleveSelectionne, setEleveSelectionne] = useState(null)
  const [popupOuvert, setPopupOuvert] = useState(false)
  const [evenementSelectionne, setEvenementSelectionne] = useState(null)

  const chargerClasses = () => {
    api.get('/classes/')
      .then(setClasses)
      .catch(() => setClasses([])) // 404 si aucune classe, liste vide
  }

  const chargerEleves = () => {
  api.get('/eleves/')
    .then(setEleves)
    .catch(() => setEleves([]))
}

const chargerEvenements = () => {
  api.get('/evenements/')
    .then(setEvenements)
    .catch(() => setEvenements([]))
}

useEffect(() => {
  chargerClasses()
  chargerEleves()
  chargerEvenements()
}, [])

  // On retrouve la classe dont l'id correspond à la vue active (undefined si aucune)
  const classeSelectionnee = classes.find((c) => c.id === vueActive)

  return (
    <div>
      <div className="flex flex-col min-h-screen">
        <EnTete
          onAccueil={() => {
            setVueActive('planning')
            setEleveSelectionne(null)
            setEvenementSelectionne(null)
          }}
        />
      <div className="flex flex-1">
        <BarreLaterale
          classes={classes}
          eleves={eleves}
          evenements={evenements}
          onCreerClasse={() => setPopupOuvert(true)}
          vueActive={vueActive}
          onChangerVue={(vue) => {
            setVueActive(vue)
            setEleveSelectionne(null)
            setEvenementSelectionne(null)
          }}
          onChoisirEleve={(eleve) => {
            setEleveSelectionne(eleve)
            setEvenementSelectionne(null)
            setVueActive(null)
          }}
          onChoisirEvenement={(evenement) => {
            setEvenementSelectionne(evenement)
            setEleveSelectionne(null)
            setVueActive(null)
          }}
        />
      <main className="flex-1 min-w-0 p-10 pl-16 bg-bleu-moyen">
        {/* Carte notifications classes et voeux */}
        {vueActive === 'planning' && (
          <>
            <div className="flex flex-wrap gap-8">
              <CarteStat titre="Classes actives" valeur={classes.length} />
              <CarteStat titre="Voeux reçu" valeur={0} />
              <CarteStat titre="Voeux en attente" valeur={0} />
            </div>
            <div className="mt-8">
              <Calendrier />
            </div>
          </>
        )}

        {/* Main Mes Classes */}
        {classeSelectionnee && (
          <EspaceClasse classe={classeSelectionnee} onClasseModifiee={chargerClasses} />
        )}

        {/* Main Mes Élèves */}
        {eleveSelectionne && (
          <FicheEleve eleve={eleveSelectionne} />
        )}

        {/* Main Mes Événements */}
        {evenementSelectionne && (
          <FicheEvenement
            evenement={evenementSelectionne}
            onSupprime={() => {
              setEvenementSelectionne(null)
              chargerEvenements()
            }}
            onModifie={() => {
              setEvenementSelectionne(null)
              chargerEvenements()
            }}
          />
        )}
      </main>
      </div>
        <div className="flex flex-col min-b-screen">
          <PiedDePage />
        </div>
        <PopupCreerClasse
          ouvert={popupOuvert}
          onFermer={() => setPopupOuvert(false)}
          onClasseCree={chargerClasses}
        />
      </div>
    </div>
  )
}

export default DashboardProfesseur
