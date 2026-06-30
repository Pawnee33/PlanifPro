import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../../services/helper'
import logo from '../../assets/logo.png'
import EnTete from '../../components/EnTete'
import BarreLateraleEleve from '../../components/eleve/BarreLateraleEleve'
import FormulaireVoeux from '../../components/eleve/FormulaireVoeux'
import PiedDePage from '../../components/PiedDePage'
import CalendrierEleve from '../../components/eleve/CalendrierEleve'
import { CalendarCheck, Mail } from 'lucide-react'

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
  const [creneaux, setCreneaux] = useState([])
  const [refreshCalendrier, setRefreshCalendrier] = useState(0)
  
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

  const chargerCreneaux = () => {
    api.get('/creneaux/')
      .then(setCreneaux)
      .catch(() => setCreneaux([]))
  }

useEffect(() => {
  chargerObjectifs()
  chargerProfesseurs()
  chargerEvenements()
  chargerNotifications()
  chargerVoeux()
  chargerCreneaux()
}, [])

  const collecteOuverte = notifications.find(
      (notif) => notif.type === 'collecte_voeux'
    )

  const voeuxNonSoumis = voeux.length === 0

  const aRejointUneClasse = professeurs.length > 0

  const afficherBanniereVoeux = collecteOuverte && voeuxNonSoumis && aRejointUneClasse

  const creneauAConfirmer = creneaux.find(
    (creneau) => creneau.statut !== 'confirme'
  )

  const confirmerCreneau = (creneauId) => {
    api.put(`/creneaux/${creneauId}/confirmer`)
      .then(() => {
        alert('Créneau ajouté à votre planning !')
        chargerCreneaux() // recharge → la bannière disparaît, le créneau s'affiche
        setRefreshCalendrier((n) => n + 1)
      })
      .catch((err) => alert(err.message))
  }

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
              <div className="flex items-center gap-4 bg-bleu-nuit border-2 border-or rounded-2xl px-5 py-4 mb-6 max-w-3xl">
                {/* Icône */}
                <div className="rounded-full bg-or w-12 h-12 flex items-center justify-center shrink-0">
                  <Mail className="text-white" />
                </div>

                {/* Texte */}
                <p className="text-white flex-1">
                  {professeurs[0] ? `${professeurs[0].prenom} ${professeurs[0].nom}` : 'Votre professeur'} a envoyé le formulaire de vœux
                </p>

                {/* Bouton */}
                <button
                  onClick={() => setPopupVoeuxOuverte(true)}
                  className="rounded-full bg-bleu-roi px-5 py-2 border border-tracer-violet text-white hover:scale-105 transition shrink-0"
                >
                  Soumettre vos vœux
                </button>
              </div>
            )}

            {creneauAConfirmer && (
              <div className="flex items-center gap-4 bg-bleu-nuit border-2 border-or rounded-2xl px-5 py-4 mb-6 max-w-3xl">
                {/* Icône */}
                <div className="rounded-full bg-or w-12 h-12 flex items-center justify-center shrink-0">
                  <CalendarCheck className="text-white" />
                </div>

                {/* Infos sur deux lignes */}
                <div className="flex-1">
                  <p className="text-white text-lg">
                    {creneauAConfirmer.type} : {creneauAConfirmer.jour} {creneauAConfirmer.heure_debut.slice(0, 5)}
                  </p>
                  <p className="text-white/70 text-sm">
                    Professeur {creneauAConfirmer.professeur_nom} : {creneauAConfirmer.duree_minutes} min
                  </p>
                </div>

                {/* Bouton */}
                <button
                  onClick={() => confirmerCreneau(creneauAConfirmer.id)}
                  className="rounded-full bg-bleu-roi px-5 py-2 border border-tracer-violet text-white hover:scale-105 transition shrink-0"
                >
                  Ajouter au calendrier
                </button>
              </div>
            )}

            <div className="mt-8">
              <CalendrierEleve refresh={refreshCalendrier} />
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