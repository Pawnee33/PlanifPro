import { connecterGoogle, exporterVersGoogle, importerDepuisGoogle } from '../services/google'
import PopupImportGoogle from '../components/eleve/PopupImportGoogle'
import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Menu } from 'lucide-react'
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
  const [creneaux, setCreneaux] = useState([])
  const [eleveSelectionne, setEleveSelectionne] = useState(null)
  const [popupOuvert, setPopupOuvert] = useState(false)
  const [evenementSelectionne, setEvenementSelectionne] = useState(null)
  const [popupImportOuverte, setPopupImportOuverte] = useState(false)
  const [sidebarOuverte, setSidebarOuverte] = useState(false)

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

const chargerCreneaux = () => {
  api.get('/creneaux/')
    .then(setCreneaux)
    .catch(() => setCreneaux([]))
}

// Recharge toutes les données du tableau de bord
const chargerTout = () => {
  chargerClasses()
  chargerEleves()
  chargerEvenements()
  chargerCreneaux()
}

useEffect(() => {
  // Chargement initial au montage
  chargerTout()

  // Rafraîchissement automatique toutes les 10 secondes, pour voir
  // les élèves rejoindre les classes sans recharger la page
  const intervalle = setInterval(chargerTout, 10000)

  // Nettoyage : on arrête l'intervalle quand le composant disparaît
  return () => clearInterval(intervalle)
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
        {/* Burger sidebar — mobile et tablette uniquement */}
        <button
          onClick={() => setSidebarOuverte(true)}
          className="lg:hidden fixed top-24 left-4 z-40 bg-or rounded-full p-2 shadow-lg"
        >
          <Menu className="text-white" />
        </button>

        {/* Overlay sombre — ferme la sidebar au clic (mobile et tablette uniquement) */}
        {sidebarOuverte && (
          <div
            onClick={() => setSidebarOuverte(false)}
            className="lg:hidden fixed inset-0 bg-black/50 z-40"
          />
        )}

        <BarreLaterale
          ouverte={sidebarOuverte}
          onFermer={() => setSidebarOuverte(false)}
          classes={classes}
          eleves={eleves}
          evenements={evenements}
          onCreerClasse={() => setPopupOuvert(true)}
          vueActive={vueActive}
          onChangerVue={(vue) => {
            setVueActive(vue)
            setEleveSelectionne(null)
            setEvenementSelectionne(null)
            setSidebarOuverte(false)
          }}
          onChoisirEleve={(eleve) => {
            setEleveSelectionne(eleve)
            setEvenementSelectionne(null)
            setVueActive(null)
            setSidebarOuverte(false)
          }}
          onChoisirEvenement={(evenement) => {
            setEvenementSelectionne(evenement)
            setEleveSelectionne(null)
            setVueActive(null)
            setSidebarOuverte(false)
          }}
          onExporter={() => exporterVersGoogle(creneaux.map((creneau) => creneau.id))}
          onImporter={() => setPopupImportOuverte(true)}
        />
      <main className="flex-1 min-w-0 p-4 pt-16 lg:p-10 lg:pl-16 bg-bleu-moyen">
        {/* Carte notifications classes et voeux */}
        {vueActive === 'planning' && (
          <>
            {/* Cartes masquées sur téléphone : le calendrier prend tout l'écran */}
            <div className="hidden md:flex flex-wrap gap-8">
              <CarteStat titre="Classes actives" valeur={classes.length} />
              <CarteStat titre="Voeux reçu" valeur={0} />
              <CarteStat titre="Voeux en attente" valeur={0} />
            </div>
            <div className="calendrier-plein-ecran -mx-4 md:mx-0 md:mt-8">
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

        {popupImportOuverte && (
          <PopupImportGoogle
            onFermer={() => setPopupImportOuverte(false)}
            onImporter={(dateDebut, dateFin) => importerDepuisGoogle(dateDebut, dateFin)}
          />
        )}
      </div>
    </div>
  )
}

export default DashboardProfesseur
