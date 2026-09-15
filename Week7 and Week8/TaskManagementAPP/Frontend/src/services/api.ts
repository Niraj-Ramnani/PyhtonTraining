import type {
  Task,
  User,
  LoginRequest,
  RegisterRequest,
  LoginResponse,
  CreateTaskRequest,
  UpdateTaskRequest,
} from '../types/types';

const BASE_URL = 'http://127.0.0.1:8000';

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Something went wrong' }));
    throw new Error(error.detail ?? 'Request failed');
  }
  // 204 No Content has no body
  if (res.status === 204) return undefined as T;
  return res.json();
}

// ── Auth ──────────────────────────────────────────────────────────────────────

export async function registerUser(data: RegisterRequest): Promise<User> {
  const res = await fetch(`${BASE_URL}/user/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<User>(res);
}

export async function loginUser(data: LoginRequest): Promise<LoginResponse> {
  const res = await fetch(`${BASE_URL}/user/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<LoginResponse>(res);
}

export async function getCurrentUser(): Promise<User> {
  const res = await fetch(`${BASE_URL}/user/is_auth`, {
    headers: getAuthHeaders(),
  });
  return handleResponse<User>(res);
}

// ── Tasks ─────────────────────────────────────────────────────────────────────

export async function getAllTasks(): Promise<Task[]> {
  const res = await fetch(`${BASE_URL}/tasks/all_tasks`, {
    headers: getAuthHeaders(),
  });
  return handleResponse<Task[]>(res);
}

export async function getOneTask(taskId: number): Promise<Task> {
  const res = await fetch(`${BASE_URL}/tasks/one_task/${taskId}`, {
    headers: getAuthHeaders(),
  });
  return handleResponse<Task>(res);
}

export async function createTask(data: CreateTaskRequest): Promise<Task> {
  const res = await fetch(`${BASE_URL}/tasks/create`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse<Task>(res);
}

export async function updateTask(taskId: number, data: UpdateTaskRequest): Promise<Task> {
  const res = await fetch(`${BASE_URL}/tasks/update_task/${taskId}`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });
  return handleResponse<Task>(res);
}

export async function deleteTask(taskId: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/tasks/delete_task/${taskId}`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  return handleResponse<void>(res);
}