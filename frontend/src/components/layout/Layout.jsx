import Sidebar from './Sidebar'
import Header from './Header'
import { motion } from 'framer-motion'

export default function Layout({ title, children }) {
  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-h-screen">
        <Header title={title} />
        <motion.main
          initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
          className="flex-1 p-6 overflow-auto"
        >
          {children}
        </motion.main>
      </div>
    </div>
  )
}
