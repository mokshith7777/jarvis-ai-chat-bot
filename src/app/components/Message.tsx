'use client'

import { Logo } from './Logo'
import { MarkdownRenderer } from './MarkdownRenderer'

interface MessageProps {
  message: {
    id: string
    role: 'user' | 'assistant'
    content: string
    timestamp: string
  }
  user?: { displayName?: string | null; email?: string | null; photoURL?: string | null }
}

export function Message({ message, user }: MessageProps) {
  const isUser = message.role === 'user'

  const avatar = isUser ? (
    user?.photoURL ? (
      <img src={user.photoURL} alt="You" style={{ width: 32, height: 32, borderRadius: '50%', objectFit: 'cover' }} />
    ) : (
      <div style={{
        width: 32,
        height: 32,
        borderRadius: '50%',
        background: 'linear-gradient(135deg, #d4af37, #e8c54a)',
        color: '#06070c',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: 700,
        fontSize: 14,
      }}>
        {(user?.displayName || user?.email || 'U').charAt(0).toUpperCase()}
      </div>
    )
  ) : (
    <Logo kind="avatar" size={32} />
  )

  return (
    <div style={{
      display: 'flex',
      flexDirection: isUser ? 'row-reverse' : 'row',
      alignItems: 'flex-end',
      gap: '8px',
      margin: '10px 0',
      animation: 'jarvis-fade-in 0.28s ease-out',
    }}>
      {avatar}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        maxWidth: isUser ? '78%' : '85%',
      }}>
        <div style={{
          padding: isUser ? '11px 15px' : '13px 16px',
          borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
          background: isUser ? 'var(--primary-grad)' : 'var(--surface-2)',
          color: isUser ? '#fff' : 'var(--text)',
          border: isUser ? 'none' : '1px solid var(--border)',
          fontSize: '15px',
          lineHeight: '1.55',
          whiteSpace: isUser ? 'pre-wrap' : 'normal',
          wordBreak: 'break-word',
          boxShadow: isUser
            ? '0 2px 12px rgba(255,0,51,0.3)'
            : '0 2px 10px rgba(0,0,0,0.35)',
        }}>
          {isUser ? message.content : <MarkdownRenderer content={message.content} />}
        </div>
        <span style={{
          fontSize: '11px',
          color: 'var(--muted)',
          marginTop: '4px',
          padding: '0 4px',
          alignSelf: isUser ? 'flex-end' : 'flex-start',
        }}>
          {isUser ? 'You' : 'JARVIS'} \u00B7 {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  )
}