import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import Layout from '../../components/layout/Layout'
import VitalsChart from '../../components/charts/VitalsChart'
import RiskGauge from '../../components/charts/RiskGauge'
import Badge from '../../components/ui/Badge'
import Spinner from '../../components/ui/Spinner'
import { listRecords } from '../../api/healthRecords'
import { listAlerts } from '../../api/alerts'
import { listPredictions } from '../../api/predictions'
import { fmtDateTime } from '../../utils/helpers'

export default function PatientDetail() {
  const { id } = useParams()
  const [records, setRecords] = useState([])
  const [alerts,  setAlerts]  = useState([])
  const [preds,   setPreds]   = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.allSettled([
      listRecords({ patient_id: id, limit: 14 }),
      listAlerts({ patient_id: id, limit: 10 }),
      listPredictions(),
    ]).then(([r,a,p]) => {
      if (r.status==='fulfilled') setRecords(r.value.data?.data||[])
      if (a.status==='fulfilled') setAlerts(a.value.data?.data||[])
      if (p.status==='fulfilled') setPreds(p.value.data?.data||[])
    }).finally(()=>setLoading(false))
  }, [id])

  const latest = records[0]
  const latestPred = preds[0]

  if (loading) return <Layout title="Patient Detail"><div className="flex justify-center py-20"><Spinner size="lg" /></div></Layout>

  return (
    <Layout title="Patient Detail">
      <div className="space-y-6">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            ['BP', latest?.systolic_bp ? `${latest.systolic_bp}/${latest.diastolic_bp}` : '—'],
            ['Heart Rate', latest?.heart_rate ? `${latest.heart_rate} bpm` : '—'],
            ['Blood Sugar', latest?.blood_sugar ? `${latest.blood_sugar} mg/dL` : '—'],
            ['Oxygen', latest?.oxygen_level ? `${latest.oxygen_level}%` : '—'],
          ].map(([l,v],i)=>(
            <div key={l} className="card-sm text-center">
              <p className="text-xl font-bold text-slate-100">{v}</p>
              <p className="text-xs text-slate-400 mt-1">{l}</p>
            </div>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-4">
          <div className="card lg:col-span-2">
            <p className="section-title mb-4">Vitals Trend</p>
            <VitalsChart records={records} metric="heart_rate" label="Heart Rate (bpm)" />
          </div>
          <div className="card flex flex-col items-center justify-center text-center">
            <p className="section-title mb-1">AI Risk</p>
            {latestPred ? <RiskGauge riskLevel={latestPred.risk_level} riskScore={latestPred.risk_score} />
              : <p className="text-slate-500 text-sm mt-4">No prediction yet</p>}
          </div>
        </div>

        <div className="card">
          <p className="section-title mb-4">Recent Alerts</p>
          {alerts.length===0 ? <p className="text-slate-500 text-sm text-center py-4">No alerts</p>
          : <div className="space-y-2">
            {alerts.map(a=>(
              <div key={a.alert_id} className="flex items-start gap-3 p-3 rounded-xl bg-slate-800/40">
                <Badge severity={a.severity} />
                <p className="text-sm text-slate-300 flex-1">{a.message}</p>
                <span className="text-xs text-slate-500">{fmtDateTime(a.created_at)}</span>
              </div>
            ))}
          </div>}
        </div>
      </div>
    </Layout>
  )
}
