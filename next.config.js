/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  // Use WASM fallback for platforms without native SWC binary
  swcMinify: false,
  experimental: {
    forceSwcTransforms: true,
  },
}

module.exports = nextConfig
