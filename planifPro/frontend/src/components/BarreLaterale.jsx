import React from 'react'
import { useState } from 'react'
import { Users, CalendarDays, CalendarArrowDown, CalendarArrowUp, GraduationCap, Star, ChevronDown, ChevronUp } from 'lucide-react'
import logo from '../assets/logo.png'

const BarreLaterale = () => {
    const [classesOuvert, setClassesOuvert] = useState(false)
    const [elevesOuvert, setElevesOuvert] = useState(false)
    const [evenementsOuvert, setEvenementsOuvert] = useState(false)
    return (
        <aside className='w-64 flex flex-col gap-3 bg-bleu-marine border-r-[4px] border-tracer-violet p-4'>

            <div className="flex flex-col gap-5">

            {/* Bouton Planning */}
            <div>
                <button className='flex items-center gap-6 rounded-[16px] bg-or w-full px-4 py-3 text-white hover:brightness-110 transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]'>
                    <CalendarDays />
                    Planning
                </button>
            </div>

                {/* Bouton Mes classes */}
                <div>
                    <button
                        onClick={() => setClassesOuvert(!classesOuvert)} 
                        className='flex items-center justify-between rounded-[16px] bg-bleu-nuit w-full px-4 py-3 text-white hover:brightness-110 transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]'>
                            <span className="flex items-center gap-6">
                                <Users fill="currentColor"/>
                                Mes classes
                            </span>
                            {classesOuvert ? <ChevronUp /> : <ChevronDown />}
                    </button>
                    {classesOuvert && (
                        <div className="flex flex-col gap-2 bg-bleu-shadow rounded-[16px] p-3 mt-2">
                            <p className="text-white/70 text-sm text-center">Aucune classe pour le moment</p>
                            <button className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet hover:scale-105 text-white">
                                + Créer une classe
                            </button>
                        </div>
                    )}
                </div>

                {/* Bouton Mes élèves */}
                <div>
                    <button
                        onClick={() => setElevesOuvert(!elevesOuvert)}
                        className='flex items-center justify-between rounded-[16px] bg-bleu-nuit w-full px-4 py-3 text-white hover:brightness-110 transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]'>
                            <span className="flex items-center gap-6">
                                <GraduationCap />
                                Mes élèves
                            </span>
                            {elevesOuvert ? <ChevronUp /> : <ChevronDown />}
                    </button>
                    {elevesOuvert && (
                        <div className="flex flex-col gap-2 bg-bleu-shadow rounded-[16px] p-3 mt-2">
                            <p className="text-white/70 text-sm text-center">Aucun élève pour le moment</p>
                            <button className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet hover:scale-105 text-white">
                                + Inviter un élève
                            </button>
                        </div>
                    )}
                </div>

                {/* Bouton Événements */}
                <div>
                    <button
                    onClick={() => setEvenementsOuvert(!evenementsOuvert)}
                        className='flex items-center justify-between rounded-[16px] bg-bleu-nuit w-full px-4 py-3 text-white hover:brightness-110 transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]'>
                            <span className="flex items-center gap-6">
                                <Star />
                                Événements
                            </span>
                            {evenementsOuvert ? <ChevronUp /> : <ChevronDown />}
                    </button>
                    {evenementsOuvert && (
                        <div className="flex flex-col gap-2 bg-bleu-shadow rounded-[16px] p-3 mt-2">
                            <p className="text-white/70 text-sm text-center">Aucun événement pour le moment</p>
                            <button className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet hover:scale-105 text-white">
                                + Ajouter un événement
                            </button>
                        </div>
                    )}
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
