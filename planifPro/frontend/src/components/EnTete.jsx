import React from 'react'
import { Bell, Menu } from 'lucide-react'
import logo from '../assets/logo.png'

const EnTete = () => {
    return (
        <header className='flex items-center justify-between bg-bleu-roi border-b-[4px] border-tracer-violet px-6 py-3'>
            <div className="flex items-center gap-3">
                <img src={logo} alt="Logo PlanifPro" className="h-12 w-auto mb-3" />
                <span className="text-black font-logo text-4xl">PlanifPro</span>
            </div>

            <div className="flex items-center gap-7">
                <div className='flex items-center gap-2 bg-bleu-nuit rounded-[10px] border border-tracer-violet px-3 py-1'>
                    <button className="bg-blanc-base rounded-[30px] p-1">
                        <Bell className="text-bleu-nuit" fill="currentColor" size={18}/>
                    </button>
                    <span className="text-white">0</span>
                </div>

                <span className="text-white">Bonjour Pauline</span>

                <div>
                    <button className="bg-or rounded-[30px] p-2">
                        <Menu className="text-white" size={18}/>
                    </button>
                </div>
            </div>
        </header>
    )
}

export default EnTete
