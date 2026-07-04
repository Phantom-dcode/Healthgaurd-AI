import { motion } from 'framer-motion'
export default function StatCard({ icon: Icon, label, value, sub, color='text-sky-400', index=0 }) {
  return (
    <motion.div className="stat-card"
      initial={{ opacity:0, y:20 }} animate={{ opacity:1, y:0 }}
      transition={{ delay: index*0.07 }}>
      <div className={`p-2.5 rounded-xl bg-slate-800 ${color}`}>
        <Icon className="w-5 h-5" />
      </div>
      <div>
        <p className="text-2xl font-bold text-slate-100">{value}</p>
        <p className="text-sm font-medium text-slate-300 mt-0.5">{label}</p>
        {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
      </div>
    </motion.div>
  )
}
