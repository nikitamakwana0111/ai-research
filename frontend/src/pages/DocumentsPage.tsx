import { FormEvent, useState } from 'react'
import axios from 'axios'
import { uploadDocument } from '../services/api'

function DocumentsPage() {
  const [file, setFile] = useState<File | null>(null)
  const [status, setStatus] = useState<string | null>(null)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    setStatus('Uploading PDF…')

    try {
      const { data } = await uploadDocument(formData)
      setStatus(`Uploaded ${data.filename}. Document ID: ${data.document_id}`)
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        setStatus(`Upload failed. ${error.response.data.detail}`)
      } else {
        setStatus('Upload failed. Verify backend is reachable and .env is configured.')
      }
    }
  }

  return (
    <section className="space-y-6">
      <header className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <h2 className="text-3xl font-semibold">PDF Upload</h2>
        <p className="mt-2 text-slate-600 dark:text-slate-300">Add documents to your knowledge base and power document-aware AI chat sessions.</p>
      </header>

      <form onSubmit={handleSubmit} className="space-y-6 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-200">Upload a PDF</label>
        <input
          type="file"
          accept="application/pdf"
          onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          className="block w-full rounded-3xl border border-slate-300 bg-slate-50 px-4 py-3 text-slate-900 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100"
        />

        <button
          type="submit"
          disabled={!file}
          className="inline-flex items-center justify-center rounded-3xl bg-sky-600 px-6 py-3 text-sm font-semibold text-white transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Upload document
        </button>
      </form>

      {status && (
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5 text-slate-700 shadow-sm dark:border-slate-800 dark:bg-slate-900 dark:text-slate-200">
          {status}
        </div>
      )}
    </section>
  )
}

export default DocumentsPage
