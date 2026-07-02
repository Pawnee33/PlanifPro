import React from 'react'
import { useState } from 'react'
import { api } from '../../services/helper'
import PopupRejoindreClasse from './PopupRejoindreClasse'
import SectionBarre from '../ui/SectionBarre'
import { supprimerDeGoogle } from '../../services/google'
import { Users, CalendarDays, CalendarArrowDown, CalendarArrowUp, GraduationCap, Star, ChevronDown, ChevronUp } from 'lucide-react'

const BarreLateraleEleve = ({ objectifs, professeurs, evenements, onRejoindreClasse, vueActive, onChangerVue, onChoisirProfesseur, onChoisirEvenement, onChoisirObjectif, onRejoint, onExporter, onImporter }) => {
    const [objectifsOuvert, setObejectifsOuvert] = useState(false)
    const [professeursOuvert, setProfesseursOuvert] = useState(false)
    const [evenementsOuvert, setEvenementsOuvert] = useState(false)
    const [popupRejoindreOuverte, setPopupRejoindreOuverte] = useState(false)
    const [popupEvenementOuverte, setPopupEvenementOuverte] = useState(false)

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

                {/* Bouton Mes Objectifs */}
                <div>
                    <SectionBarre
                        icone={<Users fill="currentColor" />}
                        titre="Mes Objectifs"
                        elements={objectifs}
                        getLabel={(objectif) => objectif.contenu}
                        messageVide="Aucun objectifs pour le moment"
                        vueActive={vueActive}
                        onChangerVue={(id) => onChoisirObjectif(objectifs.find((o) => o.id === id))}
                    />
                </div>

                {/* Bouton Mes Professeurss */}
                <div>
                    <SectionBarre
                    icone={<GraduationCap />}
                    titre="Mes Professeurs"
                    elements={professeurs.map((p) => ({ ...p, couleur: p.classe_couleur }))}
                    getLabel={(professeur) => `${professeur.prenom} ${professeur.nom}`}
                    messageVide="Aucun Professeur pour le moment"
                    libelleBouton="+ Rejoindre une classe"
                    onAction={() => setPopupRejoindreOuverte(true)}
                    onChangerVue={(id) => onChoisirProfesseur(professeurs.find((p) => p.id === id))}
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
                    onChangerVue={(id) => onChoisirEvenement(evenements.find((e) => e.id === id))}
                    />
                </div>

                {/* Bouton exporter vers Google Calendar */}
                <div>
                    <button
                      onClick={onExporter}
                      className="flex items-center mt-6 gap-6 rounded-full bg-or w-full px-4 py-3 text-white hover:brightness-110 transition shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]"
                    >
                        <CalendarArrowDown />
                        <span className="flex flex-col items-start">
                            <span>Exporter</span>
                            <span className="text-xs">vers Google Calendar</span>
                        </span>
                    </button>
                </div>

                {/* Bouton importer vers Google Calendar */}
                <div>
                    <button
                      onClick={onImporter}
                      className="flex items-center mt-3 gap-6 rounded-full bg-or w-full px-4 py-3 text-white hover:brightness-110 transition shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]"
                    >
                        <CalendarArrowUp />
                        <span className="flex flex-col items-start">
                            <span>Importer</span>
                            <span className="text-xs">vers le Planning</span>
                        </span>
                    </button>
                </div>

                {/* Bouton supprimer les créneaux exportés */}
                <div>
                    <button
                      onClick={supprimerDeGoogle}
                      className="flex items-center mt-3 gap-6 rounded-full bg-red-900 w-full px-4 py-3 text-white hover:brightness-110 transition shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]"
                    >
                        <CalendarArrowDown />
                        <span className="flex flex-col items-start">
                            <span>Supprimer</span>
                            <span className="text-xs">les créneaux exportés</span>
                        </span>
                    </button>
                </div>

            </div>
            <PopupRejoindreClasse
              ouvert={popupRejoindreOuverte}
              onFermer={() => setPopupRejoindreOuverte(false)}
              onRejoint={onRejoint}
            />
        </aside>
    )
}

export default BarreLateraleEleve
