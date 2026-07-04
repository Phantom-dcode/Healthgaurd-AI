import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Users, Search, UserPlus } from 'lucide-react'
import Layout from '../../components/layout/Layout'
import Spinner from '../../components/ui/Spinner'
import Modal from '../../components/ui/Modal'
import { getMyPatients, assignPatient } from '../../api/doctors'
import { listPatients } from '../../api/patients'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

export default function PatientList() {
  const [patients, setPatients] = useState([])
  const [all,      setAll]      = useState([])
  const [loading,  setLoading]  = useState(true)
  const [modal,    setModal]    = useState(false)
  const [search,   setSearch]   = useState('')
  const navigate = useNavigate()

  const load = async () => {
    try {
      const r = await getMyPatients()
      setPatients(r.data?.data || [])
    } finally { setLoading(false) }
  }

  const openAssign = async () => {
    const r = await listPatients()
    setAll(r.data?.data || [])
    setModal(true)
  }

  const assign = async id => {
    try {
      await assignPatient({ patient_id: id })
      toast.success('Patient assigned!')
      setModal(false)
      load()
    } catch { toast.error('Failed to assign') }
  }

  useEffect(() => { load() }, [])
  const filtered = patients.filter(p => p.name?.toLowerCase().includes(search.toLowerCase()))

  return (
    <Layout title="My Patients">
      <div className="space-y-4">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input value={search} onChange={e=>setSearch(e.target.value)}
              placeholder="Search patients…" className="input-field pl-9" />
          </div>
          <button onClick={openAssign} className="btn-primary flex items-center gap-2">
            <UserPlus className="w-4 h-4" /> Assign Patient
          </button>
        </div>

        {loading ? <div className="flex justify-center py-20"><Spinner size="lg" /></div>
        : filtered.length===0 ? (
          <div className="card text-center py-16">
            <Users className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <p className="text-slate-400">No patients found</p>
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map((p,i)=>(
              <motion.div key={p.patient_id} initial={{opacity:0,y:16}} animate={{opacity:1,y:0}} transition={{delay:i*0.06}}
                onClick={() => navigate(`/doctor/patients/${p.patient_id}`)}
                className="card hover:border-sky-500/30 cursor-pointer transition-all hover:shadow-lg hover:shadow-sky-500/5">
                <div className="flex items-center gap-3 mb-3">
                  <div className="w-10 h-10 bg-sky-500/20 rounded-xl flex items-center justify-center text-sky-400 font-bold">
                    {p.name?.[0]?.toUpperCase()}
                  </div>
                  <div>
                    <p className="font-medium text-slate-200">{p.name}</p>
                    <p className="text-xs text-slate-500">{p.email}</p>
                  </div>
                </div>
                <p className="text-xs text-slate-600">Assigned {new Date(p.assigned_at).toLocaleDateString()}</p>
              </motion.div>
            ))}
          </div>
        )}
      </div>
      <Modal open={modal} onClose={()=>setModal(false)} title="Assign a Patient">
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {all.map(p => (
            <div key={p.patient_id} className="flex items-center justify-between p-3 rounded-xl bg-slate-800">
              <div>
                <p className="text-sm font-medium text-slate-200">{p.user_name}</p>
                <p className="text-xs text-slate-500">{p.user_email}</p>
              </div>
              <button onClick={()=>assign(p.patient_id)} className="btn-primary text-xs py-1.5 px-3">Assign</button>
            </div>
          ))}
        </div>
      </Modal>
    </Layout>
  )
}
