import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Users, UserX, Trash2, Search } from 'lucide-react'
import Layout from '../../components/layout/Layout'
import Spinner from '../../components/ui/Spinner'
import { listUsers, deactivateUser, deleteUser } from '../../api/users'
import { fmtDate } from '../../utils/helpers'
import toast from 'react-hot-toast'

export default function UserManagement() {
  const [users,   setUsers]   = useState([])
  const [loading, setLoading] = useState(true)
  const [search,  setSearch]  = useState('')

  const load = () => listUsers().then(r=>setUsers(r.data?.data||[])).finally(()=>setLoading(false))
  useEffect(()=>{ load() },[])

  const deactivate = async id => {
    if (!confirm('Deactivate this user?')) return
    await deactivateUser(id); toast.success('User deactivated'); load()
  }
  const del = async id => {
    if (!confirm('Permanently delete this user and ALL their data?')) return
    await deleteUser(id); toast.success('User deleted'); load()
  }

  const filtered = users.filter(u=>
    u.name?.toLowerCase().includes(search.toLowerCase()) ||
    u.email?.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <Layout title="User Management">
      <div className="space-y-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
          <input value={search} onChange={e=>setSearch(e.target.value)}
            placeholder="Search by name or email…" className="input-field pl-9" />
        </div>
        {loading ? <div className="flex justify-center py-20"><Spinner size="lg" /></div>
        : (
          <div className="card overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-xs text-slate-500 border-b border-slate-800">
                  {['Name','Email','Role','Status','Joined','Actions'].map(h=>(
                    <th key={h} className="pb-3 text-left font-medium pr-6">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filtered.map((u,i)=>(
                  <motion.tr key={u.id} initial={{opacity:0}} animate={{opacity:1}} transition={{delay:i*0.03}}
                    className="border-b border-slate-800/40 text-slate-300">
                    <td className="py-3 pr-6 font-medium">{u.name}</td>
                    <td className="py-3 pr-6 text-slate-400 text-xs">{u.email}</td>
                    <td className="py-3 pr-6">
                      <span className={`text-xs px-2 py-0.5 rounded-full ${u.role==='admin'?'bg-purple-500/20 text-purple-400':u.role==='doctor'?'bg-emerald-500/20 text-emerald-400':'bg-sky-500/20 text-sky-400'}`}>
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3 pr-6">
                      <span className={`text-xs px-2 py-0.5 rounded-full ${u.is_active?'bg-emerald-500/20 text-emerald-400':'bg-red-500/20 text-red-400'}`}>
                        {u.is_active?'Active':'Inactive'}
                      </span>
                    </td>
                    <td className="py-3 pr-6 text-slate-500 text-xs">{fmtDate(u.created_at)}</td>
                    <td className="py-3 flex gap-2">
                      <button onClick={()=>deactivate(u.id)} title="Deactivate"
                        className="p-1.5 rounded-lg hover:bg-amber-500/10 text-slate-500 hover:text-amber-400 transition-colors">
                        <UserX className="w-4 h-4" />
                      </button>
                      <button onClick={()=>del(u.id)} title="Delete"
                        className="p-1.5 rounded-lg hover:bg-red-500/10 text-slate-500 hover:text-red-400 transition-colors">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  )
}
