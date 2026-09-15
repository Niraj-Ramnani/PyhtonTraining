export interface Task {
  id: number;
  title: string;
  description: string;
  is_completed: boolean;
  user_id: number | null;
}

export interface User {
  id: number;
  name: string;
  username: string;
  email: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  username: string;
  password: string;
  email: string;
}

export interface LoginResponse {
  token: string;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
  is_completed?: boolean;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  is_completed?: boolean;
}