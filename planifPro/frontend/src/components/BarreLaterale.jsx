import React from 'react'
import { useState } from 'react'
import { api } from '../services/helper'
import PopupInviterEleveClasse from './PopupInviterEleveClasse'
import PopupCreerEvenement from './PopupCreerEvenement'
import SectionBarre from './ui/SectionBarre'
import { Users, CalendarDays, CalendarArrowDown, CalendarArrowUp, GraduationCap, Star, ChevronDown, ChevronUp } from 'lucide-react'
import logo from '../assets/logo.png'

const BarreLaterale = ({ classes, eleves, evenements, onCreerClasse, vueActive, onChangerVue, onChoisirEleve, onChoisirEvenement }) => {
    const [classesOuvert, setClassesOuvert] = useState(false)
    const [elevesOuvert, setElevesOuvert] = useState(false)
    const [evenementsOuvert, setEvenementsOuvert] = useState(false)
    const [popupInviterOuverte, setPopupInviterOuverte] = useState(false)
    const [popupEvenementOuverte, setPopupEvenementOuverte] = useState(false)

    const inviterEleve = (classeId, email) => {
        api.post(`/classes/${classeId}/inviter`, { email })
            .then(() => {
            alert('Invitation envoyée !')
            setPopupInviterOuverte(false)
            })
            .catch(() => alert("Erreur lors de l'envoi de l'invitation"))
        }

    const creerEvenement = (donnees) => {
        api.post('/evenements/', donnees)
            .then(() => {
            alert('Événement créé et notifications envoyées !')
            setPopupEvenementOuverte(false)
            })
            .catch(() => alert("Erreur lors de la création de l'événement"))
        }

    return (
        <aside className='w-64 flex flex-col gap-3 bg-bleu-marine border-r-[4px] border-tracer-violet p-4'>

            <div className="flex flex-col gap-5">

            {/* Bouton Planning */}
            <div>
                <button
                    onClick={() => onChangerVue('planning')}
                    className={
                        `flex items-center gap-6 rounded-[16px] w-full px-4 py-3 text-white hover:brightness-110
                        transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]
                        ${vueActive === 'planning' ? 'bg-or' : 'bg-bleu-nuit'
                    }`}
                >
                    <CalendarDays />
                    Planning
                </button>
            </div>

                {/* Bouton Mes classes */}
                <div>
                    <SectionBarre
                        icone={<Users fill="currentColor" />}
                        titre="Mes classes"
                        elements={classes}
                        getLabel={(classe) => classe.nom}
                        messageVide="Aucune classe pour le moment"
                        libelleBouton="+ Créer une classe"
                        onAction={onCreerClasse}
                        vueActive={vueActive}
                        onChangerVue={onChangerVue}
                    />
                </div>

                {/* Bouton Mes élèves */}
                <div>
                    <SectionBarre
                    icone={<GraduationCap />}
                    titre="Mes élèves"
                    elements={eleves.map((e) => ({ ...e, couleur: e.classe_couleur }))}
                    getLabel={(eleve) => `${eleve.prenom} ${eleve.nom}`}
                    messageVide="Aucun élève pour le moment"
                    libelleBouton="+ Inviter un élève"
                    onAction={() => setPopupInviterOuverte(true)}
                    onChangerVue={(id) => onChoisirEleve(eleves.find((e) => e.id === id))}
                    />
                </div>

                {/* Bouton Événements */}
                <div>
                    <SectionBarre
                    icone={<Star />}
                    titre="Événements"
                    elements={evenements}
                    getLabel={(evenement) => evenement.titre}
                    messageVide="Aucun événement pour le moment"
                    libelleBouton="+ Ajouter un événement"
                    onAction={() => setPopupEvenementOuverte(true)}
                    onChangerVue={(id) => onChoisirEvenement(evenements.find((e) => e.id === id))}
                    />
                </div>

                {/* Bouton exporter vers Google Calendar */}
                <div>
                    <button className="flex items-center mt-6 gap-6 rounded-full bg-or w-full px-4 py-3 text-white hover:brightness-110 transition shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]">
                        <CalendarArrowDown />
                        <span className="flex flex-col items-start">
                            <span>Exporter</span>
                            <span className="text-xs">vers Google Calendar</span>
                        </span>
                    </button>
                </div>

                {/* Bouton importer vers Google Calendar */}
                <div>
                    <button className="flex items-center mt-3 gap-6 rounded-full bg-or w-full px-4 py-3 text-white hover:brightness-110 transition shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]">
                        <CalendarArrowUp />
                        <span className="flex flex-col items-start">
                            <span>Importer</span>
                            <span className="text-xs">vers le Planning</span>
                        </span>
                    </button>
                </div>
            </div>
            <PopupInviterEleveClasse
              ouvert={popupInviterOuverte}
              onFermer={() => setPopupInviterOuverte(false)}
              classes={classes}
              onInviter={inviterEleve}
            />

            <PopupCreerEvenement
              ouvert={popupEvenementOuverte}
              onFermer={() => setPopupEvenementOuverte(false)}
              onCreer={creerEvenement}
              classes={classes}
              eleves={eleves}
            />
        </aside>
    )
}

export default BarreLaterale
