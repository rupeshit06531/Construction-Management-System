import type { ReactNode } from 'react'

import { useAuth } from '../../context/AuthContext'


interface TopbarProps {
  title?: string
  subtitle?: string
  actions?: ReactNode
}


function Topbar({
  title = 'Dashboard',
  subtitle = 'Construction Management System',
  actions,
}: TopbarProps) {

  const { user } = useAuth()


  const fullName =
    user
      ? `${user.first_name} ${user.last_name}`.trim()
      : 'User'


  const role =
    user?.role || 'Guest'


  const initials =
    user
      ? `${user.first_name?.[0] || ''}${user.last_name?.[0] || ''}`
          .toUpperCase()
      : 'U'


  return (
    <header className="topbar">

      <div className="topbar-heading">
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>


      <div className="topbar-actions">

        {actions}


        <button
          type="button"
          className="topbar-icon-button"
          aria-label="Notifications"
        >
          !
        </button>


        <div className="topbar-user">

          <div className="topbar-avatar">
            {initials}
          </div>


          <div className="topbar-user-info">

            <strong>
              {fullName}
            </strong>

            <span>
              {role}
            </span>

          </div>

        </div>

      </div>

    </header>
  )
}


export default Topbar