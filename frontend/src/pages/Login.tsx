import {
  useState,
} from 'react'

import type {
  FormEvent,
} from 'react'
import {
  Navigate,
  useNavigate,
} from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

export default function Login() {
  const navigate = useNavigate()

  const {
    login,
    isAuthenticated,
  } = useAuth()

  const [email, setEmail] =
    useState('')

  const [password, setPassword] =
    useState('')

  const [error, setError] =
    useState('')

  const [loading, setLoading] =
    useState(false)

  if (isAuthenticated) {
    return (
      <Navigate
        to="/dashboard"
        replace
      />
    )
  }

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault()

    setError('')

    if (!email.trim()) {
      setError(
        'Please enter your email address.',
      )
      return
    }

    if (!password) {
      setError(
        'Please enter your password.',
      )
      return
    }

    try {
      setLoading(true)

      await login(
        email.trim(),
        password,
      )

      navigate(
        '/dashboard',
        { replace: true },
      )
    } catch {
      setError(
        'Invalid email or password.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '24px',
        background: '#f4f6f8',
      }}
    >
      <section
        style={{
          width: '100%',
          maxWidth: '420px',
          padding: '32px',
          background: '#ffffff',
          borderRadius: '12px',
          boxShadow:
            '0 8px 30px rgba(0, 0, 0, 0.08)',
        }}
      >
        <h1
          style={{
            margin: '0 0 8px',
            fontSize: '28px',
          }}
        >
          Construction Management
        </h1>

        <p
          style={{
            margin: '0 0 24px',
            color: '#667085',
          }}
        >
          Sign in to your account
        </p>

        <form
          onSubmit={handleSubmit}
        >
          <div
            style={{
              marginBottom: '16px',
            }}
          >
            <label
              htmlFor="email"
              style={{
                display: 'block',
                marginBottom: '6px',
                fontWeight: 600,
              }}
            >
              Email
            </label>

            <input
              id="email"
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              placeholder="Enter your email"
              autoComplete="email"
              disabled={loading}
              style={{
                width: '100%',
                boxSizing: 'border-box',
                padding: '11px 12px',
                border:
                  '1px solid #d0d5dd',
                borderRadius: '8px',
                fontSize: '15px',
              }}
            />
          </div>

          <div
            style={{
              marginBottom: '16px',
            }}
          >
            <label
              htmlFor="password"
              style={{
                display: 'block',
                marginBottom: '6px',
                fontWeight: 600,
              }}
            >
              Password
            </label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Enter your password"
              autoComplete="current-password"
              disabled={loading}
              style={{
                width: '100%',
                boxSizing: 'border-box',
                padding: '11px 12px',
                border:
                  '1px solid #d0d5dd',
                borderRadius: '8px',
                fontSize: '15px',
              }}
            />
          </div>

          {error && (
            <div
              role="alert"
              style={{
                marginBottom: '16px',
                padding: '10px 12px',
                borderRadius: '8px',
                background: '#fef3f2',
                color: '#b42318',
                fontSize: '14px',
              }}
            >
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '12px',
              border: 'none',
              borderRadius: '8px',
              background: '#1d4ed8',
              color: '#ffffff',
              fontSize: '15px',
              fontWeight: 600,
              cursor: loading
                ? 'not-allowed'
                : 'pointer',
              opacity: loading ? 0.7 : 1,
            }}
          >
            {loading
              ? 'Signing in...'
              : 'Sign In'}
          </button>
        </form>
      </section>
    </main>
  )
}