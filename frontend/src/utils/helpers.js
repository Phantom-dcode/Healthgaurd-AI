export const fmtDate = d => d ? new Date(d).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'}) : '—'
export const fmtTime = d => d ? new Date(d).toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'}) : '—'
export const fmtDateTime = d => d ? `${fmtDate(d)} ${fmtTime(d)}` : '—'
export const capitalize = s => s ? s.charAt(0).toUpperCase()+s.slice(1) : ''

export const severityColor = s => ({
  low:'text-emerald-400', medium:'text-amber-400', high:'text-orange-400', critical:'text-red-400'
}[s] || 'text-slate-400')

export const riskColor = r => ({
  low:'text-emerald-400', medium:'text-amber-400', high:'text-red-400'
}[r] || 'text-slate-400')

export const riskBg = r => ({
  low:'bg-emerald-500/10 border-emerald-500/30',
  medium:'bg-amber-500/10 border-amber-500/30',
  high:'bg-red-500/10 border-red-500/30'
}[r] || '')
