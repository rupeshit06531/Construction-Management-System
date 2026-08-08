import { useNavigate } from 'react-router-dom'

import { useAuth } from '../../context/AuthContext'


type SidebarItem = {
  label: string
  icon: string
  path: string
  roles: string[]
}


const sidebarItems: SidebarItem[] = [
  {
    label: 'Dashboard',
    icon: 'D',
    path: '/dashboard',
    roles: [
      'SUPER_ADMIN',
      'ADMIN',
      'MANAGER',
      'ENGINEER',
      'WORKER',
      'CUSTOMER',
    ],
  },
  {
    label: 'Projects',
    icon: 'P',
    path: '/projects',
    roles: [
      'SUPER_ADMIN',
      'ADMIN',
      'MANAGER',
      'ENGINEER',
    ],
  },
]


function Sidebar() {
  const navigate = useNavigate()

  const { user } = useAuth()

  const role = user?.role || 'CUSTOMER'


  const visibleItems = sidebarItems.filter(
    (item) => item.roles.includes(role),
  )


  return (
    <aside
      style={{
        width: '260px',
        minHeight: '100vh',
        background: '#111827',
        color: '#ffffff',
        display: 'flex',
        flexDirection: 'column',
        flexShrink: 0,
      }}
    >
      <div
        style={{
          height: '72px',
          display: 'flex',
          alignItems: 'center',
          padding: '0 24px',
          borderBottom: '1px solid #1f2937',
        }}
      >
        <div>
          <div
            style={{
              fontSize: '18px',
              fontWeight: 700,
            }}
          >
            Construction CMS
          </div>

          <div
            style={{
              marginTop: '3px',
              fontSize: '11px',
              color: '#9ca3af',
            }}
          >
            Management System
          </div>
        </div>
      </div>


      <nav
        aria-label="Main navigation"
        style={{
          flex: 1,
          padding: '20px 12px',
        }}
      >
        <div
          style={{
            padding: '0 12px 10px',
            fontSize: '11px',
            color: '#6b7280',
          }}
        >
          Main Menu
        </div>


        {visibleItems.map((item, index) => (
          <button
            key={item.label}
            type="button"
            onClick={() => navigate(item.path)}
            style={{
              width: '100%',
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '11px 12px',
              marginBottom: '4px',
              border: 'none',
              borderRadius: '8px',
              background:
                index === 0
                  ? '#2563eb'
                  : 'transparent',
              color: '#ffffff',
              cursor: 'pointer',
            }}
          >
            <span>
              {item.icon}
            </span>

            <span>
              {item.label}
            </span>
          </button>
        ))}
      </nav>


      <div
        style={{
          padding: '16px',
          borderTop: '1px solid #1f2937',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            padding: '10px',
            borderRadius: '8px',
            background: '#1f2937',
          }}
        >
          <div
            style={{
              width: '34px',
              height: '34px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '50%',
              background: '#2563eb',
              fontSize: '13px',
              fontWeight: 700,
            }}
          >
            {(user?.first_name?.[0] || 'U').toUpperCase()}
          </div>

          <div>
            <div
              style={{
                fontSize: '13px',
                fontWeight: 600,
              }}
            >
              {user
                ? `${user.first_name} ${user.last_name}`.trim()
                : 'User'}
            </div>

            <div
              style={{
                marginTop: '2px',
                fontSize: '11px',
                color: '#9ca3af',
              }}
            >
              {user?.role || 'Guest'}
            </div>
          </div>
        </div>
      </div>

    </aside>
  )
}


export default Sidebar