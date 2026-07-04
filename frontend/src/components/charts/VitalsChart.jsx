import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS, CategoryScale, LinearScale,
  PointElement, LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'
import { format } from 'date-fns'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const COLORS = {
  systolic:  '#EF4444',
  diastolic: '#F97316',
  heart_rate:'#0EA5E9',
  blood_sugar:'#A855F7',
  oxygen:    '#10B981',
  temperature:'#F59E0B',
}

export default function VitalsChart({ records = [], metric = 'heart_rate', label = 'Heart Rate (bpm)' }) {
  const sorted = [...records].sort((a, b) => new Date(a.recorded_at) - new Date(b.recorded_at)).slice(-14)

  const data = {
    labels: sorted.map(r => format(new Date(r.recorded_at), 'MMM d')),
    datasets: [{
      label,
      data:            sorted.map(r => r[metric]),
      borderColor:     COLORS[metric] || '#0EA5E9',
      backgroundColor: (COLORS[metric] || '#0EA5E9') + '18',
      borderWidth:     2,
      pointRadius:     4,
      pointHoverRadius:6,
      fill:            true,
      tension:         0.4,
    }],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { labels: { color: '#94A3B8', font: { size: 12 } } },
      tooltip: {
        backgroundColor: '#1E293B',
        borderColor:     '#334155',
        borderWidth:     1,
        titleColor:      '#F1F5F9',
        bodyColor:       '#94A3B8',
      },
    },
    scales: {
      x: { grid: { color: '#1E293B' }, ticks: { color: '#64748B' } },
      y: { grid: { color: '#1E293B' }, ticks: { color: '#64748B' } },
    },
  }

  return (
    <div className="h-56">
      {sorted.length > 0
        ? <Line data={data} options={options} />
        : <div className="h-full flex items-center justify-center text-slate-500 text-sm">No data yet</div>
      }
    </div>
  )
}
