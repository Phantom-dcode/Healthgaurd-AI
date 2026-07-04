export default function Badge({ severity }) {
  const cls = { low:'badge-low', medium:'badge-medium', high:'badge-high', critical:'badge-critical' }
  return <span className={cls[severity] || 'badge-low'}>{severity}</span>
}
