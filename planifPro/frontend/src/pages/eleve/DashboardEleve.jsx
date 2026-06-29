import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../../services/helper'
import logo from '../../assets/logo.png'
import EnTete from '../../components/EnTete'
import BarreLateraleEleve from '../../components/eleve/BarreLateraleEleve'
import PiedDePage from '../../components/PiedDePage'
import Calendrier from '../../components/Calendrier'

// Page de connexion — version d'interactivité.

function DashboardEleve() {
  const [vueActive, setVueActive] = useState('planning')
  const [popupOuvert, setPopupOuvert] = useState(false)
  const [professeurs, setProfesseurs] = useState([])

    const chargerProfesseurs = () => {
    api.get('/professeurs/')
      .then(setProfesseurs)
      .catch(() => setProfesseurs([])) // 404 si aucun professeurs, liste vide
  }

useEffect(() => {
  chargerProfesseurs()
}, [])

  return (
    <div>
      <div className="flex flex-col min-h-screen">
        <EnTete
          onAccueil={() => {
            setVueActive('planning')
          }}
        />
      <div className="flex flex-1">
        <BarreLateraleEleve
          objectifs={[]}
          professeurs={professeurs}
          evenements={[]}
          vueActive={vueActive}
          onChangerVue={setVueActive}
          onRejoint={chargerProfesseurs}
        />
      <main className="flex-1 min-w-0 p-10 pl-16 bg-bleu-moyen">
        {/* Carte notifications classes et voeux */}
        {vueActive === 'planning' && (
          <>
            <div className="mt-8">
              <Calendrier />
            </div>
          </>
        )}

      </main>
      </div>
        <div className="flex flex-col min-b-screen">
          <PiedDePage />
        </div>
      </div>
    </div>
  )
}

export default DashboardEleve