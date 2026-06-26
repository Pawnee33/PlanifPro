import { useState, useEffect } from 'react'
import { X } from 'lucide-react'
import { api } from '../services/helper'

function PopupAjouterCours({ ouvert, onFermer, classes, dateInitiale, heureInitiale, onCreer }) {
  const [classeId, setClasseId] = useState('')
  const [eleveId, setEleveId] = useState('')
  const [elevesDeLaClasse, setElevesDeLaClasse] = useState([])
  const [heureDebut, setHeureDebut] = useState(heureInitiale || '')
  const [heureFin, setHeureFin] = useState('')
  const [scope, setScope] = useState('toute_la_periode')

  // Quand la classe change, on charge ses élèves
  useEffect(() => {
    if (!classeId) {
      setElevesDeLaClasse([])
      return
    }
    api.get(`/classes/${classeId}/eleves`)
      .then(setElevesDeLaClasse)
      .catch(() => setElevesDeLaClasse([]))
  }, [classeId])

  if (!ouvert) return null

  const valider = () => {
    if (!classeId || !eleveId || !heureDebut || !heureFin) {
      alert('Veuillez choisir une classe, un élève et les heures')
      return
    }
    onCreer({
      classeId,
      eleveId,
      heureDebut,
      heureFin,
      scope,
      date: dateInitiale,
    })
  }

  return (
    <div onClick={onFermer} className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div onClick={(e) => e.stopPropagation()} className="relative bg-bleu-clair border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <button onClick={onFermer} className="absolute top-4 right-4 bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110 transition">
          <X size={18} />
        </button>

        <h3 className="text-white text-xl font-titre mb-4">Ajouter un cours</h3>

        <label className="block text-white mb-1">Classe</label>
        <select
          value={classeId}
          onChange={(e) => { setClasseId(e.target.value); setEleveId('') }}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        >
          <option value="">— Choisir une classe —</option>
          {classes.map((classe) => (
            <option key={classe.id} value={classe.id}>{classe.nom}</option>
          ))}
        </select>

        <label className="block text-white mb-1">Élève</label>
        <select
          value={eleveId}
          onChange={(e) => setEleveId(e.target.value)}
          className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet mb-4"
        >
          <option value="">— Choisir un élève —</option>
          {elevesDeLaClasse.map((eleve) => (
            <option key={eleve.utilisateur_id} value={eleve.utilisateur_id}>
              {eleve.prenom} {eleve.nom}
            </option>
          ))}
        </select>

        <div className="flex gap-3 mb-4">
          <div className="flex-1">
            <label className="block text-white mb-1 text-sm">Heure de début</label>
            <input type="time" value={heureDebut} onChange={(e) => setHeureDebut(e.target.value)}
              className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet" />
          </div>
          <div className="flex-1">
            <label className="block text-white mb-1 text-sm">Heure de fin</label>
            <input type="time" value={heureFin} onChange={(e) => setHeureFin(e.target.value)}
              className="w-full bg-bleu-nuit rounded-lg px-3 py-2 text-white border border-tracer-violet" />
          </div>
        </div>

        <p className="text-white mb-2">Appliquer à :</p>
        <div className="flex flex-col gap-2 mb-4">
          <label className="flex items-center gap-2 text-white">
            <input type="radio" checked={scope === 'ce_jour'} onChange={() => setScope('ce_jour')} />
            Ce jour seulement
          </label>
          <label className="flex items-center gap-2 text-white">
            <input type="radio" checked={scope === 'toute_la_periode'} onChange={() => setScope('toute_la_periode')} />
            Toute la période
          </label>
        </div>

        <div className="flex justify-end gap-3">
          <button onClick={onFermer} className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Annuler
          </button>
          <button onClick={valider} className="rounded-[16px] bg-or px-4 py-2 border border-tracer-violet text-white hover:scale-105">
            Ajouter
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupAjouterCours
