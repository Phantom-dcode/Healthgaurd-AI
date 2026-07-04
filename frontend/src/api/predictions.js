import api from './axios'
export const runPrediction    = (d={}) => api.post('/predictions/predict', d)
export const listPredictions  = ()     => api.get('/predictions')
export const latestPrediction = ()     => api.get('/predictions/latest')
