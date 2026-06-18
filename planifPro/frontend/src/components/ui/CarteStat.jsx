function CarteStat({ titre, valeur }) {
  return (
    <div className="w-full md:w-56 h-30 bg-bleu-nuit rounded-2xl m-6 p-6 px-6 shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)] border border-tracer-violet">
      <p className="text-4xl text-or font-base">{valeur}</p>   {/* le chiffre, gros et doré */}
      <p className="text-white font-base">{titre}</p>    {/* le libellé, blanc */}
    </div>
  )
}

export default CarteStat
