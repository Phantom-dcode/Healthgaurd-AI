import api from './axios'
export const register   = d => api.post('/auth/register', d)
export const login      = d => api.post('/auth/login', d)
export const logout     = ()=> api.post('/auth/logout')
export const refresh    = d => api.post('/auth/refresh', d)
export const getMe      = ()=> api.get('/auth/me')
