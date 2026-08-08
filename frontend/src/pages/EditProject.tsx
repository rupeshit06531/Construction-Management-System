import {
  useEffect,
  useState,
  type FormEvent,
} from 'react'

import {
  useNavigate,
  useParams,
} from 'react-router-dom'

import DashboardLayout from '../components/layout/DashboardLayout'
import {
  getProject,
  updateProject,
  type Project,
  type ProjectInput,
} from '../api/projects'


function EditProject() {

  const { id } = useParams()
  const navigate = useNavigate()


  const [project, setProject] =
    useState<Project | null>(null)


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


  const [loading, setLoading] =
    useState(true)

  const [saving, setSaving] =
    useState(false)

  const [error, setError] =
    useState('')


  useEffect(() => {

    const loadProject = async () => {

      if (!id) {
        setError('Invalid project ID.')
        setLoading(false)
        return
      }


      try {

        const data =
          await getProject(
            Number(id),
          )


        setProject(data)

        setName(data.name)
        setCode(data.code)
        setDescription(data.description || '')
        setClient(data.client)
        setLocation(data.location)
        setStartDate(data.start_date)
        setEndDate(data.end_date)
        setBudget(data.budget)
        setStatus(data.status)
        setManager(
          String(data.manager),
        )

      } catch (requestError) {

        console.error(
          'Failed to load project',
          requestError,
        )

        setError(
          'Failed to load project.',
        )

      } finally {

        setLoading(false)

      }
    }


    loadProject()

  }, [id])


  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {

    event.preventDefault()

    setError('')


    if (!id || !project) {
      setError(
        'Project information is unavailable.',
      )
      return
    }


    if (!name.trim()) {
      setError(
        'Project name is required.',
      )
      return
    }


    if (!code.trim()) {
      setError(
        'Project code is required.',
      )
      return
    }


    if (!client.trim()) {
      setError(
        'Client name is required.',
      )
      return
    }


    if (!location.trim()) {
      setError(
        'Location is required.',
      )
      return
    }


    if (!startDate) {
      setError(
        'Start date is required.',
      )
      return
    }


    if (!endDate) {
      setError(
        'End date is required.',
      )
      return
    }


    if (!budget) {
      setError(
        'Budget is required.',
      )
      return
    }


    if (!manager) {
      setError(
        'Manager ID is required.',
      )
      return
    }


    const projectData: ProjectInput = {
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
    }


    try {

      setSaving(true)


      const updatedProject =
        await updateProject(
          Number(id),
          projectData,
        )


      navigate(
        `/projects/${updatedProject.id}`,
        { replace: true },
      )

    } catch (requestError) {

      console.error(
        'Failed to update project',
        requestError,
      )

      setError(
        'Failed to update project. Please check the entered information.',
      )

    } finally {

      setSaving(false)

    }
  }


  return (
    <DashboardLayout>

      <section className="dashboard-page">

        <div className="page-header">

          <div>

            <h1>
              Edit Project
            </h1>

            <p>
              Update construction project information.
            </p>

          </div>

        </div>


        {loading ? (

          <p>
            Loading project...
          </p>

        ) : !project ? (

          <div>

            <p>
              {error || 'Project not found.'}
            </p>

            <button
              type="button"
              onClick={() =>
                navigate('/projects')
              }
              style={{
                marginTop: '12px',
                padding: '10px 16px',
                border: 'none',
                borderRadius: '8px',
                background: '#2563eb',
                color: '#ffffff',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Back to Projects
            </button>

          </div>

        ) : (

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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                  disabled={saving}
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
                rows={4}
                disabled={saving}
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
                disabled={saving}
                style={{
                  padding: '11px 18px',
                  border: 'none',
                  borderRadius: '8px',
                  background: '#2563eb',
                  color: '#ffffff',
                  fontWeight: 600,
                  cursor: saving
                    ? 'not-allowed'
                    : 'pointer',
                  opacity: saving ? 0.7 : 1,
                }}
              >
                {saving
                  ? 'Saving...'
                  : 'Save Changes'}
              </button>


              <button
                type="button"
                disabled={saving}
                onClick={() =>
                  navigate(
                    `/projects/${project.id}`,
                  )
                }
                style={{
                  padding: '11px 18px',
                  border:
                    '1px solid #d0d5dd',
                  borderRadius: '8px',
                  background: '#ffffff',
                  color: '#344054',
                  fontWeight: 600,
                  cursor: saving
                    ? 'not-allowed'
                    : 'pointer',
                }}
              >
                Cancel
              </button>

            </div>

          </form>

        )}

      </section>

    </DashboardLayout>
  )
}


export default EditProject