import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({ baseURL: BASE, timeout: 15000 })

// ── Request: attach Bearer token ─────────────────────────────
api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('access_token')
  if (token) cfg.headers.Authorization = `Bearer ${token}`
  return cfg
})

// ── Response: auto-refresh on 401 ────────────────────────────
let refreshing = false
let queue = []

api.interceptors.response.use(
  res => res,
  async err => {
    const original = err.config
    if (err.response?.status === 401 && !original._retry) {
      if (refreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject })
        }).then(token => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        })
      }
      original._retry = true
      refreshing = true
      try {
        const refresh = localStorage.getItem('refresh_token')
        if (!refresh) throw new Error('No refresh token')
        const { data } = await axios.post(`${BASE}/auth/refresh`, { refresh_token: refresh })
        const newToken = data.data.access_token
        localStorage.setItem('access_token',  newToken)
        localStorage.setItem('refresh_token', data.data.refresh_token)
        queue.forEach(p => p.resolve(newToken))
        queue = []
        original.headers.Authorization = `Bearer ${newToken}`
        return api(original)
      } catch {
        queue.forEach(p => p.reject())
        queue = []
        localStorage.clear()
        window.location.href = '/login'
      } finally {
        refreshing = false
      }
    }
    return Promise.reject(err)
  }
)

export default api
