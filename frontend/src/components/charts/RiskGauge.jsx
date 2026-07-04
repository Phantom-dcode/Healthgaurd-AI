import { Doughnut } from 'react-chartjs-2'
import { Chart as ChartJS, ArcElement, Tooltip } from 'chart.js'
ChartJS.register(ArcElement, Tooltip)

const RISK_CONFIG = {
  low:    { color: '#10B981', label: 'Low Risk',      bg: 'bg-emerald-500/10' },
  medium: { color: '#F59E0B', label: 'Medium Risk',   bg: 'bg-amber-500/10'  },
  high:   { color: '#EF4444', label: 'High Risk',     bg: 'bg-red-500/10'    },
}

export default function RiskGauge({ riskLevel = 'low', riskScore = 0 }) {
  const cfg  = RISK_CONFIG[riskLevel] || RISK_CONFIG.low
  const pct  = Math.round(parseFloat(riskScore) * 100)

  const data = {
    datasets: [{
      data:            [pct, 100 - pct],
      backgroundColor: [cfg.color, '#1E293B'],
      borderWidth:     0,
      circumference:   180,
      rotation:        -90,
    }],
  }

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-40">
        <Doughnut data={data} options={{ plugins: { tooltip: { enabled: false } }, cutout: '80%' }} />
        <div className="absolute inset-0 flex flex-col items-center justify-end pb-2">
          <span className="text-2xl font-bold" style={{ color: cfg.color }}>{pct}%</span>
          <span className="text-xs text-slate-400">{cfg.label}</span>
        </div>
      </div>
    </div>
  )
}
