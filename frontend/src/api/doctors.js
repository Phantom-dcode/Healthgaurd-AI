import api from './axios'
export const getMyProfile    = ()  => api.get('/doctors/me')
export const updateMyProfile = d   => api.put('/doctors/me', d)
export const getMyPatients   = ()  => api.get('/doctors/my-patients')
export const assignPatient   = d   => api.post('/doctors/assign-patient', d)
