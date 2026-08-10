import apiClient from './client'


export interface DashboardKPI {
  total_projects: number
  total_employees: number
  total_tasks: number
  total_materials: number
  total_inventory_items: number
  total_expenses: string
  total_payroll: string
}


export interface MonthlyExpense {
  month: string
  total_expense: string
}


export interface MonthlyPayroll {
  month: string
  total_payroll: string
}


export const getDashboardKPI =
  async (): Promise<DashboardKPI> => {

    const response =
      await apiClient.get<DashboardKPI>(
        '/dashboard/kpi/',
      )

    return response.data
  }


export const getMonthlyExpenses =
  async (): Promise<MonthlyExpense[]> => {

    const response =
      await apiClient.get<MonthlyExpense[]>(
        '/dashboard/monthly-expenses/',
      )

    return response.data
  }


export const getMonthlyPayroll =
  async (): Promise<MonthlyPayroll[]> => {

    const response =
      await apiClient.get<MonthlyPayroll[]>(
        '/dashboard/monthly-payroll/',
      )

    return response.data
  }