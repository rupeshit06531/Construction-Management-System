import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'

import DashboardLayout from '../components/layout/DashboardLayout'
import { createProject } from '../api/projects'


function CreateProject() {

  const navigate = useNavigate()


  const [name, setName] = useState('')
  const [code, setCode] = useState('')
  const [description, setDescription] = useState('')
  const [client, setClient] = useState('')
  const [location, setLocation] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [budget, setBudget] = useState('')
  const [status, setStatus] = useState('ACTIVE')
  const [manager, setManager] = useState('')


  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')


  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {

    event.preventDefault()

    setError('')


    if (!name.trim()) {
      setError('Project name is required.')
      return
    }


    if (!code.trim()) {
      setError('Project code is required.')
      return
    }


    if (!client.trim()) {
      setError('Client name is required.')
      return
    }


    if (!location.trim()) {
      setError('Location is required.')
      return
    }


    if (!startDate) {
      setError('Start date is required.')
      return
    }


    if (!endDate) {
      setError('End date is required.')
      return
    }


    if (!budget) {
      setError('Budget is required.')
      return
    }


    if (!manager) {
      setError('Manager ID is required.')
      return
    }


    try {

      setLoading(true)


      const project = await createProject({
        name: name.trim(),
        code: code.trim(),
        description: description.trim(),
        client: client.trim(),
        location: location.trim(),
        start_date: startDate,
        end_date: endDate,
        budget,
        status,
        manager: Number(manager),
      })


      navigate(
        `/projects/${project.id}`,
        { replace: true },
      )

    } catch (requestError) {

      console.error(
        'Failed to create project',
        requestError,
      )

      setError(
        'Failed to create project. Please check the entered information.',
      )

    } finally {

      setLoading(false)

    }
  }


  return (
    <DashboardLayout>

      <section className="dashboard-page">

        <div className="page-header">

          <div>

            <h1>
              Create Project
            </h1>

            <p>
              Add a new construction project.
            </p>

          </div>

        </div>


        <form
          onSubmit={handleSubmit}
          style={{
            maxWidth: '800px',
            background: '#ffffff',
            padding: '24px',
            borderRadius: '10px',
            boxShadow:
              '0 2px 8px rgba(0, 0, 0, 0.05)',
          }}
        >

          <div
            style={{
              display: 'grid',
              gridTemplateColumns:
                'repeat(2, minmax(0, 1fr))',
              gap: '16px',
            }}
          >

            <div>

              <label
                htmlFor="name"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                Project Name
              </label>

              <input
                id="name"
                value={name}
                onChange={(event) =>
                  setName(event.target.value)
                }
                placeholder="Metro Station Project"
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                }}
              />

            </div>


            <div>

              <label
                htmlFor="code"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                Project Code
              </label>

              <input
                id="code"
                value={code}
                onChange={(event) =>
                  setCode(event.target.value)
                }
                placeholder="PRJ002"
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                }}
              />

            </div>


            <div>

              <label
                htmlFor="client"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                Client
              </label>

              <input
                id="client"
                value={client}
                onChange={(event) =>
                  setClient(event.target.value)
                }
                placeholder="ABC Infrastructure Ltd"
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                }}
              />

            </div>


            <div>

              <label
                htmlFor="location"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                Location
              </label>

              <input
                id="location"
                value={location}
                onChange={(event) =>
                  setLocation(event.target.value)
                }
                placeholder="Ranchi"
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                }}
              />

            </div>


            <div>

              <label
                htmlFor="start-date"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                Start Date
              </label>

              <input
                id="start-date"
                type="date"
                value={startDate}
                onChange={(event) =>
                  setStartDate(event.target.value)
                }
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                }}
              />

            </div>


            <div>

              <label
                htmlFor="end-date"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                End Date
              </label>

              <input
                id="end-date"
                type="date"
                value={endDate}
                onChange={(event) =>
                  setEndDate(event.target.value)
                }
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                }}
              />

            </div>


            <div>

              <label
                htmlFor="budget"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                Budget
              </label>

              <input
                id="budget"
                type="number"
                min="0"
                step="0.01"
                value={budget}
                onChange={(event) =>
                  setBudget(event.target.value)
                }
                placeholder="50000000"
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                }}
              />

            </div>


            <div>

              <label
                htmlFor="manager"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                Manager ID
              </label>

              <input
                id="manager"
                type="number"
                min="1"
                value={manager}
                onChange={(event) =>
                  setManager(event.target.value)
                }
                placeholder="2"
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                }}
              />

            </div>


            <div>

              <label
                htmlFor="status"
                style={{
                  display: 'block',
                  marginBottom: '6px',
                  fontWeight: 600,
                }}
              >
                Status
              </label>

              <select
                id="status"
                value={status}
                onChange={(event) =>
                  setStatus(event.target.value)
                }
                disabled={loading}
                style={{
                  width: '100%',
                  boxSizing: 'border-box',
                  padding: '10px 12px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                  background: '#ffffff',
                }}
              >

                <option value="ACTIVE">
                  Active
                </option>

                <option value="PLANNED">
                  Planned
                </option>

                <option value="COMPLETED">
                  Completed
                </option>

                <option value="ON_HOLD">
                  On Hold
                </option>

              </select>

            </div>

          </div>


          <div
            style={{
              marginTop: '16px',
            }}
          >

            <label
              htmlFor="description"
              style={{
                display: 'block',
                marginBottom: '6px',
                fontWeight: 600,
              }}
            >
              Description
            </label>

            <textarea
              id="description"
              value={description}
              onChange={(event) =>
                setDescription(event.target.value)
              }
              placeholder="Construction project description"
              rows={4}
              disabled={loading}
              style={{
                width: '100%',
                boxSizing: 'border-box',
                padding: '10px 12px',
                border:
                  '1px solid #d0d5dd',
                borderRadius: '8px',
                resize: 'vertical',
              }}
            />

          </div>


          {error && (

            <div
              role="alert"
              style={{
                marginTop: '16px',
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


          <div
            style={{
              display: 'flex',
              gap: '10px',
              marginTop: '20px',
            }}
          >

            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '11px 18px',
                border: 'none',
                borderRadius: '8px',
                background: '#2563eb',
                color: '#ffffff',
                fontWeight: 600,
                cursor: loading
                  ? 'not-allowed'
                  : 'pointer',
                opacity: loading ? 0.7 : 1,
              }}
            >
              {loading
                ? 'Creating...'
                : 'Create Project'}
            </button>


            <button
              type="button"
              disabled={loading}
              onClick={() =>
                navigate('/projects')
              }
              style={{
                padding: '11px 18px',
                border: '1px solid #d0d5dd',
                borderRadius: '8px',
                background: '#ffffff',
                color: '#344054',
                fontWeight: 600,
                cursor: loading
                  ? 'not-allowed'
                  : 'pointer',
              }}
            >
              Cancel
            </button>

          </div>

        </form>

      </section>

    </DashboardLayout>
  )
}


export default CreateProject