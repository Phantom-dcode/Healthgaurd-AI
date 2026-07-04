import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Activity, Heart, Droplets, Wind, AlertTriangle, TrendingUp, Plus } from 'lucide-react'
import Layout from '../../components/layout/Layout'
import StatCard from '../../components/ui/StatCard'
import VitalsChart from '../../components/charts/VitalsChart'
import RiskGauge from '../../components/charts/RiskGauge'
import HealthRecordForm from '../../components/forms/HealthRecordForm'
import Modal from '../../components/ui/Modal'
import Badge from '../../components/ui/Badge'
import { listRecords } from '../../api/healthRecords'
import { alertsSummary, listAlerts } from '../../api/alerts'
import { latestPrediction } from '../../api/predictions'
import { fmtDateTime } from '../../utils/helpers'

export default function PatientDashboard() {
  const [records,    setRecords]    = useState([])
  const [alerts,     setAlerts]     = useState([])
  const [summary,    setSummary]    = useState({})
  const [prediction, setPrediction] = useState(null)
  const [modal,      setModal]      = useState(false)

  const load = async () => {
    try {
      const [recs, sum, alts, pred] = await Promise.allSettled([
        listRecords({ limit: 14 }),
        alertsSummary(),
        listAlerts({ limit: 5, unread_only: true }),
        latestPrediction(),
      ])
      if (recs.status === 'fulfilled')  setRecords(recs.value.data?.data || [])
      if (sum.status  === 'fulfilled')  setSummary(sum.value.data?.data  || {})
      if (alts.status === 'fulfilled')  setAlerts(alts.value.data?.data  || [])
      if (pred.status === 'fulfilled')  setPrediction(pred.value.data?.data)
    } catch {}
  }

  useEffect(() => { load() }, [])
  const latest = records[0]

  return (
    <Layout title="My Dashboard">
      <div className="space-y-6">
        {/* KPI Row */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard index={0} icon={Activity}       label="Heart Rate"    value={latest?.heart_rate   ? `${latest.heart_rate} bpm`   : '—'} color="text-sky-400" />
          <StatCard index={1} icon={Heart}          label="Blood Pressure" value={latest?.systolic_bp  ? `${latest.systolic_bp}/${latest.diastolic_bp}` : '—'} color="text-red-400" />
          <StatCard index={2} icon={Droplets}       label="Blood Sugar"   value={latest?.blood_sugar  ? `${latest.blood_sugar} mg/dL` : '—'} color="text-purple-400" />
          <StatCard index={3} icon={Wind}           label="Oxygen"        value={latest?.oxygen_level ? `${latest.oxygen_level}%`    : '—'} color="text-emerald-400" />
        </div>

        {/* Middle Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Chart */}
          <div className="card lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="section-title">Heart Rate Trend</p>
                <p className="section-sub">Last 14 readings</p>
              </div>
              <button onClick={() => setModal(true)} className="btn-primary flex items-center gap-2 text-sm py-2 px-4">
                <Plus className="w-4 h-4" /> Log Vitals
              </button>
            </div>
            <VitalsChart records={records} metric="heart_rate" label="Heart Rate (bpm)" />
          </div>

          {/* Risk Gauge */}
          <div className="card flex flex-col items-center justify-center text-center">
            <p className="section-title mb-1">AI Risk Score</p>
            <p className="section-sub mb-4">Based on latest vitals</p>
            {prediction
              ? <RiskGauge riskLevel={prediction.risk_level} riskScore={prediction.risk_score} />
              : <p className="text-slate-500 text-sm mt-4">Submit a record to get your risk score</p>
            }
            {prediction && (
              <p className="text-xs text-slate-500 mt-3">
                Model v{prediction.model_version} • {fmtDateTime(prediction.created_at)}
              </p>
            )}
          </div>
        </div>

        {/* Alerts */}
        {alerts.length > 0 && (
          <div className="card">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <p className="section-title">Unread Alerts ({summary.unread || 0})</p>
            </div>
            <div className="space-y-2">
              {alerts.map(a => (
                <motion.div key={a.alert_id} initial={{opacity:0,x:-10}} animate={{opacity:1,x:0}}
                  className="flex items-start gap-3 p-3 rounded-xl bg-slate-800/50 border border-slate-700/50">
                  <Badge severity={a.severity} />
                  <p className="text-sm text-slate-300 flex-1">{a.message}</p>
                  <span className="text-xs text-slate-500 shrink-0">{fmtDateTime(a.created_at)}</span>
                </motion.div>
              ))}
            </div>
          </div>
        )}
      </div>

      <Modal open={modal} onClose={() => setModal(false)} title="Log Health Vitals">
        <HealthRecordForm onSuccess={() => { setModal(false); load() }} />
      </Modal>
    </Layout>
  )
}
