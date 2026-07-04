import { Bell } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import { useEffect, useState } from 'react'
import { alertsSummary } from '../../api/alerts'

export default function Header({ title }) {
  const { user } = useAuth()
  const [unread, setUnread] = useState(0)

  useEffect(() => {
    alertsSummary().then(r => setUnread(r.data?.data?.unread || 0)).catch(()=>{})
  }, [])

  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-20">
      <h1 className="text-lg font-semibold text-slate-100">{title}</h1>
      <div className="flex items-center gap-3">
        <button className="relative p-2 rounded-xl hover:bg-slate-800 transition-colors">
          <Bell className="w-5 h-5 text-slate-400" />
          {unread > 0 && (
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
          )}
        </button>
        <div className="w-8 h-8 bg-sky-500/20 rounded-full flex items-center justify-center">
          <span className="text-sky-400 text-sm font-semibold">{user?.name?.[0]?.toUpperCase()}</span>
        </div>
      </div>
    </header>
  )
}
