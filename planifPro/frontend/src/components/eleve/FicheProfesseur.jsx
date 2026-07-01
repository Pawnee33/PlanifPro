import { GraduationCap } from 'lucide-react'

function FicheProfesseur({ professeur }) {
  const nomComplet = `${professeur.prenom} ${professeur.nom}`

  return (
    <div className="bg-bleu-nuit border-2 border-or rounded-2xl p-6 max-w-3xl">
      {/* En-tête : logo + nom */}
      <div className="flex items-center gap-3 mb-4">
        <div className="rounded-full bg-or w-12 h-12 flex items-center justify-center shrink-0">
          <GraduationCap className="text-white" />
        </div>
        <h2 className="text-white text-2xl">{nomComplet}</h2>
      </div>

      {/* Infos dans une carte imbriquée */}
      <div className="bg-bleu-marine border-2 border-tracer-violet rounded-xl p-4 flex flex-col gap-3">
        <div>
          <p className="text-white/70 text-sm mb-1">Email</p>
          <p className="text-white">{professeur.email}</p>
        </div>

        {professeur.classe_nom && (
          <>
            <div>
              <p className="text-white/70 text-sm mb-1">Classe</p>
              <p className="text-white">{professeur.classe_nom}</p>
            </div>
            <div>
              <p className="text-white/70 text-sm mb-1">Code de la classe</p>
              <p className="text-white">{professeur.code_classe}</p>
            </div>
          </>
        )}
      </div>
    </div>
  )
}

export default FicheProfesseur
