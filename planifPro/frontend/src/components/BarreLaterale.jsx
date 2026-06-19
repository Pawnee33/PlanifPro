import React from 'react'
import { useState } from 'react'
import SectionBarre from './ui/SectionBarre'
import { Users, CalendarDays, CalendarArrowDown, CalendarArrowUp, GraduationCap, Star, ChevronDown, ChevronUp } from 'lucide-react'
import logo from '../assets/logo.png'

const BarreLaterale = ({ classes, onCreerClasse, vueActive, onChangerVue }) => {
    const [classesOuvert, setClassesOuvert] = useState(false)
    const [elevesOuvert, setElevesOuvert] = useState(false)
    const [evenementsOuvert, setEvenementsOuvert] = useState(false)
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
                    messageVide="Aucun élève pour le moment"
                    libelleBouton="+ Inviter un élève"
                    />
                </div>

                {/* Bouton Événements */}
                <div>
                    <SectionBarre
                    icone={<Star />}
                    titre="Événements"
                    messageVide="Aucun événement pour le moment"
                    libelleBouton="+ Ajouter un événement"
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
        </aside>
    )
}

export default BarreLaterale
