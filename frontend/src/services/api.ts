import axios from 'axios'

const STORAGE_KEY = 'apiBaseUrl'

function getSavedApiBaseUrl(): string | null {
  if (typeof window === 'undefined') return null
  try {
    const item = window.localStorage.getItem(STORAGE_KEY)
    if (!item) return null

    try {
      return JSON.parse(item) as string
    } catch {
      return item
    }
  } catch {
    return null
  }
}

function getDefaultApiBaseUrl(): string {
  return import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'
}

export function getApiBaseUrl(): string {
  return getSavedApiBaseUrl() || getDefaultApiBaseUrl()
}

const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 30000,
})

export function setApiBaseUrl(baseURL: string) {
  api.defaults.baseURL = baseURL

  if (typeof window === 'undefined') return

  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(baseURL))
  } catch {
    // ignore storage write errors
  }
}

export const researchStart = (payload: { topic: string; enable_web_search: boolean; include_documents: boolean }) =>
  api.post('/research/start', payload)

export const generateReport = (payload: { topic: string; report_format: string }) =>
  api.post('/research/report', payload)

export const chatQuery = (payload: { message: string; session_id?: string }) => api.post('/chat/query', payload)

export const uploadDocument = (formData: FormData) => api.post('/documents/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } })

export const healthCheck = () => {
  const baseURL = String(api.defaults.baseURL || getApiBaseUrl()).replace(/\/+$/, '')
  const healthURL = baseURL.endsWith('/api/v1') ? `${baseURL.slice(0, -'/api/v1'.length)}/health` : `${baseURL}/health`
  return axios.get(healthURL, { timeout: 10000 })
}

export default api
