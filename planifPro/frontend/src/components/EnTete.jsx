import React from 'react'
import { useState, useEffect } from 'react'
import { api } from '../services/helper'
import { Bell, Menu } from 'lucide-react'
import logo from '../assets/logo.png'

const EnTete = () => {
    const [utilisateur, setUtilisateur] = useState(null)

    useEffect(() => {
        api.get('/utilisateurs/profil')
            .then(setUtilisateur)
            .catch(() => {})
        }, [])
    return (
        <header className='flex items-center justify-between bg-bleu-roi border-b-[4px] border-tracer-violet px-6 py-3'>
            <div className="flex items-center gap-3">
                <img src={logo} alt="Logo PlanifPro" className="h-12 w-auto mb-3 hover:scale-105" />
                <span className="text-white font-logo text-2xl md:text-4xl">PlanifPro</span>
            </div>

            <div className="flex items-center gap-7">
                <div className='flex items-center gap-2 bg-bleu-nuit rounded-[10px] border border-tracer-violet px-3 py-1'>
                    <button className="bg-blanc-base rounded-[30px] p-1 hover:scale-105">
                        <Bell className="text-bleu-nuit" fill="currentColor" size={18}/>
                    </button>
                    <span className="text-white">0</span>
                </div>

                <span className="text-white hidden md:inline">Bonjour {utilisateur?.prenom}</span>

                <div>
                    <button className="bg-or rounded-[30px] p-2 hover:scale-105">
                        <Menu className="text-white" size={18}/>
                    </button>
                </div>
            </div>
        </header>
    )
}

export default EnTete
