'use client'

import { useEffect, useRef } from 'react'
import { Message } from './Message'
import { Logo } from './Logo'

interface MessageListProps {
  messages: {
    id: string
    role: 'user' | 'assistant'
    content: string
    timestamp: string
  }[]
  isLoading: boolean
  endRef: React.RefObject<HTMLDivElement>
  user?: { displayName?: string | null; email?: string | null; photoURL?: string | null }
}

export function MessageList({ messages, isLoading, endRef, user }: MessageListProps) {
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, isLoading, endRef])

  if (messages.length === 0) {
    return <div style={{ flex: 1 }} />
  }

  return (
    <div style={{ flex: 1, overflowY: 'auto', padding: '16px 24px 8px' }}>
      {messages.map((m) => (
        <Message key={m.id} message={m} user={user} />
      ))}
      {isLoading && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          margin: '10px 0',
          paddingLeft: '4px',
        }}>
          <Logo kind="avatar" size={32} />
          <div style={{
            display: 'flex',
            gap: '5px',
            alignItems: 'center',
            padding: '12px 16px',
            background: 'var(--surface-2)',
            borderRadius: '18px 18px 18px 4px',
            border: '1px solid var(--border)',
          }}>
            <span className="jarvis-dot" style={{
              width: 7,
              height: 7,
              borderRadius: '50%',
              background: 'var(--cyan)',
              animation: 'jarvis-blink 1.4s infinite both',
            }} />
            <span className="jarvis-dot" style={{
              width: 7,
              height: 7,
              borderRadius: '50%',
              background: 'var(--cyan)',
              animation: 'jarvis-blink 1.4s infinite both',
              animationDelay: '0.2s',
            }} />
            <span className="jarvis-dot" style={{
              width: 7,
              height: 7,
              borderRadius: '50%',
              background: 'var(--cyan)',
              animation: 'jarvis-blink 1.4s infinite both',
              animationDelay: '0.4s',
            }} />
          </div>
        </div>
      )}
      <div ref={endRef} />
    </div>
  )
}