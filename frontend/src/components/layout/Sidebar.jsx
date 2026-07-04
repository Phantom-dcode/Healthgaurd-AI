import { NavLink, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../../context/AuthContext'
import { logout as apiLogout } from '../../api/auth'
import {
  Heart, LayoutDashboard, ClipboardList, Bell,
  FileText, Users, Activity, LogOut, Shield, UserCircle
} from 'lucide-react'
import toast from 'react-hot-toast'

const NAV = {
  patient: [
    { to: '/patient',          icon: LayoutDashboard, label: 'Dashboard'     },
    { to: '/patient/records',  icon: ClipboardList,   label: 'Health Records' },
    { to: '/patient/alerts',   icon: Bell,            label: 'Alerts'         },
    { to: '/patient/profile',  icon: UserCircle,      label: 'My Profile'     },
  ],
  doctor: [
    { to: '/doctor',           icon: LayoutDashboard, label: 'Dashboard'     },
    { to: '/doctor/patients',  icon: Users,           label: 'My Patients'   },
    { to: '/doctor/reports',   icon: FileText,        label: 'Reports'       },
    { to: '/doctor/alerts',    icon: Bell,            label: 'Alerts'        },
  ],
  admin: [
    { to: '/admin',            icon: LayoutDashboard, label: 'Dashboard'     },
    { to: '/admin/users',      icon: Users,           label: 'Users'         },
    { to: '/admin/audit',      icon: Activity,        label: 'Audit Logs'    },
  ],
}

export default function Sidebar() {
  const { user, signout } = useAuth()
  const navigate   = useNavigate()
  const links      = NAV[user?.role] || []

  const handleLogout = async () => {
    try { await apiLogout() } catch {}
    signout()
    toast.success('Logged out')
    navigate('/login')
  }

  return (
    <motion.aside
      initial={{ x: -280 }} animate={{ x: 0 }} transition={{ type: 'spring', damping: 25 }}
      className="fixed inset-y-0 left-0 w-64 bg-slate-900 border-r border-slate-800 flex flex-col z-30"
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-slate-800">
        <div className="w-9 h-9 bg-sky-500 rounded-xl flex items-center justify-center">
          <Heart className="w-5 h-5 text-white" strokeWidth={2.5} />
        </div>
        <div>
          <p className="font-bold text-slate-100 leading-none">HealthGuard</p>
          <p className="text-xs text-sky-400 font-medium mt-0.5">AI Platform</p>
        </div>
      </div>

      {/* Nav Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to} end
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ` +
              (isActive
                ? 'bg-sky-500/15 text-sky-400 border border-sky-500/20'
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800')
            }
          >
            <Icon className="w-4.5 h-4.5 shrink-0" />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* User + Logout */}
      <div className="px-3 pb-4 border-t border-slate-800 pt-3">
        <div className="flex items-center gap-3 px-3 py-2 mb-2">
          <div className="w-8 h-8 bg-sky-500/20 rounded-full flex items-center justify-center">
            <span className="text-sky-400 text-sm font-semibold">
              {user?.name?.[0]?.toUpperCase()}
            </span>
          </div>
          <div className="min-w-0">
            <p className="text-sm font-medium text-slate-200 truncate">{user?.name}</p>
            <p className="text-xs text-slate-500 capitalize">{user?.role}</p>
          </div>
        </div>
        <button onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-all">
          <LogOut className="w-4 h-4" /> Logout
        </button>
      </div>
    </motion.aside>
  )
}
