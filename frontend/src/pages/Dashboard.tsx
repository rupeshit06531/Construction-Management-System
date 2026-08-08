import { useEffect, useState } from 'react'

import DashboardLayout from '../components/layout/DashboardLayout'
import { getProjects } from '../api/projects'


interface Project {
  id: number
  status: string
  budget: string
}


function Dashboard() {

  const [projects, setProjects] =
    useState<Project[]>([])


  useEffect(() => {

    const loadProjects = async () => {
      try {

        const data = await getProjects()

        setProjects(data)

      } catch (error) {

        console.error(
          'Failed to load projects',
          error,
        )

      }
    }


    loadProjects()

  }, [])


  const totalProjects =
    projects.length


  const activeProjects =
    projects.filter(
      (project) =>
        project.status === 'ACTIVE',
    ).length


  const completedProjects =
    projects.filter(
      (project) =>
        project.status === 'COMPLETED',
    ).length


  const totalBudget =
    projects.reduce(
      (sum, project) =>
        sum + Number(project.budget || 0),
      0,
    )


  return (
    <DashboardLayout>

      <section className="dashboard-page">

        <div className="page-header">

          <div>
            <h1>
              Dashboard
            </h1>

            <p>
              Overview of your construction management system.
            </p>
          </div>

        </div>


        <div className="dashboard-grid">


          <div className="dashboard-card">

            <span>
              Total Projects
            </span>

            <strong>
              {totalProjects}
            </strong>

          </div>



          <div className="dashboard-card">

            <span>
              Active Projects
            </span>

            <strong>
              {activeProjects}
            </strong>

          </div>



          <div className="dashboard-card">

            <span>
              Completed Projects
            </span>

            <strong>
              {completedProjects}
            </strong>

          </div>



          <div className="dashboard-card">

            <span>
              Total Budget
            </span>

            <strong>
              ₹{totalBudget.toLocaleString()}
            </strong>

          </div>


        </div>

      </section>

    </DashboardLayout>
  )
}


export default Dashboard