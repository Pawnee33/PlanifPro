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
  const [classes, setClasses] = useState([])
  const [popupOuvert, setPopupOuvert] = useState(false)

  useEffect(() => {
    api.get('/classes/')
    .then(setClasses)
    .catch(() => setClasses([]))
  }, [])
  return (
    <div>
      <div className="flex flex-col min-h-screen">
        <EnTete />
      <div className="flex flex-1">
        <BarreLaterale classes={classes} onCreerClasse={() => setPopupOuvert(true)} />
      <main className="flex-1 min-w-0 p-10 pl-16 bg-bleu/50">
        {/* Carte notifications classes et voeux */}
        <div className="flex flex-wrap gap-8">
          <CarteStat titre="Classes actives" valeur={classes.length} />
          <CarteStat titre="Voeux reçu" valeur={0} />
          <CarteStat titre="Voeux en attente" valeur={0} />
        </div>
        <div className="mt-8">
          <Calendrier />
        </div>
      </main>
      </div>
        <div className="flex flex-col min-b-screen">
          <PiedDePage />
        </div>
        <PopupCreerClasse ouvert={popupOuvert} onFermer={() => setPopupOuvert(false)} />
      </div>
    </div>
  )
}

export default DashboardProfesseur
