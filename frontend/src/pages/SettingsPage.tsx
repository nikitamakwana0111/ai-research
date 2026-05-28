import { useState } from 'react'
import { setApiBaseUrl } from '../services/api'
import { useLocalStorage } from '../hooks/useLocalStorage'

function SettingsPage() {
  const [apiBase, setApiBase] = useLocalStorage('apiBaseUrl', import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1')
  const [message, setMessage] = useState('')

  const handleSave = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setApiBase(apiBase)
    setApiBaseUrl(apiBase)
    setMessage('Backend URL saved. The app will use this value immediately. Reload if a page still shows the old backend.')
  }

  return (
    <section className="space-y-6">
      <header className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <h2 className="text-3xl font-semibold">Settings</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300">Configure API endpoints and inspect frontend environment details.</p>
      </header>

      <form onSubmit={handleSave} className="space-y-6 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <div className="space-y-4">
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">Backend API Base URL</label>
          <input
            value={apiBase}
            onChange={(event) => setApiBase(event.target.value)}
            className="w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-sky-500 focus:ring-2 focus:ring-sky-200 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100 dark:focus:border-sky-400 dark:focus:ring-sky-900"
          />
        </div>

        <button type="submit" className="inline-flex items-center justify-center rounded-3xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-700">
          Save settings
        </button>
      </form>

      {message && <p className="rounded-3xl bg-slate-50 p-4 text-slate-700 shadow-sm dark:bg-slate-900 dark:text-slate-200">{message}</p>}
    </section>
  )
}

export default SettingsPage
