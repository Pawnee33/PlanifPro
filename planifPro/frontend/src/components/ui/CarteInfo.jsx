function CarteInfo({ titre, children }) {
  return (
    <div className="flex-1 min-w-[180px] bg-bleu-nuit border-2 border-or rounded-2xl p-4 text-center">
      <p className="text-or uppercase text-sm mb-1">{titre}</p>
      <div className="text-white text-sm">{children}</div>
    </div>
  )
}

export default CarteInfo
