import apiClient from './client'


interface RefreshTokenResponse {
  access: string
}


export const refreshAccessToken = async (
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