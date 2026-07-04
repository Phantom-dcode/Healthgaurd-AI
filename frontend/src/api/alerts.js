import api from './axios'
export const listAlerts    = (params={})=> api.get('/alerts', { params })
export const updateAlert   = (id, d)   => api.patch(`/alerts/${id}`, d)
export const alertsSummary = ()        => api.get('/alerts/summary')
