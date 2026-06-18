function SectionHoraires({ jour, info, index, onChange }) {
  // Alterne la couleur de fond un sur deux selon la position
  const couleurFond = index % 2 === 0 ? 'bg-or' : 'bg-bleu-roi'

  return (
    <div
      className={`rounded-xl p-3 mb-2 transition ${couleurFond} ${
        info.actif ? '' : 'opacity-50'
      }`}
    >
      <div className="flex items-center gap-3">
        {/* Interrupteur du jour */}
        <button
          type="button"
          onClick={() => onChange('actif', !info.actif)}
          className={`w-10 h-6 rounded-full flex items-center px-1 transition ${
            info.actif ? 'bg-bleu-roi justify-end' : 'bg-gray-400 justify-start'
          }`}
        >
          <span className="w-4 h-4 rounded-full bg-white"></span>
        </button>
        <span className="capitalize text-white">{jour}</span>
      </div>

      {/* Horaires affichés uniquement si le jour est actif */}
      {info.actif && (
        <div className="flex items-center gap-2 mt-2 text-white">
          <span>De</span>
          <input
            type="time"
            value={info.debut}
            onChange={(e) => onChange('debut', e.target.value)}
            className="bg-bleu-nuit rounded px-2 py-1 text-white"
          />
          <span>à</span>
          <input
            type="time"
            value={info.fin}
            onChange={(e) => onChange('fin', e.target.value)}
            className="bg-bleu-nuit rounded px-2 py-1 text-white"
          />
        </div>
      )}
    </div>
  )
}

export default SectionHoraires
