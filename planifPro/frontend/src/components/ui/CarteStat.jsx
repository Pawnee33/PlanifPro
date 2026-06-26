function CarteStat({ titre, valeur, vert }) {
  return (
    <div className={`w-full md:w-56 h-30 bg-bleu-nuit rounded-2xl m-6 p-6 px-6 shadow-[0_6px_14px_-4px_rgba(0,0,0,0.5)] border ${vert ? 'border-green-500' : 'border-tracer-violet'}`}>
      <p className={`text-4xl ${vert ? 'text-green-500' : 'text-or'} font-base`}>{valeur}</p>   {/* le chiffre, gros, doré ou vert */}
      <p className="text-white font-base">{titre}</p>    {/* le libellé, blanc */}
    </div>
  )
}

export default CarteStat
