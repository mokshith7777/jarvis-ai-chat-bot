---
version: alpha
name: JARVIS AI
description: Cinematic AI assistant — midnight depths, arc-reactor gold, neural cyan, alert neon. Futuristic, precise, alive.
colors:
  primary: "#0B1421"          # midnight - deep space bg
  secondary: "#1A1D24"        # charcoal - surfaces
  tertiary: "#E8C54A"         # gold - arc reactor, primary actions
  gold-deep: "#D4AF37"        # gold-deep - reactor rings, hover
  gold-soft: "rgba(232,197,74,0.12)"  # gold glow
  neon: "#FF0033"             # neon - alerts, accents
  cyan: "#1EC8E6"             # cyan - neural links, data
  cyan-deep: "#0A3A4A"        # cyan-deep - subtle glows
  neon-soft: "rgba(255,0,51,0.14)"   # neon glow
  border: "rgba(255,0,51,0.22)"      # borders
  surface-2: "#161B26"        # elevated surfaces
  text: "#EAF6F8"             # primary text
  muted: "#8AA0B0"            # secondary text
  on-primary: "#EAF6F8"
  on-tertiary: "#0B1421"
typography:
  h1:
    fontFamily: "Orbitron, Rajdhani, system-ui, sans-serif"
    fontSize: "4.5rem"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  h2:
    fontFamily: "Orbitron, Rajdhani, system-ui, sans-serif"
    fontSize: "2.5rem"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  body-lg:
    fontFamily: "Space Grotesk, Inter, system-ui, sans-serif"
    fontSize: "1.25rem"
    lineHeight: 1.6
  label-caps:
    fontFamily: "Space Grotesk, Inter, system-ui, sans-serif"
    fontSize: "0.7rem"
    fontWeight: 600
    letterSpacing: "0.12em"
    textTransform: "uppercase"
  hud-mono:
    fontFamily: "JetBrains Mono, Fira Code, monospace"
    fontSize: "0.85rem"
    lineHeight: 1.5
    letterSpacing: "0.02em"
rounded:
  sm: 4px
  md: 10px
  lg: 18px
  xl: 28px
  full: 9999px
spacing:
  xs: 6px
  sm: 12px
  md: 20px
  lg: 32px
  xl: 56px
  xxl: 96px
elevation:
  glow-sm: "0 0 12px rgba(232,197,74,0.25)"
  glow-md: "0 0 28px rgba(232,197,74,0.35), 0 0 60px rgba(30,200,230,0.18)"
  glow-lg: "0 0 60px rgba(255,0,51,0.4), 0 0 120px rgba(232,197,74,0.25)"
  vignette: "radial-gradient(ellipse at center, transparent 35%, rgba(4,4,6,0.92) 100%)"
components:
  reactor-core:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.full}"
    boxShadow: "{elevation.glow-md}"
  reactor-ring:
    borderColor: "{colors.gold-deep}"
    borderWidth: "3px"
    rounded: "{rounded.full}"
  hud-bracket:
    borderColor: "{colors.tertiary}"
    borderWidth: "3px"
    rounded: "{rounded.sm}"
  button-primary:
    backgroundColor: "transparent"
    textColor: "{colors.tertiary}"
    borderColor: "{colors.tertiary}"
    borderWidth: "2px"
    rounded: "{rounded.md}"
    padding: "14px 32px"
  button-primary-hover:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
  card-glass:
    backgroundColor: "rgba(26,29,36,0.7)"
    backdropFilter: "blur(16px)"
    borderColor: "rgba(232,197,74,0.18)"
    borderWidth: "1px"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
---

## Overview

JARVIS AI is Tony Stark's dream made real — an AI assistant that feels like a neural extension. The visual identity centers on the **arc reactor**: concentric gold rings, a pulsing core, 16 spokes radiating intelligence. Around it, a HUD aesthetic — corner brackets, scanlines, neural-web connections, live telemetry. Colors are midnight (#0B1421) + charcoal (#1A1D24) for depth, **gold (#E8C54A)** for the reactor soul, **cyan (#1EC8E6)** for neural data streams, **neon (#FF0033)** for urgent signals. Everything glows, breathes, responds. No flat UI — every surface has depth, every element has state.

## Colors

- **Primary (#0B1421)**: Infinite midnight. Page bg, deepest space.
- **Secondary (#1A1D24)**: Charcoal. Cards, elevated surfaces.
- **Tertiary / Accent (#E8C54A)**: Arc reactor gold. The *only* high-emphasis driver — logo, primary CTAs, reactor rings, active states. Use sparingly; its rarity is its power.
- **Cyan (#1EC8E6)**: Neural links, data flow, secondary info, HUD readouts.
- **Neon (#FF0033)**: Alerts, warnings, quota-exceeded, critical CTAs. High contrast, demands attention.
- **Gold-deep (#D4AF37)**: Reactor ring variants, hover states.
- **Muted (#8AA0B0)**: Supporting text, timestamps, disabled states.
- **Text (#EAF6F8)**: Primary content, high readability on midnight.

Gradients are **never decorative** — they map to physical light: reactor core → gold radial, neural link → cyan linear, alert → neon pulse.

## Typography

- **Display (Orbitron/Rajdhani)**: Geometric, engineered, squared curves — feels like spacecraft markings. Used for "JARVIS", major numbers, HUD headers. Tight tracking (-0.03em) for density.
- **UI (Space Grotesk)**: Technical humanist, slightly condensed. Body, labels, buttons. Clean at small sizes.
- **Mono (JetBrains Mono)**: Telemetry, coordinates, code, timestamps. Ligatures off, tabular nums on.

Hierarchy is **scale + weight + color**, not font switching. H1 at 4.5rem gold, H2 at 2.5rem cyan, body at 1.25rem text.

## Layout

Spacing is a **6px baseline** (xs=6, sm=12, md=20, lg=32, xl=56, xxl=96). Sections breathe at xxl; components pack at md.

Grid: **12-col desktop, 6-col tablet, 4-col mobile**. Reactor always center-anchored; HUD brackets hug viewport corners.

## Elevation & Depth

Three glow tiers replace traditional shadows:
- **glow-sm**: Resting reactor, inactive cards
- **glow-md**: Active reactor, primary focus
- **glow-lg**: Critical alert, loading pulse

**Vignette** is mandatory on full-bleed surfaces — radial from center to midnight edges, 92% opacity at corners. Creates the "helmet visor" frame.

## Shapes

- **Reactor**: Perfect circles, full-radius. Rings at 1.0, 0.86, 0.72, 0.58, 0.44, 0.30, 0.16 × radius.
- **HUD brackets**: L-corners at 4.5% inset, 7.5% span, 3px stroke, 10px radius tips.
- **Cards**: 18px radius, glassmorphism with purpose (blur + border = depth cue).
- **Buttons**: 10px radius, border-only default, fill on hover.

## Components

- **reactor-core**: The soul. Gold fill, full-radius, pulse animation (0.8s ease-in-out infinite).
- **reactor-ring**: Stroke-only rings, gold-deep, dashed variants for telemetry.
- **hud-bracket**: Corner anchors, gold stroke, subtle glow. Never centered — always corners.
- **button-primary**: Border gold, text gold, transparent bg. Hover → fill gold, text midnight.
- **card-glass**: Charcoal glass, gold border at 18%, blur 16px. Content sits on this.

## Do's and Don'ts

- **Do** use token references (`{colors.tertiary}`) — single source of truth.
- **Do** animate with purpose: reactor pulse (breathing), scanline drift (alive), data ticker (live).
- **Do** respect `prefers-reduced-motion` — kill pulse, drop opacity to 0.03, static brackets.
- **Don't** add colors outside this palette — extend via `gold-warm`, `cyan-warm` tokens first.
- **Don't** use flat fills without glow/depth — everything lives in 3D space.
- **Don't** center body text — left-align UI, center only reactor & hero headlines.
- **Don't** use generic icons — every symbol is reactor-derived (spokes, brackets, rings).