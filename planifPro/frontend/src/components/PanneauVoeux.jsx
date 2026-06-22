import { useState, useEffect } from 'react'
import { api } from '../services/helper'
import CarteStat from './ui/CarteStat'

function PanneauVoeux({ eleves, classe }) {
  const [voeux, setVoeux] = useState([])

  // Recharge les voeux quand on change de classe
  useEffect(() => {
    api
      .get(`/voeux/statut/${classe.id}`)
      .then(setVoeux)
      .catch(() => setVoeux([]))
  }, [classe.id])

  // --- Helpers d'affichage ---
  const joursAbrege = {
    lundi: 'Lun', mardi: 'Mar', mercredi: 'Mer', jeudi: 'Jeu',
    vendredi: 'Ven', samedi: 'Sam', dimanche: 'Dim',
  }

  const formatCreneaux = (creneaux) => {
    return Object.values(creneaux)
      .map((creneau) => `${joursAbrege[creneau.jour]} ${creneau.heure.replace(':', 'h')}`)
      .join(' - ')
  }

  const voeuDeleve = (eleveID) => voeux.find((v) => v.eleve_id === eleveID)

  const nombreSoumis = voeux.length

  const nombreAttente = eleves.length - voeux.length

  const tousSoumis = eleves.length > 0 && nombreAttente === 0

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap gap-8">
        <CarteStat titre="Voeux soumis" valeur={nombreSoumis} />
        <CarteStat titre="En attente" valeur={nombreAttente} />
        <CarteStat titre="Total élèves" valeur={eleves.length} />
      </div>
    </div>
  )
}

export default PanneauVoeux
