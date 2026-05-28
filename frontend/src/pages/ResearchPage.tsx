import { useState } from 'react'
import axios from 'axios'
import { researchStart } from '../services/api'

type AgentResult = {
  agent_name: string
  output: string
  metadata?: Record<string, unknown> | null
}

type ResearchResponse = {
  topic: string
  results: AgentResult[]
  summary: string
  report_url?: string | null
}

function ResearchPage() {
  const [topic, setTopic] = useState('')
  const [enableWebSearch, setEnableWebSearch] = useState(true)
  const [includeDocuments, setIncludeDocuments] = useState(true)
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState<ResearchResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setLoading(true)
    setResponse(null)
    setErrorMessage(null)

    try {
      const { data } = await researchStart({ topic, enable_web_search: enableWebSearch, include_documents: includeDocuments })
      setResponse(data)
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response?.data?.detail) {
          setErrorMessage(error.response.data.detail)
        } else if (error.response) {
          setErrorMessage(
            `Backend returned ${error.response.status} ${error.response.statusText}. ${JSON.stringify(error.response.data)}`
          )
        } else {
          setErrorMessage(`Network error: ${error.message}. Verify the backend URL and that the service is running.`)
        }
      } else {
        setErrorMessage('Failed to start research workflow. Please check your backend configuration.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="space-y-6">
      <header className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <h2 className="text-3xl font-semibold">Research Topic</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300">Enter a topic and run a multi-agent research workflow with optional web search and document context.</p>
      </header>

      <form onSubmit={handleSubmit} className="space-y-6 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <div className="space-y-4">
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">Research topic</label>
          <input
            value={topic}
            onChange={(event) => setTopic(event.target.value)}
            placeholder="e.g. Future of AI in climate research"
            className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-sky-400 dark:focus:ring-sky-900"
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="flex items-center gap-3 rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4 dark:border-slate-700 dark:bg-slate-900">
            <input type="checkbox" checked={enableWebSearch} onChange={() => setEnableWebSearch((prev) => !prev)} className="h-5 w-5 rounded-md text-sky-600" />
            <span className="text-sm text-slate-700 dark:text-slate-300">Enable web search agent</span>
          </label>

          <label className="flex items-center gap-3 rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4 dark:border-slate-700 dark:bg-slate-900">
            <input type="checkbox" checked={includeDocuments} onChange={() => setIncludeDocuments((prev) => !prev)} className="h-5 w-5 rounded-md text-sky-600" />
            <span className="text-sm text-slate-700 dark:text-slate-300">Include uploaded documents</span>
          </label>
        </div>

        <button
          type="submit"
          disabled={!topic.trim() || loading}
          className="inline-flex items-center justify-center rounded-3xl bg-sky-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Running agents...' : 'Start research'}
        </button>
      </form>

      {errorMessage && (
        <section className="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-900 shadow-sm dark:border-red-900/60 dark:bg-red-950/30 dark:text-red-100">
          <h3 className="text-xl font-semibold">Research failed</h3>
          <p className="mt-3 text-sm leading-6">{errorMessage}</p>
        </section>
      )}

      {response && (
        <section className="space-y-5 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
          <div>
            <p className="text-sm font-medium uppercase tracking-wide text-sky-600 dark:text-sky-400">{response.topic}</p>
            <h3 className="mt-1 text-xl font-semibold">Research output</h3>
          </div>

          <article className="rounded-2xl border border-slate-200 bg-slate-50 p-5 dark:border-slate-800 dark:bg-slate-950">
            <h4 className="text-base font-semibold">Summary</h4>
            <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-700 dark:text-slate-200">{response.summary}</p>
          </article>

          <div className="space-y-4">
            {response.results.map((result) => (
              <article key={result.agent_name} className="rounded-2xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
                <h4 className="text-base font-semibold">{result.agent_name}</h4>
                <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-700 dark:text-slate-200">{result.output}</p>
              </article>
            ))}
          </div>
        </section>
      )}
    </section>
  )
}

export default ResearchPage
