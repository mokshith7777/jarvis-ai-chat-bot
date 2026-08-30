import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'JARVIS Chat',
  description: 'JARVIS AI Chat Assistant',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preload" as="video" href="/ambient.webm" type="video/webm" />
        <link rel="icon" href="/logo.png" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
      </head>
      <body>
        {/* 3D Reactor Background */}
        <ThreeJSRocket aria-hidden="true" />

        {children}
      </body>
    </html>
  );
}
