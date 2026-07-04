import api from './axios'
export const createReport = d  => api.post('/reports', d)
export const listReports  = () => api.get('/reports')
