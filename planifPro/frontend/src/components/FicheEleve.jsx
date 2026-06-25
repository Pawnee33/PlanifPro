function FicheEleve({ eleve }) {
  return (
    <div className="flex flex-col gap-4 max-w-4xl mx-auto">
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
    </div>
  )
}

export default FicheEleve
