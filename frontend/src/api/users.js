import api from './axios'
export const listUsers      = ()  => api.get('/users')
export const deactivateUser = id  => api.patch(`/users/${id}/deactivate`)
export const deleteUser     = id  => api.delete(`/users/${id}`)
export const updateMe       = d   => api.put('/users/me', d)
