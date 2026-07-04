import { useEffect, useState } from 'react'
import { FileText, Plus } from 'lucide-react'
import Layout from '../../components/layout/Layout'
import Modal from '../../components/ui/Modal'
import { listReports, createReport } from '../../api/reports'
import { getMyPatients } from '../../api/doctors'
import { fmtDate } from '../../utils/helpers'
import toast from 'react-hot-toast'

export default function DoctorReports() {
  const [reports,  setReports]  = useState([])
  const [patients, setPatients] = useState([])
  const [modal,    setModal]    = useState(false)
  const [form,     setForm]     = useState({ patient_id:'', title:'', date_from:'', date_to:'' })

  const load = async () => {
    const [r,p] = await Promise.allSettled([listReports(), getMyPatients()])
    if (r.status==='fulfilled') setReports(r.value.data?.data||[])
    if (p.status==='fulfilled') setPatients(p.value.data?.data||[])
  }
  useEffect(()=>{ load() },[])

  const submit = async e => {
    e.preventDefault()
    try {
      await createReport(form)
      toast.success('Report created')
      setModal(false)
      load()
    } catch { toast.error('Failed to create report') }
  }

  return (
    <Layout title="Reports">
      <div className="space-y-4">
        <div className="flex justify-end">
          <button onClick={()=>setModal(true)} className="btn-primary flex items-center gap-2">
            <Plus className="w-4 h-4" /> New Report
          </button>
        </div>
        {reports.length===0 ? (
          <div className="card text-center py-16">
            <FileText className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <p className="text-slate-400">No reports yet</p>
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {reports.map(r=>(
              <div key={r.report_id} className="card hover:border-sky-500/30 transition-colors">
                <div className="flex items-start gap-3">
                  <div className="p-2 rounded-lg bg-sky-500/10"><FileText className="w-4 h-4 text-sky-400" /></div>
                  <div>
                    <p className="font-medium text-slate-200 text-sm">{r.title || 'Health Report'}</p>
                    <p className="text-xs text-slate-500 mt-0.5">{r.patient_name}</p>
                    <p className="text-xs text-slate-600 mt-1">{fmtDate(r.date_from)} → {fmtDate(r.date_to)}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <Modal open={modal} onClose={()=>setModal(false)} title="Create Report">
        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="block text-xs text-slate-400 mb-1.5">Patient</label>
            <select value={form.patient_id} onChange={e=>setForm(f=>({...f,patient_id:e.target.value}))} className="input-field" required>
              <option value="">Select patient…</option>
              {patients.map(p=><option key={p.patient_id} value={p.patient_id}>{p.name}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs text-slate-400 mb-1.5">Report Title</label>
            <input value={form.title} onChange={e=>setForm(f=>({...f,title:e.target.value}))} placeholder="Monthly Health Review" className="input-field" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs text-slate-400 mb-1.5">From</label>
              <input type="date" value={form.date_from} onChange={e=>setForm(f=>({...f,date_from:e.target.value}))} className="input-field" required />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1.5">To</label>
              <input type="date" value={form.date_to} onChange={e=>setForm(f=>({...f,date_to:e.target.value}))} className="input-field" required />
            </div>
          </div>
          <button type="submit" className="btn-primary w-full">Create Report</button>
        </form>
      </Modal>
    </Layout>
  )
}
