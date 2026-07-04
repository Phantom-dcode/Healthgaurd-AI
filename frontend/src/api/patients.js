import api from './axios'
export const getMyProfile    = ()  => api.get('/patients/me')
export const updateMyProfile = d   => api.put('/patients/me', d)
export const listPatients    = ()  => api.get('/patients')
export const getPatient      = id  => api.get(`/patients/${id}`)
