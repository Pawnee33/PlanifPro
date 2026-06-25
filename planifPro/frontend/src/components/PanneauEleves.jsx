import { useState } from 'react'
import { api } from '../services/helper'
import PopupConfigurerDuree from './PopupConfigurerDuree'
import { Pencil } from 'lucide-react'

function PanneauEleves({ eleves, classe, onElevesModifies }) {
  const [eleveAModifier, setEleveAModifier] = useState(null)

  const formatDuree = (minutes) => {
    if (minutes === 60) return '1 heure'
    if (minutes % 60 === 0) return `${minutes / 60} heures`
    return `${minutes} min`
  }

  const configurerDuree = (eleveId, duree) => {
    api.put(`/eleves/${eleveId}`, {
      classe_id: classe.id,
      duree_minutes: duree,
    })
      .then(() => onElevesModifies())
      .catch(() => alert('Erreur lors de la modification de la durée'))
  }

  const lancerCollecte = async () => {
    try {
      await api.post(`/classes/${classe.id}/collecte`)
      alert('Collecte des vœux lancée !')
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="flex flex-col gap-3">
      {eleves.length === 0 ? (
        <p className="text-white/70">Aucun élève n'a encore rejoint cette classe.</p>
      ) : (
        eleves.map((eleve) => (
          <div
            key={eleve.id}
            className="bg-bleu-nuit rounded-2xl border-2 border-or p-4 flex items-center justify-between gap-4"
          >
            <div className="flex items-center gap-3">
              <div className="rounded-full bg-or w-10 h-10 flex items-center justify-center text-white font-bold">
                {eleve.prenom?.[0]}{eleve.nom?.[0]}
              </div>
              <div>
                <p className="text-or text-lg">{eleve.prenom} {eleve.nom}</p>
                <p className="text-white/70 text-sm">
                  Durée : {eleve.duree_minutes ? formatDuree(eleve.duree_minutes) : 'non configurée'}
                </p>
              </div>
            </div>
            <button
              onClick={() => setEleveAModifier(eleve)}
              className="flex items-center gap-2 rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105 transition"
            >
              <Pencil size={16} /> {eleve.duree_minutes ? 'Modifier' : 'Configurer'}
            </button>
          </div>
        ))
      )}

      <div className="bg-linear-to-br from-gray-500/70 to-gray-400/50 border-2 border-dashed border-or rounded-3xl p-6 text-center mt-2">
        <p className="text-or text-lg mb-1">Prêt à lancer la collecte des vœux ?</p>
        <p className="text-white/70 text-sm mb-3">{eleves.length} élève(s) dans la classe</p>
        <button
          onClick={lancerCollecte}
          className="bg-linear-to-b from-or-clair to-or border-3 border-or-tres-clair rounded-full px-6 py-2 text-white hover:scale-105 transition"
        >
          Lancer la collecte des vœux
        </button>
      </div>
      {eleveAModifier && (
        <PopupConfigurerDuree
          ouvert={true}
          onFermer={() => setEleveAModifier(null)}
          eleve={eleveAModifier}
          onConfigurer={(eleveId, duree) => {
            configurerDuree(eleveId, duree)
            setEleveAModifier(null)
          }}
        />
      )}
    </div>
  )
}

export default PanneauEleves
