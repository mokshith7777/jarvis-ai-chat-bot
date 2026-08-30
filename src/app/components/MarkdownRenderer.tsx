'use client'

import { useState, useEffect } from 'react'
import { unified } from 'unified'
import remarkParse from 'remark-parse'
import remarkGfm from 'remark-gfm'
import remarkRehype from 'remark-rehype'
import rehypeStringify from 'rehype-stringify'
import rehypeRaw from 'rehype-raw'

const processor = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkRehype, { allowDangerousHtml: true })
  .use(rehypeRaw)
  .use(rehypeStringify)

export function MarkdownRenderer({ content }: { content: string }) {
  const [html, setHtml] = useState('')

  useEffect(() => {
    processor.process(content).then((file) => {
      setHtml(String(file))
    })
  }, [content])

  return <div className="jarvis-md" dangerouslySetInnerHTML={{ __html: html }} />
}