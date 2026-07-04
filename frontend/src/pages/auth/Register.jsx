import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Heart, Mail, Lock, User, Eye, EyeOff } from 'lucide-react'
import { register } from '../../api/auth'
import { getMe } from '../../api/auth'
import { useAuth } from '../../context/AuthContext'
import toast from 'react-hot-toast'

export default function Register() {
  const { signin }      = useAuth()
  const navigate        = useNavigate()
  const [form, setForm] = useState({ name:'', email:'', password:'', role:'patient' })
  const [show, setShow] = useState(false)
  const [loading, setLoading] = useState(false)

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const submit = async e => {
    e.preventDefault()
    setLoading(true)
    try {
      const { data: tokenData } = await register(form)
      const tokens = tokenData.data
      localStorage.setItem('access_token', tokens.access_token)
      const { data: userData } = await getMe()
      signin(tokens, userData.data)
      toast.success('Account created successfully!')
      const role = userData.data.role
      navigate(role === 'patient' ? '/patient' : role === 'doctor' ? '/doctor' : '/admin')
    } catch (err) {
      const d = err.response?.data
      toast.error(d?.message || d?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-sky-500/5 rounded-full blur-3xl" />
      </div>
      <motion.div initial={{ opacity:0, y:24 }} animate={{ opacity:1, y:0 }}
        transition={{ duration:0.4 }} className="w-full max-w-md relative">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 bg-sky-500/15 rounded-2xl mb-4 border border-sky-500/20">
            <Heart className="w-7 h-7 text-sky-400" strokeWidth={2.5} />
          </div>
          <h1 className="text-2xl font-bold text-slate-100">Create account</h1>
          <p className="text-slate-400 mt-1 text-sm">Join HealthGuard AI today</p>
        </div>
        <div className="card space-y-4">
          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">Full Name</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input name="name" value={form.name} onChange={handle} required
                  placeholder="John Doe" className="input-field pl-9" />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input name="email" type="email" value={form.email} onChange={handle} required
                  placeholder="you@example.com" className="input-field pl-9" />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input name="password" type={show ? 'text':'password'} value={form.password}
                  onChange={handle} required placeholder="Min 8 chars, 1 uppercase, 1 number" className="input-field pl-9 pr-10" />
                <button type="button" onClick={()=>setShow(s=>!s)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300">
                  {show ? <EyeOff className="w-4 h-4"/> : <Eye className="w-4 h-4"/>}
                </button>
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">I am a</label>
              <select name="role" value={form.role} onChange={handle} className="input-field">
                <option value="patient">Patient</option>
                <option value="doctor">Doctor</option>
              </select>
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? 'Creating account…' : 'Create Account'}
            </button>
          </form>
          <p className="text-center text-sm text-slate-500">
            Already have an account?{' '}
            <Link to="/login" className="text-sky-400 hover:text-sky-300 font-medium">Sign in</Link>
          </p>
        </div>
      </motion.div>
    </div>
  )
}
