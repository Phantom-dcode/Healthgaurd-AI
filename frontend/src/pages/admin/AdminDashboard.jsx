import { useEffect, useState } from 'react'
import { Users, Activity, Shield, TrendingUp } from 'lucide-react'
import Layout from '../../components/layout/Layout'
import StatCard from '../../components/ui/StatCard'
import { listUsers } from '../../api/users'

export default function AdminDashboard() {
  const [users, setUsers] = useState([])
  useEffect(() => { listUsers().then(r => setUsers(r.data?.data || [])).catch(()=>{}) }, [])
  const patients = users.filter(u=>u.role==='patient').length
  const doctors  = users.filter(u=>u.role==='doctor').length
  const admins   = users.filter(u=>u.role==='admin').length
  const active   = users.filter(u=>u.is_active).length
  return (
    <Layout title="Admin Dashboard">
      <div className="space-y-6">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard index={0} icon={Users}    label="Total Users"    value={users.length} color="text-sky-400" />
          <StatCard index={1} icon={Users}    label="Patients"       value={patients}     color="text-purple-400" />
          <StatCard index={2} icon={Shield}   label="Doctors"        value={doctors}      color="text-emerald-400" />
          <StatCard index={3} icon={Activity} label="Active Users"   value={active}       color="text-amber-400" />
        </div>
        <div className="card">
          <p className="section-title mb-4">Recent Users</p>
          <div className="space-y-2">
            {users.slice(0,10).map(u=>(
              <div key={u.id} className="flex items-center gap-3 p-3 rounded-xl bg-slate-800/40">
                <div className="w-8 h-8 bg-sky-500/20 rounded-full flex items-center justify-center text-sky-400 font-semibold text-sm">
                  {u.name?.[0]?.toUpperCase()}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-200">{u.name}</p>
                  <p className="text-xs text-slate-500">{u.email}</p>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${u.role==='admin'?'bg-purple-500/20 text-purple-400':u.role==='doctor'?'bg-emerald-500/20 text-emerald-400':'bg-sky-500/20 text-sky-400'}`}>
                  {u.role}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${u.is_active?'bg-emerald-500/20 text-emerald-400':'bg-red-500/20 text-red-400'}`}>
                  {u.is_active?'Active':'Inactive'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  )
}
