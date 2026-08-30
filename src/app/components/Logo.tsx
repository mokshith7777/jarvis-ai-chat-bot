'use client'

import { useState } from 'react'

export function Logo({ kind, size = 32 }: { kind: 'logo' | 'avatar'; size?: number }) {
  const [src, setSrc] = useState(`/${kind}.png`)

  if (src) {
    return (
      <img
        src={src}
        alt={kind === 'logo' ? 'JARVIS' : 'JARVIS avatar'}
        width={size}
        height={size}
        style={{
          width: size,
          height: size,
          display: 'block',
          borderRadius: kind === 'avatar' ? '50%' : 0,
          objectFit: 'contain',
        }}
        onError={() => {
          if (src === `/${kind}.png`) setSrc(`/${kind}.svg`)
          else if (src === `/${kind}.svg`) setSrc(`/${kind}.jpg`)
          else setSrc('')
        }}
      />
    )
  }

  return <LogoSvg size={size} glow />
}

function LogoSvg({ size = 32, glow = true }: { size?: number; glow?: boolean }) {
  const center = size / 2
  const radius = 0.47 * size
  const spokes = Array.from({ length: 16 }, (_, i) => {
    const angle = (i * Math.PI * 2) / 16 - Math.PI / 2
    return {
      x1: center + Math.cos(angle) * size * 0.13,
      y1: center + Math.sin(angle) * size * 0.13,
      x2: center + Math.cos(angle) * radius,
      y2: center + Math.sin(angle) * radius,
    }
  })

  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      style={glow ? { filter: 'drop-shadow(0 0 7px rgba(10,74,92,0.6)) drop-shadow(0 0 3px rgba(212,175,55,0.5))' } : undefined}
    >
      <defs>
        <radialGradient id="jm-core" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#fff7d6" />
          <stop offset="40%" stopColor="#f5d77a" />
          <stop offset="100%" stopColor="#8a6d1f" />
        </radialGradient>
        <linearGradient id="jm-ring" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#f5d77a" />
          <stop offset="55%" stopColor="#d4af37" />
          <stop offset="100%" stopColor="#0a4a5c" />
        </linearGradient>
        <radialGradient id="jm-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="rgba(10,74,92,0.35)" />
          <stop offset="100%" stopColor="rgba(10,74,92,0)" />
        </radialGradient>
      </defs>
      <circle cx={center} cy={center} r={radius} fill="url(#jm-glow)" />
      <path
        d={`M ${center - radius} ${center} A ${radius} ${radius} 0 0 1 ${center + radius} ${center}`}
        fill="none"
        stroke="url(#jm-ring)"
        strokeWidth={Math.max(1, 0.05 * size)}
        strokeLinecap="round"
      />
      <path
        d={`M ${center - radius} ${center} A ${radius} ${radius} 0 0 0 ${center + radius} ${center}`}
        fill="none"
        stroke="rgba(212,175,55,0.35)"
        strokeWidth={Math.max(0.8, 0.03 * size)}
        strokeDasharray={`${0.04 * size} ${0.05 * size}`}
      />
      <g stroke="rgba(245,215,122,0.4)" strokeWidth={Math.max(0.5, 0.018 * size)}>
        {spokes.map((s, i) => (
          <line key={i} x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} />
        ))}
      </g>
      {[0.94, 0.7, 0.46].map((scale, i) => (
        <circle
          key={i}
          cx={center}
          cy={center}
          r={size * scale * 0.5}
          fill="none"
          stroke="url(#jm-ring)"
          strokeWidth={Math.max(0.8, 0.03 * size)}
          strokeDasharray={i === 1 ? `${0.1 * size} ${0.05 * size}` : undefined}
          opacity={0.9}
        />
      ))}
      <path
        d={`M ${center} ${center - 0.55 * radius} L ${center + 0.16 * radius} ${center - 0.28 * radius} L ${center} ${center - 0.12 * radius} L ${center - 0.16 * radius} ${center - 0.28 * radius} Z`}
        fill="rgba(245,215,122,0.85)"
        stroke="rgba(255,247,214,0.9)"
        strokeWidth={Math.max(0.4, 0.012 * size)}
      />
      <circle cx={center} cy={center} r={0.17 * size} fill="url(#jm-core)" />
      <circle cx={center} cy={center} r={0.17 * size} fill="none" stroke="rgba(255,247,214,0.9)" strokeWidth={Math.max(0.5, 0.014 * size)} />
    </svg>
  )
}
