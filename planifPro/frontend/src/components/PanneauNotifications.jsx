import { X } from 'lucide-react'

function PanneauNotifications({ ouvert, onFermer, notifications, onToutMarquerLu }) {
  if (!ouvert) return null

  return (
    <div onClick={onFermer} className="fixed inset-0 bg-black/50 flex items-start justify-end z-50">
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-bleu-clair border-2 border-tracer-violet rounded-2xl w-full max-w-sm mt-20 mr-6 max-h-[70vh] overflow-y-auto"
      >
        <div className="relative bg-bleu-nuit px-5 py-4 flex items-center justify-between">
          <h3 className="text-white font-titre text-lg">Notifications</h3>
          <button onClick={onFermer} className="bg-bleu-roi rounded-lg p-1 border border-tracer-violet text-white hover:brightness-110">
            <X size={16} />
          </button>
        </div>

        {notifications.length === 0 ? (
          <p className="text-white/70 text-sm px-5 py-6 text-center">Aucune notification.</p>
        ) : (
          <div className="flex flex-col">
            {notifications.map((notif) => (
              <div
                key={notif.id}
                className={`px-5 py-3 border-t border-tracer-violet/40 ${notif.lu ? 'opacity-60' : ''}`}
              >
                <p className="text-white font-bold text-sm">{notif.titre}</p>
                <p className="text-white/80 text-sm">{notif.message}</p>
              </div>
            ))}
          </div>
        )}

        {notifications.some((n) => !n.lu) && (
          <button
            onClick={onToutMarquerLu}
            className="w-full px-5 py-3 text-or hover:bg-bleu-roi/40 border-t border-tracer-violet/40 text-sm"
          >
            Tout marquer comme lu
          </button>
        )}
      </div>
    </div>
  )
}

export default PanneauNotifications
