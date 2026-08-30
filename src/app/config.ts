export const API_BASE = 'https://jarvis-ai.streamjarvis7.workers.dev'

export const MODEL_OPTIONS = [
  { id: 'Jarvis Pro', key: 'pro', description: 'Flagship reasoning', category: 'Flagship' },
  { id: 'Jarvis Lite', key: 'lite', description: 'Fast everyday assistant', category: 'Fast' },
  { id: 'Jarvis Ultron', key: 'qwen', description: 'Balanced general', category: 'Balanced' },
] as const

export const DEFAULT_MODEL = 'Jarvis Lite'