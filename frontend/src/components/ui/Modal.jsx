import { motion, AnimatePresence } from 'framer-motion'
import { X } from 'lucide-react'
export default function Modal({ open, onClose, title, children }) {
  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}}
            className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
          <motion.div initial={{opacity:0,scale:0.95,y:10}} animate={{opacity:1,scale:1,y:0}}
            exit={{opacity:0,scale:0.95}} transition={{type:'spring',damping:25}}
            className="relative card w-full max-w-lg z-10 shadow-2xl">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-slate-100">{title}</h2>
              <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors">
                <X className="w-4 h-4" />
              </button>
            </div>
            {children}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
