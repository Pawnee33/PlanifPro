import { useState, useEffect } from 'react'
import { api } from '../services/helper'

function FicheEleve({ eleve }) {
  const [creneaux, setCreneaux] = useState([])

  useEffect(() => {
    api.get('/plannings/global')
      .then((tous) => setCreneaux(tous.filter((c) => c.eleve_id === eleve.utilisateur_id)))
      .catch(() => setCreneaux([]))
  }, [eleve.utilisateur_id])

  return (
    <div className="flex flex-col gap-4 max-w-4xl mx-auto">
      {/* Carte identité */}
      <div className="bg-bleu-nuit border-3 border-or rounded-2xl p-5 flex items-center gap-4">
        <div
          style={{ backgroundColor: eleve.classe_couleur || '#D59813' }}
          className="rounded-full w-14 h-14 flex items-center justify-center text-white text-xl font-bold"
        >
          {eleve.prenom?.[0]}{eleve.nom?.[0]}
        </div>
        <div>
          <h2 className="text-2xl text-white font-titre">{eleve.prenom} {eleve.nom}</h2>
          <p className="text-white/80 text-sm">Classe : {eleve.classe_nom}</p>
          <p className="text-white/80 text-sm">
            Durée : {eleve.duree_minutes ? `${eleve.duree_minutes} min` : 'non configurée'}
          </p>
        </div>
      </div>

      {/* Créneaux de l'élève */}
      <div className="bg-bleu-nuit border-3 border-or rounded-2xl p-5">
        <h3 className="text-or text-lg mb-3">Créneaux</h3>
        {creneaux.length === 0 ? (
          <p className="text-white/70 text-sm">Aucun créneau pour cet élève.</p>
        ) : (
          <div className="flex flex-col gap-2">
            {creneaux.map((creneau) => (
              <div key={creneau.id} className="bg-bleu-marine rounded-xl px-4 py-2 text-white">
                <span className="capitalize">{creneau.jour}</span>{' '}
                {creneau.heure_debut?.slice(0, 5)} - {creneau.heure_fin?.slice(0, 5)}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default FicheEleve
