import { useState } from 'react'
import { motion } from 'framer-motion'
import { submitRecord } from '../../api/healthRecords'
import toast from 'react-hot-toast'
import { Activity, Thermometer, Droplets, Wind, Scale, FileText } from 'lucide-react'

const FIELDS = [
  { key:'systolic_bp',  label:'Systolic BP',  unit:'mmHg', icon:Activity,    type:'number', placeholder:'e.g. 120' },
  { key:'diastolic_bp', label:'Diastolic BP', unit:'mmHg', icon:Activity,    type:'number', placeholder:'e.g. 80'  },
  { key:'heart_rate',   label:'Heart Rate',   unit:'bpm',  icon:Activity,    type:'number', placeholder:'e.g. 72'  },
  { key:'blood_sugar',  label:'Blood Sugar',  unit:'mg/dL',icon:Droplets,    type:'number', placeholder:'e.g. 100' },
  { key:'oxygen_level', label:'Oxygen Level', unit:'%',    icon:Wind,        type:'number', placeholder:'e.g. 98'  },
  { key:'temperature',  label:'Temperature',  unit:'°C',   icon:Thermometer, type:'number', placeholder:'e.g. 36.6'},
  { key:'weight_kg',    label:'Weight',       unit:'kg',   icon:Scale,       type:'number', placeholder:'e.g. 70'  },
]

export default function HealthRecordForm({ onSuccess }) {
  const [form,    setForm]    = useState({})
  const [loading, setLoading] = useState(false)

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const submit = async e => {
    e.preventDefault()
    setLoading(true)
    try {
      const payload = {}
      FIELDS.forEach(({ key }) => {
        if (form[key] !== '' && form[key] !== undefined) payload[key] = parseFloat(form[key])
      })
      if (form.notes) payload.notes = form.notes
      await submitRecord(payload)
      toast.success('Health record submitted! AI prediction generated.')
      setForm({})
      onSuccess?.()
    } catch (err) {
      const msg = err.response?.data?.detail || err.response?.data?.message || 'Submission failed'
      toast.error(typeof msg === 'string' ? msg : 'Validation error. Check your values.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.form onSubmit={submit} initial={{ opacity:0 }} animate={{ opacity:1 }}
      className="space-y-5">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {FIELDS.map(({ key, label, unit, icon: Icon, placeholder }) => (
          <div key={key}>
            <label className="block text-xs font-medium text-slate-400 mb-1.5">
              {label} <span className="text-slate-600">({unit})</span>
            </label>
            <div className="relative">
              <Icon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                name={key} type="number" step="any" value={form[key] || ''}
                onChange={handle} placeholder={placeholder}
                className="input-field pl-9"
              />
            </div>
          </div>
        ))}
      </div>
      <div>
        <label className="block text-xs font-medium text-slate-400 mb-1.5">
          <FileText className="inline w-3.5 h-3.5 mr-1" />Notes (optional)
        </label>
        <textarea name="notes" value={form.notes || ''} onChange={handle} rows={2}
          placeholder="Any symptoms or notes…"
          className="input-field resize-none" />
      </div>
      <button type="submit" disabled={loading} className="btn-primary w-full">
        {loading ? 'Submitting…' : 'Submit Health Record'}
      </button>
    </motion.form>
  )
}
