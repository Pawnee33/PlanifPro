import { useState } from 'react'
import PopupMonProfil from './PopupMonProfil'
import { api } from '../services/helper'
import { User, Settings, Bell, Calendar, HelpCircle, LogOut, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

function MenuBurger({ ouvert, onFermer, utilisateur, onOuvrirNotifications }) {
  const navigate = useNavigate()
  const [profilOuvert, setProfilOuvert] = useState(false)

  if (!ouvert) return null

  const seDeconnecter = () => {
    // On demande au serveur d'effacer le cookie httpOnly (le front ne peut pas le faire lui-même)
    api.post('/authentification/deconnexion')
      .finally(() => navigate('/connexion'))
  }

  // initiales pour l'avatar
  const initiales = `${utilisateur?.prenom?.[0] || ''}${utilisateur?.nom?.[0] || ''}`

  // une ligne du menu
  const ligne = (icone, libelle, onClick) => (
    <button
      onClick={onClick}
      className="flex items-center gap-3 w-full px-5 py-4 text-white hover:bg-bleu-roi/50 transition border-t border-tracer-violet/40"
    >
      {icone}
      <span>{libelle}</span>
    </button>
  )

  return (
    <>
    <div onClick={onFermer} className="fixed inset-0 bg-black/50 flex items-start justify-end z-50">
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-bleu-clair border-2 border-tracer-violet rounded-2xl w-full max-w-xs mt-20 mr-6 overflow-y-auto max-h-[calc(100vh-6rem)]"
      >
        {/* En-tête : avatar + nom + rôle */}
        <div className="relative bg-bleu-nuit px-5 py-4 flex items-center gap-3">
          <div className="bg-or rounded-full w-12 h-12 flex items-center justify-center text-white text-lg font-bold">
            {initiales}
          </div>
          <div>
            <p className="text-white font-bold">{utilisateur?.prenom} {utilisateur?.nom}</p>
            <p className="text-white/70 text-sm capitalize">{utilisateur?.role}</p>
          </div>
          <button onClick={onFermer} className="absolute top-3 right-3 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110">
            <X size={16} />
          </button>
        </div>

        {/* Entrées */}
        {ligne(<User className="text-or" size={20} />, 'Mon Profil', () => setProfilOuvert(true))}
        {ligne(<Settings className="text-white" size={20} />, 'Paramètres', () => alert('Paramètres — à venir'))}
        {ligne(<Bell className="text-or" size={20} />, 'Notifications', onOuvrirNotifications)}
        {ligne(<Calendar className="text-white" size={20} />, 'Exporter vers Google Calendar', () => alert('Export — à venir'))}
        {ligne(<HelpCircle className="text-or" size={20} />, 'Aide', () => alert('Aide — à venir'))}
        {ligne(<LogOut className="text-white" size={20} />, 'Se déconnecter', seDeconnecter)}
      </div>
    </div>
      {profilOuvert && <PopupMonProfil onFermer={() => setProfilOuvert(false)} />}
    </>
  )
}

export default MenuBurger
