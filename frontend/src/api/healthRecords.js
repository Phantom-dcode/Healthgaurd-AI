import api from './axios'
export const submitRecord  = d          => api.post('/health-records', d)
export const listRecords   = (params={})=> api.get('/health-records', { params })
export const getRecord     = id         => api.get(`/health-records/${id}`)
