import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import DashboardLayout from '../components/layout/DashboardLayout'
import {
  getProjects,
  type Project,
} from '../api/projects'


function Projects() {

  const navigate = useNavigate()


  const [projects, setProjects] =
    useState<Project[]>([])


  const [loading, setLoading] =
    useState(true)


  const [error, setError] =
    useState('')


  const [page, setPage] =
    useState(1)


  const [pageSize] =
    useState(20)


  const [totalProjects, setTotalProjects] =
    useState(0)


  const [hasNextPage, setHasNextPage] =
    useState(false)


  const [hasPreviousPage, setHasPreviousPage] =
    useState(false)


  useEffect(() => {

    const loadProjects = async () => {

      try {

        setLoading(true)
        setError('')

        const data =
          await getProjects(
            page,
            pageSize,
          )

        setProjects(data.results)

        setTotalProjects(data.count)

        setHasNextPage(
          Boolean(data.next),
        )

        setHasPreviousPage(
          Boolean(data.previous),
        )

      } catch (error) {

        console.error(
          'Failed to load projects',
          error,
        )

        setError(
          'Unable to load projects.',
        )

        setProjects([])

      } finally {

        setLoading(false)

      }

    }


    loadProjects()

  }, [
    page,
    pageSize,
  ])


  const totalPages =
    Math.ceil(
      totalProjects / pageSize,
    )


  return (
    <DashboardLayout>

      <section className="dashboard-page">

        <div className="page-header">

          <div>

            <h1>
              Projects
            </h1>

            <p>
              Manage construction projects.
            </p>

          </div>

        </div>


        {loading ? (

          <p>
            Loading projects...
          </p>

        ) : error ? (

          <p>
            {error}
          </p>

        ) : (

          <div>

            {projects.length === 0 ? (

              <p>
                No projects found.
              </p>

            ) : (

              <>

                <table
                  style={{
                    width: '100%',
                    background: '#ffffff',
                    borderRadius: '8px',
                  }}
                >

                  <thead>

                    <tr>

                      <th>
                        Name
                      </th>

                      <th>
                        Code
                      </th>

                      <th>
                        Client
                      </th>

                      <th>
                        Status
                      </th>

                      <th>
                        Budget
                      </th>

                    </tr>

                  </thead>


                  <tbody>

                    {projects.map(
                      (project) => (

                        <tr
                          key={project.id}
                          onClick={() =>
                            navigate(
                              `/projects/${project.id}`,
                            )
                          }
                          style={{
                            cursor: 'pointer',
                          }}
                        >

                          <td>
                            {project.name}
                          </td>

                          <td>
                            {project.code}
                          </td>

                          <td>
                            {project.client}
                          </td>

                          <td>
                            {project.status}
                          </td>

                          <td>
                            ₹
                            {Number(
                              project.budget,
                            ).toLocaleString(
                              'en-IN',
                            )}
                          </td>

                        </tr>

                      ),
                    )}

                  </tbody>

                </table>


                {totalPages > 1 && (

                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      marginTop: '20px',
                      padding: '12px 0',
                    }}
                  >

                    <button
                      type="button"
                      onClick={() =>
                        setPage(
                          (currentPage) =>
                            Math.max(
                              currentPage - 1,
                              1,
                            ),
                        )
                      }
                      disabled={
                        !hasPreviousPage ||
                        loading
                      }
                    >
                      Previous
                    </button>


                    <span>
                      Page {page} of {totalPages}
                    </span>


                    <button
                      type="button"
                      onClick={() =>
                        setPage(
                          (currentPage) =>
                            currentPage + 1,
                        )
                      }
                      disabled={
                        !hasNextPage ||
                        loading
                      }
                    >
                      Next
                    </button>

                  </div>

                )}

              </>

            )}

          </div>

        )}

      </section>

    </DashboardLayout>
  )
}


export default Projects