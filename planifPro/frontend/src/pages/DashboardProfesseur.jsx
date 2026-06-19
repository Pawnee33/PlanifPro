import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../services/helper'
import logo from '../assets/logo.png'
import EnTete from '../components/EnTete'
import BarreLaterale from '../components/BarreLaterale'
import PiedDePage from '../components/PiedDePage'
import Calendrier from '../components/Calendrier'
import PopupCreerClasse from '../components/PopupCreerClasse'
import CarteStat from '../components/ui/CarteStat'
// Page de connexion — version d'interactivité.

function DashboardProfesseur() {
  const [vueActive, setVueActive] = useState('planning')
  const [classes, setClasses] = useState([])
  const [popupOuvert, setPopupOuvert] = useState(false)

  const chargerClasses = () => {
    api.get('/classes/')
      .then(setClasses)
      .catch(() => setClasses([])) // 404 si aucune classe, liste vide
  }
  useEffect(() => {
    chargerClasses()
  }, [])

  // On retrouve la classe dont l'id correspond à la vue active (undefined si aucune)
  const classeSelectionnee = classes.find((c) => c.id === vueActive)

  return (
    <div>
      <div className="flex flex-col min-h-screen">
        <EnTete />
      <div className="flex flex-1">
        <BarreLaterale
          classes={classes}
          onCreerClasse={() => setPopupOuvert(true)}
          vueActive={vueActive}
          onChangerVue={setVueActive}
        />
      <main className="flex-1 min-w-0 p-10 pl-16 bg-bleu/50">
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

        {classeSelectionnee && (
          <div>
            <h2 className="text-2xl text-white font-titre mb-4">{classeSelectionnee.nom}</h2>
            {/* contenu de la classe à venir */}
          </div>
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
