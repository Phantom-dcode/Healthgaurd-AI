import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ClipboardList, Plus } from 'lucide-react'
import Layout from '../../components/layout/Layout'
import VitalsChart from '../../components/charts/VitalsChart'
import Modal from '../../components/ui/Modal'
import HealthRecordForm from '../../components/forms/HealthRecordForm'
import Spinner from '../../components/ui/Spinner'
import { listRecords } from '../../api/healthRecords'
import { fmtDateTime } from '../../utils/helpers'

const METRICS = [
  { key:'heart_rate',   label:'Heart Rate (bpm)'         },
  { key:'systolic_bp',  label:'Systolic BP (mmHg)'       },
  { key:'blood_sugar',  label:'Blood Sugar (mg/dL)'      },
  { key:'oxygen_level', label:'Oxygen Level (%)'         },
]

export default function HealthHistory() {
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [modal,   setModal]   = useState(false)
  const [metric,  setMetric]  = useState('heart_rate')

  const load = () => listRecords({ limit:30 }).then(r => setRecords(r.data?.data||[])).finally(()=>setLoading(false))
  useEffect(() => { load() }, [])

  return (
    <Layout title="Health History">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex gap-2 flex-wrap">
            {METRICS.map(m => (
              <button key={m.key} onClick={() => setMetric(m.key)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${metric===m.key ? 'bg-sky-500 text-white' : 'bg-slate-800 text-slate-400 hover:text-slate-200'}`}>
                {m.label.split(' ')[0]} {m.label.split(' ')[1]}
              </button>
            ))}
          </div>
          <button onClick={() => setModal(true)} className="btn-primary flex items-center gap-2 text-sm py-2 px-4">
            <Plus className="w-4 h-4" /> Log Vitals
          </button>
        </div>

        <div className="card">
          <p className="section-title mb-1">{METRICS.find(m=>m.key===metric)?.label}</p>
          <p className="section-sub mb-4">Last 30 readings</p>
          {loading ? <div className="flex justify-center py-10"><Spinner /></div>
            : <VitalsChart records={records} metric={metric} label={METRICS.find(m=>m.key===metric)?.label} />}
        </div>

        <div className="card">
          <p className="section-title mb-4">Recent Records</p>
          {loading ? <div className="flex justify-center py-8"><Spinner /></div>
          : records.length === 0 ? <p className="text-slate-500 text-center py-8">No records yet</p>
          : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-xs text-slate-500 border-b border-slate-800">
                    {['Date','BP','HR','Sugar','O2','Temp','Weight'].map(h=>(
                      <th key={h} className="pb-2 text-left font-medium pr-4">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {records.map((r,i) => (
                    <motion.tr key={r.record_id} initial={{opacity:0}} animate={{opacity:1}} transition={{delay:i*0.03}}
                      className="border-b border-slate-800/50 text-slate-300">
                      <td className="py-2.5 pr-4 text-slate-400 text-xs">{fmtDateTime(r.recorded_at)}</td>
                      <td className="py-2.5 pr-4">{r.systolic_bp && r.diastolic_bp ? `${r.systolic_bp}/${r.diastolic_bp}` : '—'}</td>
                      <td className="py-2.5 pr-4">{r.heart_rate ?? '—'}</td>
                      <td className="py-2.5 pr-4">{r.blood_sugar ?? '—'}</td>
                      <td className="py-2.5 pr-4">{r.oxygen_level ?? '—'}</td>
                      <td className="py-2.5 pr-4">{r.temperature ?? '—'}</td>
                      <td className="py-2.5 pr-4">{r.weight_kg ?? '—'}</td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
      <Modal open={modal} onClose={() => setModal(false)} title="Log Health Vitals">
        <HealthRecordForm onSuccess={() => { setModal(false); load() }} />
      </Modal>
    </Layout>
  )
}
