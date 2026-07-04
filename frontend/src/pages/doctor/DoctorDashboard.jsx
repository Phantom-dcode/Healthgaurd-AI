import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Users, Bell, AlertTriangle, TrendingUp, Activity } from 'lucide-react'
import Layout from '../../components/layout/Layout'
import StatCard from '../../components/ui/StatCard'
import Badge from '../../components/ui/Badge'
import { getMyPatients } from '../../api/doctors'
import { listAlerts, alertsSummary } from '../../api/alerts'
import { fmtDateTime, riskColor } from '../../utils/helpers'
import { useNavigate } from 'react-router-dom'

export default function DoctorDashboard() {
  const [patients, setPatients]   = useState([])
  const [alerts,   setAlerts]     = useState([])
  const [summary,  setSummary]    = useState({})
  const navigate = useNavigate()

  useEffect(() => {
    Promise.allSettled([
      getMyPatients(),
      listAlerts({ limit:10 }),
      alertsSummary(),
    ]).then(([p, a, s]) => {
      if (p.status==='fulfilled') setPatients(p.value.data?.data || [])
      if (a.status==='fulfilled') setAlerts(a.value.data?.data   || [])
      if (s.status==='fulfilled') setSummary(s.value.data?.data  || {})
    })
  }, [])

  return (
    <Layout title="Doctor Dashboard">
      <div className="space-y-6">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard index={0} icon={Users}         label="My Patients"      value={patients.length}         color="text-sky-400" />
          <StatCard index={1} icon={Bell}          label="Unread Alerts"    value={summary.unread  || 0}    color="text-amber-400" />
          <StatCard index={2} icon={AlertTriangle} label="Critical Alerts"  value={summary.critical|| 0}    color="text-red-400" />
          <StatCard index={3} icon={Activity}      label="High Severity"    value={summary.high    || 0}    color="text-orange-400" />
        </div>

        <div className="grid lg:grid-cols-2 gap-4">
          <div className="card">
            <p className="section-title mb-1">My Patients</p>
            <p className="section-sub mb-4">Assigned patients overview</p>
            {patients.length===0 ? <p className="text-slate-500 text-sm py-4 text-center">No patients assigned yet</p>
            : <div className="space-y-2">
              {patients.slice(0,8).map((p,i) => (
                <motion.div key={p.patient_id} initial={{opacity:0,x:-10}} animate={{opacity:1,x:0}} transition={{delay:i*0.05}}
                  onClick={() => navigate(`/doctor/patients/${p.patient_id}`)}
                  className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-800 cursor-pointer transition-colors">
                  <div className="w-8 h-8 bg-sky-500/20 rounded-full flex items-center justify-center text-sky-400 font-semibold text-sm">
                    {p.name?.[0]?.toUpperCase()}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-200">{p.name}</p>
                    <p className="text-xs text-slate-500">{p.email}</p>
                  </div>
                  <span className="ml-auto text-xs text-slate-600">{fmtDateTime(p.assigned_at)}</span>
                </motion.div>
              ))}
            </div>}
          </div>

          <div className="card">
            <p className="section-title mb-1">Recent Alerts</p>
            <p className="section-sub mb-4">Across all patients</p>
            {alerts.length===0 ? <p className="text-slate-500 text-sm py-4 text-center">No alerts</p>
            : <div className="space-y-2">
              {alerts.map((a,i) => (
                <motion.div key={a.alert_id} initial={{opacity:0,x:10}} animate={{opacity:1,x:0}} transition={{delay:i*0.05}}
                  className="flex items-start gap-3 p-3 rounded-xl bg-slate-800/40">
                  <Badge severity={a.severity} />
                  <p className="text-xs text-slate-300 flex-1 leading-relaxed">{a.message}</p>
                </motion.div>
              ))}
            </div>}
          </div>
        </div>
      </div>
    </Layout>
  )
}
