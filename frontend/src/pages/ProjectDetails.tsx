import { useEffect, useState } from 'react'
import {
  Link,
  useParams,
} from 'react-router-dom'

import DashboardLayout from '../components/layout/DashboardLayout'
import {
  getProject,
  type Project,
} from '../api/projects'


function ProjectDetails() {

  const { id } =
    useParams()


  const [project, setProject] =
    useState<Project | null>(null)


  const [loading, setLoading] =
    useState(true)


  useEffect(() => {

    const loadProject = async () => {

      if (!id) {
        return
      }


      try {

        const data =
          await getProject(
            Number(id),
          )

        setProject(data)

      } catch (error) {

        console.error(
          'Failed to load project',
          error,
        )

      } finally {

        setLoading(false)

      }

    }


    loadProject()

  }, [id])


  return (
    <DashboardLayout>

      <section className="dashboard-page">

        <div
          className="page-header"
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            gap: '16px',
          }}
        >

          <div>

            <h1>
              Project Details
            </h1>

            <p>
              View construction project information.
            </p>

          </div>

          {project && id && (

            <Link
              to={`/projects/${id}/edit`}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '10px 18px',
                borderRadius: '8px',
                background: '#2563eb',
                color: '#ffffff',
                textDecoration: 'none',
                fontSize: '14px',
                fontWeight: 600,
              }}
            >
              Edit Project
            </Link>

          )}

        </div>


        {loading ? (

          <p>
            Loading project...
          </p>

        ) : !project ? (

          <p>
            Project not found.
          </p>

        ) : (

          <div
            className="dashboard-card"
          >

            <h2>
              {project.name}
            </h2>


            <p>
              <strong>
                Code:
              </strong>{' '}
              {project.code}
            </p>


            <p>
              <strong>
                Client:
              </strong>{' '}
              {project.client}
            </p>


            <p>
              <strong>
                Location:
              </strong>{' '}
              {project.location}
            </p>


            <p>
              <strong>
                Status:
              </strong>{' '}
              {project.status}
            </p>


            <p>
              <strong>
                Budget:
              </strong>{' '}
              ₹
              {Number(
                project.budget,
              ).toLocaleString()}
            </p>


            <p>
              <strong>
                Manager:
              </strong>{' '}
              {project.manager_name}
            </p>


          </div>

        )}

      </section>

    </DashboardLayout>
  )
}


export default ProjectDetails