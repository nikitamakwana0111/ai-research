import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1',
  timeout: 30000,
})

export const researchStart = (payload: { topic: string; enable_web_search: boolean; include_documents: boolean }) =>
  api.post('/research/start', payload)

export const generateReport = (payload: { topic: string; report_format: string }) =>
  api.post('/research/report', payload)

export const chatQuery = (payload: { message: string; session_id?: string }) => api.post('/chat/query', payload)

export const uploadDocument = (formData: FormData) => api.post('/documents/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } })

export default api
