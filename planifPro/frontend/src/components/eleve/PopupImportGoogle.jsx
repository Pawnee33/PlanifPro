import { useState } from 'react'

function PopupImportGoogle({ onFermer, onImporter }) {
  const [dateDebut, setDateDebut] = useState('')
  const [dateFin, setDateFin] = useState('')

  const lancerImport = () => {
    // Transmet les dates (peuvent être vides = pas de borne)
    onImporter(dateDebut, dateFin)
    onFermer()
  }

  return (
    <div
      onClick={onFermer}
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        onClick={(evenement) => evenement.stopPropagation()}
        className="bg-bleu-nuit border-2 border-or rounded-2xl p-6 max-w-md w-full mx-4"
      >
        <h2 className="text-or text-2xl mb-4">Importer depuis Google Calendar</h2>

        <div className="flex flex-col gap-4">
          <div>
            <label className="text-white/70 text-sm mb-1 block">Du</label>
            <input
              type="date"
              value={dateDebut}
              onChange={(evenement) => setDateDebut(evenement.target.value)}
              className="w-full rounded-lg bg-bleu-marine border-2 border-tracer-violet px-3 py-2 text-white"
            />
          </div>

          <div>
            <label className="text-white/70 text-sm mb-1 block">Au</label>
            <input
              type="date"
              value={dateFin}
              onChange={(evenement) => setDateFin(evenement.target.value)}
              className="w-full rounded-lg bg-bleu-marine border-2 border-tracer-violet px-3 py-2 text-white"
            />
          </div>
        </div>

        <div className="flex gap-3 mt-6">
          <button
            onClick={lancerImport}
            className="flex-1 rounded-full bg-or px-5 py-2 text-white hover:brightness-110 transition"
          >
            Importer
          </button>
          <button
            onClick={onFermer}
            className="rounded-full bg-bleu-roi px-5 py-2 border border-tracer-violet text-white hover:brightness-110 transition"
          >
            Annuler
          </button>
        </div>
      </div>
    </div>
  )
}

export default PopupImportGoogle
