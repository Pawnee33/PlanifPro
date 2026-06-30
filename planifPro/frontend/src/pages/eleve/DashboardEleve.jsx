import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../../services/helper'
import logo from '../../assets/logo.png'
import EnTete from '../../components/EnTete'
import BarreLateraleEleve from '../../components/eleve/BarreLateraleEleve'
import FormulaireVoeux from '../../components/eleve/FormulaireVoeux'
import PiedDePage from '../../components/PiedDePage'
import CalendrierEleve from '../../components/eleve/CalendrierEleve'

// Page de connexion — version d'interactivité.

function DashboardEleve() {
  const [vueActive, setVueActive] = useState('planning')
  const [popupOuvert, setPopupOuvert] = useState(false)
  const [professeurs, setProfesseurs] = useState([])
  const [objectifs, setObjectifs] = useState([])
  const [evenements, setEvenements] = useState([])
  const [notifications, setNotifications] = useState([])
  const [voeux, setVoeux] = useState([])
  const [popupVoeuxOuverte, setPopupVoeuxOuverte] = useState(false)
  
  const chargerObjectifs = () => {
    api.get('/objectifs/')
      .then(setObjectifs)
      .catch(() => setObjectifs([])) // 404 si aucun objectifs, liste vide
  }

  const chargerProfesseurs = () => {
    api.get('/professeurs/')
      .then(setProfesseurs)
      .catch(() => setProfesseurs([])) // 404 si aucun professeurs, liste vide
  }

  const chargerEvenements = () => {
    api.get('/evenements/')
      .then(setEvenements)
      .catch(() => setEvenements([])) // 404 si aucun événements, liste vide
  }

  const chargerNotifications = () => {
    api.get('/notifications/')
      .then(setNotifications)
      .catch(() => setNotifications([]))
  }

  const chargerVoeux = () => {
    api.get('/voeux/')
      .then(setVoeux)
      .catch(() => setVoeux([])) // 404 si aucun vœu
  }

useEffect(() => {
  chargerObjectifs()
  chargerProfesseurs()
  chargerEvenements()
  chargerNotifications()
  chargerVoeux()
}, [])

  const collecteOuverte = notifications.find(
      (notif) => notif.type === 'collecte_voeux'
    )

  const voeuxNonSoumis = voeux.length === 0

  const afficherBanniereVoeux = collecteOuverte && voeuxNonSoumis

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
          objectifs={objectifs}
          professeurs={professeurs}
          evenements={evenements}
          vueActive={vueActive}
          onChangerVue={setVueActive}
          onRejoint={chargerProfesseurs}
        />
      <main className="flex-1 min-w-0 p-10 pl-16 bg-bleu-moyen">
        {/* Carte notifications classes et voeux */}
        {vueActive === 'planning' && (
          <>
            {afficherBanniereVoeux && (
              <div className="flex items-center justify-between bg-bleu-nuit border-2 border-or rounded-2xl px-5 py-4 mb-6">
                <p className="text-white">{collecteOuverte.message}</p>
                <button
                  onClick={() => setPopupVoeuxOuverte(true)}
                  className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105 transition"
                >
                  Soumettre vos vœux
                </button>
              </div>
            )}

            <div className="mt-8">
              <CalendrierEleve />
            </div>
          </>
        )}

      </main>
      </div>
        <div className="flex flex-col min-b-screen">
          <PiedDePage />
        </div>
      </div>
      {popupVoeuxOuverte && (
        <FormulaireVoeux
          ouvert={true}
          onFermer={() => setPopupVoeuxOuverte(false)}
          onVoeuxSoumis={chargerVoeux}
        />
      )}
    </div>
  )
}

export default DashboardEleve