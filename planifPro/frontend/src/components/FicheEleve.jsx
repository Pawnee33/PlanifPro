import { useState, useEffect } from 'react'
import { api } from '../services/helper'
import PopupAjouterObjectif from './PopupAjouterObjectif'
import PopupModifierObjectif from './PopupModifierObjectif'

function FicheEleve({ eleve }) {
  const [creneaux, setCreneaux] = useState([])
  const [objectifs, setObjectifs] = useState([])
  const [creneauObjectif, setCreneauObjectif] = useState(null)
  const [objectifAModifier, setObjectifAModifier] = useState(null)

  const chargerObjectifs = () => {
    api.get(`/objectifs/eleve/${eleve.utilisateur_id}`)
      .then(setObjectifs)
      .catch(() => setObjectifs([]))
  }

  useEffect(() => {
    api.get('/plannings/global')
      .then((tous) => setCreneaux(tous.filter((c) => c.eleve_id === eleve.utilisateur_id)))
      .catch(() => setCreneaux([]))
    chargerObjectifs()
  }, [eleve.utilisateur_id])

  const ajouterObjectif = (contenu, conseils) => {
    api.post('/objectifs/', {
      eleve_id: eleve.utilisateur_id,
      creneau_id: creneauObjectif.id,
      contenu,
      conseils,
    })
      .then(() => {
        chargerObjectifs()
        setCreneauObjectif(null)
      })
      .catch(() => alert("Erreur lors de l'ajout de l'objectif"))
  }

  const modifierObjectif = (objectifId, contenu, conseils) => {
    api.put(`/objectifs/${objectifId}`, { contenu, conseils })
      .then(() => {
        chargerObjectifs()
        setObjectifAModifier(null)
      })
      .catch(() => alert("Erreur lors de la modification"))
  }

  const supprimerObjectif = (objectifId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer cet objectif ?')) return
    api.delete(`/objectifs/${objectifId}`)
      .then(() => chargerObjectifs())
      .catch(() => alert("Erreur lors de la suppression"))
  }

  const formatDate = (iso) => {
    const [annee, mois, jour] = iso.split('-')
    return `${jour}/${mois}/${annee}`
  }

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
              <div key={creneau.id} className="bg-bleu-marine border-2 border-tracer-violet rounded-xl px-4 py-2 text-white flex items-center justify-between">
                <span>
                  <span className="capitalize">{creneau.jour}</span>{' '}
                  {creneau.heure_debut?.slice(0, 5)} - {creneau.heure_fin?.slice(0, 5)}
                </span>
                <button
                  onClick={() => setCreneauObjectif(creneau)}
                  className="rounded-[16px] bg-or border-2 border-or-tres-clair px-3 py-1 text-sm border border-tracer-violet hover:scale-105"
                >
                  + Objectif
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
      {/* Objectifs de l'élève */}
      <div className="bg-bleu-nuit border-3 border-or rounded-2xl p-5">
        <h3 className="text-or text-lg mb-3">Objectifs</h3>
        {objectifs.length === 0 ? (
          <p className="text-white/70 text-sm">Aucun objectif pour cet élève.</p>
        ) : (
          <div className="flex flex-col gap-2">
            {objectifs.map((objectif) => (
              <div key={objectif.id} className="bg-bleu-marine border-2 border-tracer-violet rounded-xl px-4 py-3 text-white">
                {objectif.date_cours && (
                  <p className="text-or text-sm mb-1">Cours du {formatDate(objectif.date_cours)}</p>
                )}
                <p>{objectif.contenu}</p>
                {objectif.conseils && (
                  <p className="text-white/70 text-sm mt-1">Conseils : {objectif.conseils}</p>
                )}
                <div className="flex gap-3 mt-3">
                  <button
                    onClick={() => setObjectifAModifier(objectif)}
                    className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white text-sm hover:scale-105 transition"
                  >
                    Modifier
                  </button>
                  <button
                    onClick={() => supprimerObjectif(objectif.id)}
                    className="rounded-full bg-[#5C1A1A] px-4 py-2 border-2 border-or-tres-clair text-or text-sm font-semibold hover:scale-105 transition"
                  >
                    Supprimer
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {objectifAModifier && (
        <PopupModifierObjectif
          ouvert={true}
          onFermer={() => setObjectifAModifier(null)}
          objectif={objectifAModifier}
          onModifier={modifierObjectif}
        />
      )}

      {creneauObjectif && (
        <PopupAjouterObjectif
          ouvert={true}
          onFermer={() => setCreneauObjectif(null)}
          onAjouter={ajouterObjectif}
        />
      )}
    </div>
  )
}

export default FicheEleve
