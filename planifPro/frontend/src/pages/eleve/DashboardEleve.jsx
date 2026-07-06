import { exporterVersGoogle, importerDepuisGoogle } from '../../services/google'
import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../../services/helper'
import logo from '../../assets/logo.png'
import EnTete from '../../components/EnTete'
import BarreLateraleEleve from '../../components/eleve/BarreLateraleEleve'
import PopupRejoindreClasse from '../../components/eleve/PopupRejoindreClasse'
import FicheObjectif from '../../components/eleve/FicheObjectif'
import FicheEvenement from '../../components/eleve/FicheEvenement'
import FicheProfesseur from '../../components/eleve/FicheProfesseur'
import FormulaireVoeux from '../../components/eleve/FormulaireVoeux'
import PiedDePage from '../../components/PiedDePage'
import CalendrierEleve from '../../components/eleve/CalendrierEleve'
import PopupImportGoogle from '../../components/eleve/PopupImportGoogle'
import { CalendarCheck, Mail, Menu } from 'lucide-react'

// Page de connexion — version d'interactivité.

function DashboardEleve() {
  const [vueActive, setVueActive] = useState('planning')
  const [popupOuvert, setPopupOuvert] = useState(false)
  const [professeurs, setProfesseurs] = useState([])
  const [mesClasses, setMesClasses] = useState([])
  const [objectifs, setObjectifs] = useState([])
  const [evenements, setEvenements] = useState([])
  const [notifications, setNotifications] = useState([])
  const [voeux, setVoeux] = useState([])
  const [classes, setClasses] = useState([])
  const [popupRejoindreOuverte, setPopupRejoindreOuverte] = useState(false)
  const [popupVoeuxOuverte, setPopupVoeuxOuverte] = useState(false)
  const [popupImportOuverte, setPopupImportOuverte] = useState(false)
  const [creneaux, setCreneaux] = useState([])
  const [refreshCalendrier, setRefreshCalendrier] = useState(0)
  const [sidebarOuverte, setSidebarOuverte] = useState(false)
  const [selection, setSelection] = useState(null)
  // selection = { type: 'objectif' | 'evenement' | 'professeur', donnees: {...} }
  
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

  const chargerClasses = () => {
    api.get('/classes/')
      .then(setClasses)
      .catch(() => setClasses([]))
  }

  const chargerMesClasses = () => {
  api.get('/eleves/mes-classes')
    .then(setMesClasses)
    .catch(() => setMesClasses([]))
}

useEffect(() => {
  chargerObjectifs()
  chargerProfesseurs()
  chargerEvenements()
  chargerNotifications()
  chargerVoeux()
  chargerCreneaux()
  chargerClasses()
  chargerMesClasses()
}, [])

  // Classes dont la collecte est ouverte et pour lesquelles l'élève n'a pas encore soumis de vœu
  const classesEnAttenteDeVoeux = mesClasses.filter(
    (classe) =>
      classe.statut === 'collecte_active' &&
      !voeux.some((voeu) => voeu.classe_id === classe.id)
  )

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
            setSelection(null)
          }}
        />
      <div className="flex flex-1">
        {/* Burger sidebar — mobile uniquement */}
        <button
          onClick={() => setSidebarOuverte(true)}
          className="lg:hidden fixed top-24 left-4 z-40 bg-or rounded-full p-2 shadow-lg"
        >
          <Menu className="text-white" />
        </button>

        {/* Overlay sombre — ferme la sidebar au clic (mobile uniquement) */}
        {sidebarOuverte && (
          <div
            onClick={() => setSidebarOuverte(false)}
            className="lg:hidden fixed inset-0 bg-black/50 z-40"
          />
        )}

        <BarreLateraleEleve
          ouverte={sidebarOuverte}
          onFermer={() => setSidebarOuverte(false)}
          objectifs={objectifs}
          professeurs={professeurs}
          evenements={evenements}
          vueActive={vueActive}
          onChangerVue={(vue) => { setVueActive(vue); setSelection(null) }}
          onRejoint={chargerProfesseurs}
          onRejoindreClasse={() => setPopupRejoindreOuverte(true)}
          onChoisirObjectif={(objectif) => { setSelection({ type: 'objectif', donnees: objectif }); setVueActive(null) }}
          onChoisirEvenement={(evenement) => { setSelection({ type: 'evenement', donnees: evenement }); setVueActive(null) }}
          onChoisirProfesseur={(professeur) => { setSelection({ type: 'professeur', donnees: professeur }); setVueActive(null) }}
          onExporter={() => exporterVersGoogle(creneaux.map((creneau) => creneau.id))}
          onImporter={() => setPopupImportOuverte(true)}
        />
      <main className="flex-1 min-w-0 p-4 lg:p-10 lg:pl-16 bg-bleu-moyen">
        {/* Carte notifications classes et voeux */}
        {vueActive === 'planning' && (
          <>
            {classesEnAttenteDeVoeux.map((classe) => (
              <div key={classe.id} className="flex items-center gap-4 bg-bleu-nuit border-2 border-or rounded-2xl px-5 py-4 mb-6 max-w-3xl">
                {/* Icône */}
                <div className="rounded-full bg-or w-12 h-12 flex items-center justify-center shrink-0">
                  <Mail className="text-white" />
                </div>

                {/* Texte */}
                <p className="text-white flex-1">
                  {classe.professeur_prenom} {classe.professeur_nom} a envoyé le formulaire de vœux pour la classe {classe.nom}
                </p>

                {/* Bouton */}
                <button
                  onClick={() => setPopupVoeuxOuverte(classe)}
                  className="rounded-full bg-bleu-roi px-5 py-2 border border-tracer-violet text-white hover:scale-105 transition shrink-0"
                >
                  Soumettre vos vœux
                </button>
              </div>
            ))}

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

            <div className="mt-4 lg:mt-8">
              <CalendrierEleve refresh={refreshCalendrier} objectifs={objectifs} professeurs={professeurs} />
            </div>
          </>
        )}

        {selection?.type === 'objectif' && <FicheObjectif objectif={selection.donnees} professeurs={professeurs} />}
        {selection?.type === 'evenement' && <FicheEvenement evenement={selection.donnees} professeurs={professeurs} />}
        {selection?.type === 'professeur' && <FicheProfesseur professeur={selection.donnees} classes={classes} />}
      </main>
      </div>
        <div className="flex flex-col min-b-screen">
          <PiedDePage />
        </div>
      </div>

      {popupRejoindreOuverte && (
        <PopupRejoindreClasse
          ouvert={true}
          onFermer={() => setPopupRejoindreOuverte(false)}
          onRejoint={chargerProfesseurs}
        />
      )}

      {popupVoeuxOuverte && (
        <FormulaireVoeux
          ouvert={true}
          classe={popupVoeuxOuverte}
          onFermer={() => setPopupVoeuxOuverte(false)}
          onVoeuxSoumis={() => { chargerVoeux(); chargerMesClasses() }}
        />
      )}

      {popupImportOuverte && (
        <PopupImportGoogle
          onFermer={() => setPopupImportOuverte(false)}
          onImporter={(dateDebut, dateFin) => importerDepuisGoogle(dateDebut, dateFin)}
        />
      )}
    </div>
  )
}

export default DashboardEleve