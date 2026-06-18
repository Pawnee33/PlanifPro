import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../services/helper'
import logo from '../assets/logo.png'
import EnTete from '../components/EnTete'
import BarreLaterale from '../components/BarreLaterale'
import PiedDePage from '../components/PiedDePage'
import CarteStat from '../components/ui/CarteStat'
// Page de connexion — version d'interactivité.

function DashboardProfesseur() {
  return (
    <div>
      <div className="flex flex-col min-h-screen">
        <EnTete />
      <div className="flex flex-1">
        <BarreLaterale />
      <main className="flex-1 min-w-0 p-10 pl-16">
        {/* Carte notifications classes et voeux */}
        <div className="flex flex-wrap gap-8">
          <CarteStat titre="Classes actives" valeur={0} />
          <CarteStat titre="Voeux reçu" valeur={0} />
          <CarteStat titre="Voeux en attente" valeur={0} />
        </div>
      </main>
      </div>
        <div className="flex flex-col min-b-screen">
          <PiedDePage />
        </div>
      </div>
    </div>
  )
}

export default DashboardProfesseur
