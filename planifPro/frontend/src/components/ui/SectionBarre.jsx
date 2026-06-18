import { useState } from 'react'
import { ChevronUp, ChevronDown } from 'lucide-react'

function SectionBarre({ icone, titre, messageVide, libelleBouton }) {
  const [ouvert, setOuvert] = useState(false)   // chaque section gère SON propre état

  return (
    <div>
      <button
        onClick={() => setOuvert(!ouvert)}
        className={`flex items-center justify-between rounded-[16px] w-full px-4 py-3 text-white hover:brightness-110 transition shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)] ${ouvert ? 'bg-or' : 'bg-bleu-nuit'}`}
      >
        <span className="flex items-center gap-6">
          {icone}
          {titre}
        </span>
        {ouvert ? <ChevronUp /> : <ChevronDown />}
      </button>

      {ouvert && (
        <div className="flex flex-col gap-2 bg-bleu-shadow rounded-[16px] p-3 mt-2">
          <p className="text-white/70 text-sm text-center">{messageVide}</p>
          <button className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet hover:scale-105 text-white">
            {libelleBouton}
          </button>
        </div>
      )}
    </div>
  )
}

export default SectionBarre
