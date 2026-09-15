import { useState, useCallback } from 'react';
import type { Task, CreateTaskRequest, UpdateTaskRequest } from '../types/types';
import {
  getAllTasks,
  createTask,
  updateTask,
  deleteTask,
} from '../services/api';

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllTasks();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  }, []);

  const addTask = useCallback(async (data: CreateTaskRequest) => {
    const newTask = await createTask(data);
    setTasks((prev) => [newTask, ...prev]);
    return newTask;
  }, []);

  const editTask = useCallback(async (taskId: number, data: UpdateTaskRequest) => {
    const updated = await updateTask(taskId, data);
    setTasks((prev) => prev.map((t) => (t.id === taskId ? updated : t)));
    return updated;
  }, []);

  const removeTask = useCallback(async (taskId: number) => {
    await deleteTask(taskId);
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  }, []);

  const toggleComplete = useCallback(async (task: Task) => {
    const updated = await updateTask(task.id, { is_completed: !task.is_completed });
    setTasks((prev) => prev.map((t) => (t.id === task.id ? updated : t)));
  }, []);

  return { tasks, loading, error, fetchTasks, addTask, editTask, removeTask, toggleComplete };
}
