import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../services/helper'
import logo from '../assets/logo.png'
import EnTete from '../components/EnTete'
import BarreLaterale from '../components/BarreLaterale'
// Page de connexion — version d'interactivité.

function DashboardProfesseur() {
  return (
    <div>
      <div className="flex flex-col min-h-screen">
        <EnTete />
      <div className="flex flex-1">
        <BarreLaterale />
      <main className="flex-1">
        {/* le contenu principal viendra ici (cartes + calendrier) */}
      </main>
      </div>
      </div>
    </div>
  )
}

export default DashboardProfesseur
