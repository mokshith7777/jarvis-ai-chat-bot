'use client'

import { Logo } from './Logo'

interface HeaderProps {
  selectedModel: string
  onModelChange: (model: string) => void
  modelOptions: { id: string; key: string; description: string; category: string }[]
  quotaRemaining: number | null
  user: { displayName?: string | null; email?: string | null; photoURL?: string | null }
  onSignOut: () => void
}

export function Header({
  selectedModel,
  onModelChange,
  modelOptions,
  quotaRemaining,
  user,
  onSignOut,
}: HeaderProps) {
  const quotaDisplay = quotaRemaining !== null ? (
    <div
      title={quotaRemaining > 0 ? `${quotaRemaining} messages left today` : 'Daily limit reached — resets in 24h'}
      style={{
        padding: '5px 10px',
        borderRadius: '14px',
        fontSize: '12px',
        fontWeight: 600,
        whiteSpace: 'nowrap',
        background: quotaRemaining <= 3 ? 'var(--neon-soft)' : 'var(--gold-soft)',
        color: quotaRemaining <= 3 ? 'var(--neon)' : 'var(--gold)',
        border: `1px solid ${quotaRemaining <= 3 ? 'var(--neon)' : 'var(--border)'}`,
      }}
    >
      {quotaRemaining > 0 ? `${quotaRemaining} left` : 'Limit reached'}
    </div>
  ) : null

  return (
    <header style={{
      display: 'flex',
      flexWrap: 'wrap',
      gap: '10px',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '12px 16px',
      borderBottom: '1px solid var(--border)',
      background: 'var(--surface)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <Logo kind="logo" size={34} />
        <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.1 }}>
          <h1 style={{
            fontSize: '20px',
            fontWeight: '600',
            color: 'var(--primary)',
            textShadow: '0 0 14px rgba(255,0,51,0.4)',
          }}>
            JARVIS AI
          </h1>
          <span style={{ fontSize: '10px', color: 'var(--muted)', letterSpacing: '0.3px' }}>
            Created by MOKSHITH Reddy \u00B7 Founder & Architect
          </span>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {quotaDisplay}
        <select
          value={selectedModel}
          onChange={(e) => onModelChange(e.target.value)}
          style={{
            padding: '8px 12px',
            borderRadius: '8px',
            background: 'var(--surface)',
            color: 'var(--text)',
            border: '1px solid var(--border)',
            fontSize: '14px',
            maxWidth: '180px',
          }}
        >
          {modelOptions.map((m) => (
            <option key={m.id} value={m.id}>
              {m.id} \u2014 {m.category}
            </option>
          ))}
        </select>
        {user ? (
          <button
            onClick={onSignOut}
            title={user.displayName || user.email || 'Sign out'}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '4px 10px',
              borderRadius: '20px',
              background: 'var(--gold-soft)',
              border: '1px solid var(--border)',
              color: 'var(--text)',
              fontSize: '13px',
            }}
          >
            {user.photoURL ? (
              <img src={user.photoURL} alt="" width={28} height={28} style={{ borderRadius: '50%' }} />
            ) : (
              <div style={{
                width: '28px',
                height: '28px',
                borderRadius: '50%',
                background: 'linear-gradient(135deg, var(--cyan-deep), var(--surface-2))',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '12px',
                color: 'var(--gold)',
              }}>
                {(user.displayName || user.email || '?').charAt(0).toUpperCase()}
              </div>
            )}
            <span>Sign Out</span>
          </button>
        ) : (
          <button
            onClick={() => {}}
            style={{
              padding: '8px 16px',
              borderRadius: '20px',
              background: 'linear-gradient(135deg, var(--gold), var(--cyan))',
              color: '#040406',
              fontWeight: '600',
              fontSize: '14px',
            }}
          >
            Sign In
          </button>
        )}
      </div>
    </header>
  )
}