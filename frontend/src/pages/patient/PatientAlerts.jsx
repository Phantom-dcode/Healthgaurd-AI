import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Bell, CheckCircle, Eye } from 'lucide-react'
import Layout from '../../components/layout/Layout'
import Badge from '../../components/ui/Badge'
import Spinner from '../../components/ui/Spinner'
import { listAlerts, updateAlert } from '../../api/alerts'
import { fmtDateTime } from '../../utils/helpers'
import toast from 'react-hot-toast'

export default function PatientAlerts() {
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(true)

  const load = () => listAlerts({ limit:50 }).then(r => setAlerts(r.data?.data || [])).finally(() => setLoading(false))
  useEffect(() => { load() }, [])

  const markRead = async id => {
    await updateAlert(id, { is_read: true })
    setAlerts(prev => prev.map(a => a.alert_id === id ? { ...a, is_read: true } : a))
    toast.success('Marked as read')
  }
  const resolve = async id => {
    await updateAlert(id, { is_resolved: true, is_read: true })
    setAlerts(prev => prev.map(a => a.alert_id === id ? { ...a, is_resolved: true, is_read: true } : a))
    toast.success('Alert resolved')
  }

  return (
    <Layout title="My Alerts">
      <div className="space-y-3">
        {loading ? <div className="flex justify-center py-20"><Spinner size="lg" /></div>
        : alerts.length === 0 ? (
          <div className="card text-center py-16">
            <Bell className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <p className="text-slate-400">No alerts yet. Keep monitoring your health!</p>
          </div>
        ) : alerts.map((a, i) => (
          <motion.div key={a.alert_id} initial={{opacity:0,y:10}} animate={{opacity:1,y:0}}
            transition={{delay:i*0.04}}
            className={`card-sm flex items-start gap-4 ${!a.is_read ? 'border-l-2 border-l-sky-500' : ''} ${a.is_resolved ? 'opacity-50' : ''}`}>
            <Badge severity={a.severity} />
            <div className="flex-1 min-w-0">
              <p className="text-sm text-slate-200">{a.message}</p>
              <p className="text-xs text-slate-500 mt-1">{fmtDateTime(a.created_at)}</p>
            </div>
            <div className="flex gap-2 shrink-0">
              {!a.is_read && <button onClick={() => markRead(a.alert_id)}
                className="p-1.5 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-sky-400 transition-colors" title="Mark read">
                <Eye className="w-4 h-4" />
              </button>}
              {!a.is_resolved && <button onClick={() => resolve(a.alert_id)}
                className="p-1.5 rounded-lg hover:bg-slate-700 text-slate-400 hover:text-emerald-400 transition-colors" title="Resolve">
                <CheckCircle className="w-4 h-4" />
              </button>}
            </div>
          </motion.div>
        ))}
      </div>
    </Layout>
  )
}
