import { useEffect, useState } from 'react'

import DashboardLayout from '../components/layout/DashboardLayout'
import {
  getDashboardKPI,
} from '../api/dashboard'

import type {
  DashboardKPI,
} from '../api/dashboard'


function Dashboard() {

  const [kpi, setKpi] =
    useState<DashboardKPI | null>(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')


  useEffect(() => {

    const loadDashboard = async () => {

      try {

        setLoading(true)
        setError('')

        const data =
          await getDashboardKPI()

        setKpi(data)

      } catch (error) {

        console.error(
          'Failed to load dashboard',
          error,
        )

        setError(
          'Unable to load dashboard data.',
        )

      } finally {

        setLoading(false)

      }
    }


    loadDashboard()

  }, [])


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


        {loading && (

          <p>
            Loading dashboard...
          </p>

        )}


        {!loading && error && (

          <p>
            {error}
          </p>

        )}


        {!loading && !error && kpi && (

          <div className="dashboard-grid">

            <div className="dashboard-card">

              <span>
                Total Projects
              </span>

              <strong>
                {kpi.total_projects}
              </strong>

            </div>


            <div className="dashboard-card">

              <span>
                Total Employees
              </span>

              <strong>
                {kpi.total_employees}
              </strong>

            </div>


            <div className="dashboard-card">

              <span>
                Total Tasks
              </span>

              <strong>
                {kpi.total_tasks}
              </strong>

            </div>


            <div className="dashboard-card">

              <span>
                Total Materials
              </span>

              <strong>
                {kpi.total_materials}
              </strong>

            </div>


            <div className="dashboard-card">

              <span>
                Inventory Items
              </span>

              <strong>
                {kpi.total_inventory_items}
              </strong>

            </div>


            <div className="dashboard-card">

              <span>
                Total Expenses
              </span>

              <strong>
                  {'₹'}{Number(
                  kpi.total_expenses || 0,
                ).toLocaleString('en-IN')}
              </strong>

            </div>


            <div className="dashboard-card">

              <span>
                Total Payroll
              </span>

              <strong>
                  {'₹'}{Number(
                  kpi.total_payroll || 0,
                ).toLocaleString('en-IN')}
              </strong>

            </div>

          </div>

        )}

      </section>

    </DashboardLayout>
  )
}


export default Dashboard