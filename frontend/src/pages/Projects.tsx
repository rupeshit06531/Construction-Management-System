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


  useEffect(() => {

    const loadProjects = async () => {

      try {

        const data =
          await getProjects()

        setProjects(data)

      } catch (error) {

        console.error(
          'Failed to load projects',
          error,
        )

      } finally {

        setLoading(false)

      }

    }


    loadProjects()

  }, [])


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

        ) : (

          <div>

            {projects.length === 0 ? (

              <p>
                No projects found.
              </p>

            ) : (

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
                          ).toLocaleString()}
                        </td>

                      </tr>

                    ),
                  )}

                </tbody>


              </table>

            )}

          </div>

        )}

      </section>

    </DashboardLayout>
  )
}


export default Projects