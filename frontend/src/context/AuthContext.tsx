import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'


import {
  clearAuthTokens,
  getAccessToken,
  setAuthTokens,
} from '../utils/auth'


import {
  getCurrentUser,
  login as loginApi,
  type AuthUser,
} from '../api/accounts'


interface AuthContextValue {
  user: AuthUser | null
  isAuthenticated: boolean
  login: (
    email: string,
    password: string,
  ) => Promise<void>
  logout: () => void
}


const AuthContext =
  createContext<AuthContextValue | undefined>(
    undefined,
  )


interface AuthProviderProps {
  children: ReactNode
}


export function AuthProvider({
  children,
}: AuthProviderProps) {

  const [user, setUser] =
    useState<AuthUser | null>(null)


  const [isAuthenticated, setIsAuthenticated] =
    useState<boolean>(
      Boolean(getAccessToken()),
    )


  useEffect(() => {

    const restoreUser = async () => {

      const token = getAccessToken()

      if (!token) {
        return
      }


      try {

        const currentUser =
          await getCurrentUser()

        setUser(currentUser)

      } catch {

        clearAuthTokens()

        setUser(null)

        setIsAuthenticated(false)
      }
    }


    restoreUser()

  }, [])


  const login = async (
    email: string,
    password: string,
  ): Promise<void> => {

    const response =
      await loginApi({
        email,
        password,
      })


    setAuthTokens(
      response.access,
      response.refresh,
    )


    setUser(response.user)

    setIsAuthenticated(true)
  }


  const logout = (): void => {

    clearAuthTokens()

    setUser(null)

    setIsAuthenticated(false)
  }


  const value = useMemo(
    () => ({
      user,
      isAuthenticated,
      login,
      logout,
    }),

    [
      user,
      isAuthenticated,
    ],
  )


  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}


export function useAuth(): AuthContextValue {

  const context =
    useContext(AuthContext)


  if (!context) {
    throw new Error(
      'useAuth must be used inside AuthProvider.',
    )
  }


  return context
}