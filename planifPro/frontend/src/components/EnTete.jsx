import React from 'react'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { api } from '../services/helper'
import { Bell, Menu } from 'lucide-react'
import logo from '../assets/logo.png'
import MenuBurger from './MenuBurger'
import PanneauNotifications from './PanneauNotifications'

const EnTete = ({ onAccueil }) => {
    const [utilisateur, setUtilisateur] = useState(null)
    const [menuOuvert, setMenuOuvert] = useState(false)
    const [notifications, setNotifications] = useState([])
    const [notifsOuvertes, setNotifsOuvertes] = useState(false)

    useEffect(() => {
        api.get('/utilisateurs/profil')
            .then(setUtilisateur)
            .catch(() => {})
        api.get('/notifications/')
            .then(setNotifications)
            .catch(() => setNotifications([]))
        }, [])

    const toutMarquerLu = () => {
        api.put('/notifications/lire')
            .then(() => {
                // on remet tout en "lu" localement
                setNotifications((prev) => prev.map((n) => ({ ...n, lu: true })))
            })
            .catch(() => alert('Erreur'))
    }

    return (
        <header className='flex items-center justify-between bg-bleu-roi border-b-[4px] border-tracer-violet px-6 py-3'>
            <div className="flex items-center gap-3">
                <button onClick={onAccueil} className="flex items-center gap-3">
                  <img src={logo} alt="Logo PlanifPro" className="h-12 w-auto mb-3 hover:scale-105" />
                  <span className="text-white font-logo text-2xl md:text-4xl">PlanifPro</span>
                </button>
            </div>

            <div className="flex items-center gap-7">
                <div className='flex items-center gap-2 bg-bleu-nuit rounded-[10px] border border-tracer-violet px-3 py-1'>
                    <button
                      onClick={() => setNotifsOuvertes(true)}
                      className="bg-blanc-base rounded-[30px] p-1 hover:scale-105">
                        <Bell className="text-bleu-nuit" fill="currentColor" size={18}/>
                    </button>
                    <span className="text-white">{notifications.filter((n) => !n.lu).length}</span>
                </div>

                <span className="text-white hidden md:inline">Bonjour {utilisateur?.prenom}</span>

                <div>
                    <button  
                      onClick={() => setMenuOuvert(true)}
                      className="bg-or rounded-[30px] p-2 hover:scale-105">
                        <Menu className="text-white" size={18}/>
                    </button>
                </div>
            </div>
            <MenuBurger
                ouvert={menuOuvert}
                onFermer={() => setMenuOuvert(false)}
                utilisateur={utilisateur}
                onOuvrirNotifications={() => {
                  setMenuOuvert(false)
                  setNotifsOuvertes(true)
                }}
            />

            <PanneauNotifications
                ouvert={notifsOuvertes}
                onFermer={() => setNotifsOuvertes(false)}
                notifications={notifications}
                onToutMarquerLu={toutMarquerLu}
            />
        </header>
    )
}

export default EnTete
