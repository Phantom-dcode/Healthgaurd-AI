import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Heart, Mail, Lock, Eye, EyeOff } from 'lucide-react'
import { login } from '../../api/auth'
import { getMe } from '../../api/auth'
import { useAuth } from '../../context/AuthContext'
import toast from 'react-hot-toast'

export default function Login() {
  const { signin }      = useAuth()
  const navigate        = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [show, setShow] = useState(false)
  const [loading, setLoading] = useState(false)

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const submit = async e => {
    e.preventDefault()
    setLoading(true)
    try {
      const { data: tokenData } = await login(form)
      const tokens = tokenData.data
      // Temporarily store token to fetch user
      localStorage.setItem('access_token', tokens.access_token)
      const { data: userData } = await getMe()
      signin(tokens, userData.data)
      toast.success(`Welcome back, ${userData.data.name}!`)
      const role = userData.data.role
      navigate(role === 'patient' ? '/patient' : role === 'doctor' ? '/doctor' : '/admin')
    } catch (err) {
      toast.error(err.response?.data?.message || err.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      {/* Background glow */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-96 h-96 bg-sky-500/5 rounded-full blur-3xl" />
      </div>

      <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }} className="w-full max-w-md relative">

        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 bg-sky-500/15 rounded-2xl mb-4 border border-sky-500/20">
            <Heart className="w-7 h-7 text-sky-400" strokeWidth={2.5} />
          </div>
          <h1 className="text-2xl font-bold text-slate-100">Welcome back</h1>
          <p className="text-slate-400 mt-1 text-sm">Sign in to HealthGuard AI</p>
        </div>

        {/* Form */}
        <div className="card">
          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">Email address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input name="email" type="email" value={form.email} onChange={handle} required
                  placeholder="you@example.com" className="input-field pl-9" autoComplete="email" />
              </div>
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1.5">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input name="password" type={show ? 'text' : 'password'} value={form.password}
                  onChange={handle} required placeholder="••••••••" className="input-field pl-9 pr-10" />
                <button type="button" onClick={() => setShow(s => !s)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300">
                  {show ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full mt-2">
              {loading ? 'Signing in…' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-sm text-slate-500 mt-5">
            Don't have an account?{' '}
            <Link to="/register" className="text-sky-400 hover:text-sky-300 font-medium">Create account</Link>
          </p>
        </div>

        {/* Demo credentials */}
        <div className="mt-4 p-3 rounded-xl bg-slate-900/50 border border-slate-800 text-xs text-slate-500 text-center">
          Demo: <span className="text-slate-400">admin@healthguard.ai</span> / <span className="text-slate-400">Admin@123</span>
        </div>
      </motion.div>
    </div>
  )
}
