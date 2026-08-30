'use client'

interface ModelInfoProps {
  modelId: string
  modelOptions: { id: string; key: string; description: string; category: string }[]
}

export function ModelInfo({ modelId, modelOptions }: ModelInfoProps) {
  const model = modelOptions.find(m => m.id === modelId)
  if (!model) return null

  return (
    <div style={{
      padding: '6px 24px',
      fontSize: '12px',
      color: 'var(--muted)',
      borderBottom: '1px solid var(--border)',
      background: 'var(--surface)',
    }}>
      {model.id} \u00B7 {model.description}
    </div>
  )
}