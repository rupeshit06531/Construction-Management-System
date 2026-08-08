import apiClient from './client'

export interface LoginRequest {
  email: string
  password: string
}

export interface AuthUser {
  id: number
  username: string
  email: string
  role: string
  first_name: string
  last_name: string
}

export interface LoginResponse {
  refresh: string
  access: string
  user: AuthUser
}

export const login = async (
  credentials: LoginRequest,
): Promise<LoginResponse> => {
  const response = await apiClient.post<LoginResponse>(
    '/accounts/login/',
    credentials,
  )

  return response.data
}

export interface RefreshTokenRequest {
  refresh: string
}


export interface RefreshTokenResponse {
  access: string
}


export const refreshToken = async (
  refresh: string,
): Promise<RefreshTokenResponse> => {
  const response =
    await apiClient.post<RefreshTokenResponse>(
      '/accounts/token/refresh/',
      {
        refresh,
      },
    )

  return response.data
}

export const getCurrentUser = async (): Promise<AuthUser> => {
  const response =
    await apiClient.get<AuthUser>(
      '/accounts/me/',
    )

  return response.data
}