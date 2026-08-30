'use client'

interface QuotaBarProps {
  remaining: number
}

export function QuotaBar({ remaining }: QuotaBarProps) {
  const used = 24 - remaining
  const percent = Math.min(100, (used / 24) * 100)

  return (
    <div style={{
      padding: '8px 24px',
      borderBottom: '1px solid var(--border)',
      background: 'var(--surface)',
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        fontSize: '12px',
        marginBottom: '5px',
      }}>
        <span style={{
          color: remaining <= 3 ? 'var(--neon)' : 'var(--gold)',
          fontWeight: 600,
        }}>
          {remaining > 0
            ? `Daily limit: ${used}/24 used \u00B7 ${remaining} left`
            : 'Daily limit reached \u2014 resets in 24h'}
        </span>
        <span style={{ color: 'var(--muted)' }}>Resets daily at midnight UTC</span>
      </div>
      <div style={{
        height: '5px',
        borderRadius: '3px',
        background: 'rgba(255,0,51,0.12)',
        overflow: 'hidden',
      }}>
        <div style={{
          height: '100%',
          width: `${percent}%`,
          background: remaining <= 3 ? 'var(--neon)' : 'linear-gradient(90deg, var(--gold), var(--cyan))',
          transition: 'width 0.3s ease',
        }} />
      </div>
    </div>
  )
}