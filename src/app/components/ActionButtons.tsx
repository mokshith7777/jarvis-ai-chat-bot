'use client'

interface ActionButtonsProps {
  isLoading: boolean
  onRegenerate: () => void
  onClear: () => void
  onStop: () => void
  hasAssistantMessage: boolean
}

function Button({ label, onClick, disabled, danger }: { label: string; onClick: () => void; disabled?: boolean; danger?: boolean }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        padding: '5px 12px',
        borderRadius: '14px',
        fontSize: '12px',
        background: danger ? 'var(--neon-soft)' : 'var(--gold-soft)',
        color: danger ? 'var(--neon)' : 'var(--gold)',
        border: `1px solid ${danger ? 'var(--neon)' : 'var(--border)'}`,
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.4 : 1,
      }}
    >
      {label}
    </button>
  )
}

export function ActionButtons({ isLoading, onRegenerate, onClear, onStop, hasAssistantMessage }: ActionButtonsProps) {
  return (
    <div style={{
      display: 'flex',
      gap: '8px',
      padding: '8px 24px',
      borderBottom: '1px solid var(--border)',
      background: 'var(--surface)',
    }}>
      <Button label="Regenerate" onClick={onRegenerate} disabled={isLoading || !hasAssistantMessage} />
      <Button label="Clear" onClick={onClear} disabled={isLoading} />
      {isLoading && <Button label="Stop" onClick={onStop} disabled={false} danger={true} />}
    </div>
  )
}