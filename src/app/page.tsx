'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { useAuth } from './providers'
import { Logo } from './components/Logo'
import { Header } from './components/Header'
import { Message } from './components/Message'
import { MessageList } from './components/MessageList'
import { InputBar } from './components/InputBar'
import { ModelInfo } from './components/ModelInfo'
import { QuotaBar } from './components/QuotaBar'
import { ErrorBanner } from './components/ErrorBanner'
import { ActionButtons } from './components/ActionButtons'
import { MODEL_OPTIONS, DEFAULT_MODEL, API_BASE } from './config'

interface MessageType {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export default function Home() {
  const { user, loading: authLoading, signIn, signOutUser } = useAuth()
  const [messages, setMessages] = useState<MessageType[]>([])
  const [input, setInput] = useState('')
  const [selectedModel, setSelectedModel] = useState(DEFAULT_MODEL)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [quotaRemaining, setQuotaRemaining] = useState<number | null>(null)
  const abortControllerRef = useRef<AbortController | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, isLoading, scrollToBottom])

  // Fetch quota when user signs in
  useEffect(() => {
    if (!user) {
      setQuotaRemaining(null)
      return
    }
    let cancelled = false
    const fetchQuota = async () => {
      try {
        const token = await user.getIdToken()
        const res = await fetch(`${API_BASE}/quota`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        if (res.ok) {
          const data = await res.json()
          if (!cancelled && typeof data.remaining === 'number') {
            setQuotaRemaining(data.remaining)
          }
        }
      } catch (e) {
        // ignore
      }
    }
    fetchQuota()
    return () => { cancelled = true }
  }, [user])

  const handleSend = async () => {
    if (!input.trim() || isLoading || !user) return
    if (quotaRemaining !== null && quotaRemaining <= 0) return

    const userMessage: MessageType = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString(),
    }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setInput('')
    await generateResponse(newMessages)
  }

  const handleRegenerate = async () => {
    if (isLoading || !user) return
    const lastAssistantIdx = [...messages].findLastIndex(m => m.role === 'assistant')
    if (lastAssistantIdx === -1) return
    const newMessages = messages.slice(0, lastAssistantIdx)
    setMessages(newMessages)
    await generateResponse(newMessages)
  }

  const handleClear = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    setMessages([])
    setError(null)
    setIsLoading(false)
  }

  const handleStop = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
      abortControllerRef.current = null
    }
    setIsLoading(false)
  }

  const generateResponse = async (currentMessages: MessageType[]) => {
    const lastUserMsg = [...currentMessages].reverse().find(m => m.role === 'user')
    if (!lastUserMsg || !user) return

    setIsLoading(true)
    setError(null)
    const controller = new AbortController()
    abortControllerRef.current = controller

    try {
      const token = await user.getIdToken()
      const modelConfig = MODEL_OPTIONS.find(m => m.id === selectedModel) || MODEL_OPTIONS[0]
      
      const res = await fetch(`${API_BASE}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          model: modelConfig.key,
          messages: currentMessages
            .filter(m => m.role === 'user' || m.role === 'assistant')
            .map(m => ({ role: m.role, content: m.content })),
          stream: false,
          temperature: 0.7,
          max_tokens: 1024,
        }),
        signal: controller.signal,
      })

      const quotaHeader = res.headers.get('X-Quota-Remaining')
      if (quotaHeader !== null) {
        setQuotaRemaining(parseInt(quotaHeader, 10))
      }

      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.error || `Backend error: ${res.status}`)
      }

      const data = await res.json()
      const content = data.choices?.[0]?.message?.content || 'No response.'
      
      const assistantMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content,
        timestamp: new Date().toISOString(),
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (e) {
      if (e instanceof DOMException && e.name === 'AbortError') return
      setError(e instanceof Error ? e.message : 'Failed to get response.')
      console.error(e)
    } finally {
      setIsLoading(false)
      abortControllerRef.current = null
    }
  }

  if (authLoading) {
    return (
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        color: 'var(--gold)',
      }}>
        Loading JARVIS\u2026
      </div>
    )
  }

  return (
    <>
      {!user ? (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          gap: '24px',
        }}>
          <Logo kind="logo" size={88} />
          <h1 style={{
            color: 'var(--gold)',
            fontSize: '28px',
            textShadow: '0 0 18px rgba(255,0,51,0.25)',
          }}>
            JARVIS AI
          </h1>
          <p style={{ color: 'var(--muted)' }}>Sign in with Google to start chatting</p>
          <button
            onClick={signIn}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '12px 24px',
              borderRadius: '8px',
              background: '#ffffff',
              color: '#1f1f1f',
              fontWeight: 500,
              fontSize: '15px',
              border: '1px solid #dadce0',
              boxShadow: '0 1px 2px rgba(0,0,0,0.18)',
              cursor: 'pointer',
            }}
          >
            <svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true">
              <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z" />
              <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6.01C43.89 39.96 46.98 33.27 46.98 24.55z" />
              <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z" />
              <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6.01c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z" />
            </svg>
            Sign in with Google
          </button>
        </div>
      ) : (
        <div className="app-shell" style={{
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          maxWidth: '900px',
          margin: '0 auto',
        }}>
          <Header
            selectedModel={selectedModel}
            onModelChange={setSelectedModel}
            modelOptions={MODEL_OPTIONS}
            quotaRemaining={quotaRemaining}
            user={user}
            onSignOut={signOutUser}
          />
          <ModelInfo modelId={selectedModel} modelOptions={MODEL_OPTIONS} />
          {messages.length > 0 && (
            <ActionButtons
              isLoading={isLoading}
              onRegenerate={handleRegenerate}
              onClear={handleClear}
              onStop={handleStop}
              hasAssistantMessage={messages[messages.length - 1]?.role === 'assistant'}
            />
          )}
          {error && <ErrorBanner message={error} />}
          {quotaRemaining !== null && <QuotaBar remaining={quotaRemaining} />}
          <MessageList messages={messages} isLoading={isLoading} endRef={messagesEndRef} user={user} />
          <InputBar
            value={input}
            onChange={setInput}
            onSubmit={handleSend}
            disabled={isLoading || quotaRemaining === 0}
          />
        </div>
      )}
    </>
  )
}