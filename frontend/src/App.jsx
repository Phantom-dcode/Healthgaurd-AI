import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import ProtectedRoute from './routes/ProtectedRoute'
import Spinner from './components/ui/Spinner'

// Auth
import Login    from './pages/auth/Login'
import Register from './pages/auth/Register'

// Patient
import PatientDashboard from './pages/patient/PatientDashboard'
import HealthHistory    from './pages/patient/HealthHistory'
import PatientAlerts    from './pages/patient/PatientAlerts'

// Doctor
import DoctorDashboard from './pages/doctor/DoctorDashboard'
import PatientList     from './pages/doctor/PatientList'
import PatientDetail   from './pages/doctor/PatientDetail'
import DoctorReports   from './pages/doctor/DoctorReports'

// Admin
import AdminDashboard  from './pages/admin/AdminDashboard'
import UserManagement  from './pages/admin/UserManagement'

function RootRedirect() {
  const { user, loading } = useAuth()
  if (loading) return <div className="min-h-screen flex items-center justify-center"><Spinner size="lg" /></div>
  if (!user)   return <Navigate to="/login" replace />
  if (user.role === 'patient') return <Navigate to="/patient"  replace />
  if (user.role === 'doctor')  return <Navigate to="/doctor"   replace />
  if (user.role === 'admin')   return <Navigate to="/admin"    replace />
  return <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/"         element={<RootRedirect />} />
      <Route path="/login"    element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Patient Routes */}
      <Route path="/patient" element={<ProtectedRoute roles={['patient']}><PatientDashboard /></ProtectedRoute>} />
      <Route path="/patient/records" element={<ProtectedRoute roles={['patient']}><HealthHistory /></ProtectedRoute>} />
      <Route path="/patient/alerts"  element={<ProtectedRoute roles={['patient']}><PatientAlerts /></ProtectedRoute>} />

      {/* Doctor Routes */}
      <Route path="/doctor"                     element={<ProtectedRoute roles={['doctor']}><DoctorDashboard /></ProtectedRoute>} />
      <Route path="/doctor/patients"            element={<ProtectedRoute roles={['doctor']}><PatientList /></ProtectedRoute>} />
      <Route path="/doctor/patients/:id"        element={<ProtectedRoute roles={['doctor']}><PatientDetail /></ProtectedRoute>} />
      <Route path="/doctor/reports"             element={<ProtectedRoute roles={['doctor']}><DoctorReports /></ProtectedRoute>} />
      <Route path="/doctor/alerts"              element={<ProtectedRoute roles={['doctor']}><PatientAlerts /></ProtectedRoute>} />

      {/* Admin Routes */}
      <Route path="/admin"        element={<ProtectedRoute roles={['admin']}><AdminDashboard /></ProtectedRoute>} />
      <Route path="/admin/users"  element={<ProtectedRoute roles={['admin']}><UserManagement /></ProtectedRoute>} />

      {/* Fallback */}
      <Route path="/unauthorized" element={
        <div className="min-h-screen flex items-center justify-center flex-col gap-4">
          <p className="text-2xl font-bold text-red-400">403 — Access Denied</p>
          <a href="/" className="text-sky-400 hover:underline text-sm">Go home</a>
        </div>
      } />
      <Route path="*" element={
        <div className="min-h-screen flex items-center justify-center flex-col gap-4">
          <p className="text-2xl font-bold text-slate-400">404 — Page Not Found</p>
          <a href="/" className="text-sky-400 hover:underline text-sm">Go home</a>
        </div>
      } />
    </Routes>
  )
}
