import apiClient from './client'


export interface Project {
  id: number
  name: string
  code: string
  description: string
  client: string
  location: string
  start_date: string
  end_date: string
  budget: string
  status: string
  manager: number
  manager_name: string
  created_at: string
  updated_at: string
}


export type ProjectInput = Omit<
  Project,
  'id' | 'created_at' | 'updated_at' | 'manager_name'
>


export const getProjects = async (): Promise<Project[]> => {
  const response =
    await apiClient.get<Project[]>(
      '/projects/',
    )

  return response.data
}


export const getProject = async (
  id: number,
): Promise<Project> => {
  const response =
    await apiClient.get<Project>(
      `/projects/${id}/`,
    )

  return response.data
}


export const createProject = async (
  projectData: ProjectInput,
): Promise<Project> => {

  const response =
    await apiClient.post<Project>(
      '/projects/',
      projectData,
    )

  return response.data
}


export const updateProject = async (
  id: number,
  projectData: ProjectInput,
): Promise<Project> => {

  const response =
    await apiClient.put<Project>(
      `/projects/${id}/`,
      projectData,
    )

  return response.data
}