export default function Spinner({ size='md' }) {
  const s = { sm:'w-4 h-4', md:'w-6 h-6', lg:'w-10 h-10' }[size]
  return <div className={`${s} border-2 border-slate-700 border-t-sky-500 rounded-full animate-spin`} />
}
