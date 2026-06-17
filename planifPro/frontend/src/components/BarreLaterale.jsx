import React from 'react'
import { Users, CalendarDays, GraduationCap, Star, ChevronDown, ChevronUp } from 'lucide-react'
import logo from '../assets/logo.png'

const BarreLaterale = () => {
    return (
        <aside className='w-64 flex flex-col gap-3 bg-bleu-marine border-r-[4px] border-tracer-violet p-4'>
            <div className="flex flex-col gap-5">
                <button className='flex items-center gap-6 rounded-[16px] bg-or w-full px-4 py-3 text-white hover:brightness-110 transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]'>
                    <CalendarDays />
                    Planning
                </button>
                <button className='flex items-center gap-6 rounded-[16px] bg-bleu-nuit w-full px-4 py-3 text-white hover:brightness-110 transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]'>
                    <Users fill="currentColor"/>
                    Mes classes
                    <ChevronUp />
                </button>
                <button className='flex items-center gap-6 rounded-[16px] bg-bleu-nuit w-full px-4 py-3 text-white hover:brightness-110 transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]'>
                    <GraduationCap />
                    Mes élèves
                    <ChevronUp />
                </button>
                <button className='flex items-center gap-6 rounded-[16px] bg-bleu-nuit w-full px-4 py-3 text-white hover:brightness-110 transition backdrop-blur-sm shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)]'>
                    <Star />
                    Événements
                    <ChevronUp />
                </button>
            </div>

            <div>
                <div>
                </div>

                <div>
                </div>
            </div>
        </aside>
    )
}

export default BarreLaterale
