function PopupCreerClasse({ ouvert, onFermer}) {
    if(!ouvert) return null //si c'est fermé on n'affiche rien

    return (
        <div
            onClick={onFermer}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
        >
            <div
                onClick={(erreur) => erreur.stopPropagation()}
                className="bg-bleu-marine border-2 border-tracer-violet rounded-2xl p-6 w-full max-w-md"
            >
                <h2 className="text-2xl text-or font-titre mb-4">Créer une classe</h2>
                {/* les champs viendront ici à l'étape 2 */}
                <button
                    onClick={onFermer}
                    className="rounded-[16px] bg-bleu-roi px-4 py-2 border border-tracer-violet text-white"
                >
                    Fermer
                </button>
            </div>
        </div>
    )
}

export default PopupCreerClasse
