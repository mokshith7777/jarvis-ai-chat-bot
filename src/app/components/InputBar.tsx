'use client'

import { useRef, useEffect } from 'react'

interface InputBarProps {
  value: string
  onChange: (value: string) => void
  onSubmit: () => void
  disabled: boolean
}

export function InputBar({ value, onChange, onSubmit, disabled }: InputBarProps) {
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      onSubmit()
    }
  }

  return (
    <div style={{
      padding: '16px 24px',
      borderTop: '1px solid var(--border)',
      background: 'var(--surface)',
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '12px',
        maxWidth: '900px',
        margin: '0 auto',
      }}>
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message..."
          disabled={disabled}
          style={{
            flex: 1,
            padding: '12px 16px',
            borderRadius: '24px',
            background: 'var(--surface)',
            color: 'var(--text)',
            border: '1px solid var(--border)',
            fontSize: '15px',
          }}
        />
        <button
          onClick={onSubmit}
          disabled={disabled || !value.trim()}
          style={{
            padding: '12px 24px',
            borderRadius: '24px',
            background: disabled || !value.trim() ? 'var(--surface-2)' : 'var(--primary-grad)',
            color: disabled || !value.trim() ? 'var(--muted)' : '#fff',
            fontWeight: '600',
            fontSize: '15px',
            transition: 'all 0.2s',
          }}
        >
          Send
        </button>
      </div>
    </div>
  )
}