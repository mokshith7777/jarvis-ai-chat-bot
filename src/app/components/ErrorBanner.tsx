'use client'

interface ErrorBannerProps {
  message: string
}

export function ErrorBanner({ message }: ErrorBannerProps) {
  return (
    <div style={{
      padding: '10px 24px',
      background: 'var(--neon-soft)',
      color: '#ff6b85',
      fontSize: '14px',
      borderBottom: '1px solid var(--border)',
    }}>
      {message}
    </div>
  )
}