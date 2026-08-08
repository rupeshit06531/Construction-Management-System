import axios from 'axios'

import {
  clearAuthTokens,
  getAccessToken,
  getRefreshToken,
  setAuthTokens,
} from '../utils/auth'

import {
  refreshAccessToken,
} from './token'


const apiClient = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ||
    'http://127.0.0.1:8000/api',

  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },

  timeout: 15000,
})


apiClient.interceptors.request.use(
  (config) => {
    const accessToken = getAccessToken()

    if (accessToken) {
      config.headers.Authorization =
        `Bearer ${accessToken}`
    }

    return config
  },

  (error) => {
    return Promise.reject(error)
  },
)


apiClient.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config

    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true

      const refreshToken =
        getRefreshToken()

      if (refreshToken) {
        try {
          const response =
            await refreshAccessToken(
              refreshToken,
            )

          setAuthTokens(
            response.access,
            refreshToken,
          )

          originalRequest.headers.Authorization =
            `Bearer ${response.access}`

          return apiClient(
            originalRequest,
          )
        } catch {
          clearAuthTokens()
        }
      }
    }

    return Promise.reject(error)
  },
)


export default apiClient