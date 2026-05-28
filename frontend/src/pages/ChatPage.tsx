import { FormEvent, useState } from 'react'
import { chatQuery } from '../services/api'

function ChatPage() {
  const [message, setMessage] = useState('')
  const [response, setResponse] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setResponse(null)

    try {
      const { data } = await chatQuery({ message })
      setResponse(JSON.stringify(data, null, 2))
    } catch (error) {
      setResponse('Chat query failed. Ensure backend is running and connected.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="space-y-6">
      <header className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <h2 className="text-3xl font-semibold">Chat with documents</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300">Ask questions about your uploaded PDFs and receive sourced answers from the RAG pipeline.</p>
      </header>

      <form onSubmit={handleSubmit} className="space-y-6 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask a research question..."
          className="min-h-[160px] w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-4 text-slate-900 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-sky-400 dark:focus:ring-sky-900"
        />

        <button
          type="submit"
          disabled={!message.trim() || loading}
          className="inline-flex items-center justify-center rounded-3xl bg-sky-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Querying…' : 'Send question'}
        </button>
      </form>

      {response && (
        <section className="rounded-3xl border border-slate-200 bg-slate-50 p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <h3 className="text-xl font-semibold">AI chat response</h3>
          <pre className="mt-4 whitespace-pre-wrap text-sm leading-6 text-slate-700 dark:text-slate-200">{response}</pre>
        </section>
      )}
    </section>
  )
}

export default ChatPage
