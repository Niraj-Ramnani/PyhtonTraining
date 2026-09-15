import { useEffect, useState } from 'react';
import type { User, Task } from '../../types/types';
import { useTasks } from '../../hooks/useTasks';
import Navbar from '../../components/Navbar/Navbar';
import TaskCard from '../../components/TaskCard/TaskCard';
import TaskForm from '../../components/TaskForm/TaskForm';
import './DashboardPage.css';

interface DashboardPageProps {
  user: User;
  onLogout: () => void;
}

type FilterType = 'all' | 'pending' | 'done';

function DashboardPage({ user, onLogout }: DashboardPageProps) {
  const { tasks, loading, error, fetchTasks, addTask, editTask, removeTask, toggleComplete } =
    useTasks();

  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [filter, setFilter] = useState<FilterType>('all');
  const [actionError, setActionError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const openCreate = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  const openEdit = (task: Task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const closeForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handleFormSubmit = async (data: { title: string; description: string; is_completed?: boolean }) => {
    setActionError(null);
    try {
      if (editingTask) {
        await editTask(editingTask.id, data);
      } else {
        await addTask(data);
      }
      closeForm();
    } catch (err) {
      throw err; // Let TaskForm show the error
    }
  };

  const handleDelete = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    setActionError(null);
    try {
      await removeTask(taskId);
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Failed to delete task');
    }
  };

  const handleToggle = async (task: Task) => {
    setActionError(null);
    try {
      await toggleComplete(task);
    } catch (err) {
      setActionError(err instanceof Error ? err.message : 'Failed to update task');
    }
  };

  const filteredTasks = tasks.filter((t) => {
    if (filter === 'pending') return !t.is_completed;
    if (filter === 'done') return t.is_completed;
    return true;
  });

  const counts = {
    all: tasks.length,
    pending: tasks.filter((t) => !t.is_completed).length,
    done: tasks.filter((t) => t.is_completed).length,
  };

  return (
    <div className="dashboard">
      <Navbar user={user} onLogout={onLogout} />

      <main className="dashboard__main">
        {/* Header */}
        <div className="dashboard__header">
          <div>
            <h1 className="dashboard__title">My Tasks</h1>
            <p className="dashboard__subtitle">
              {counts.pending} pending · {counts.done} completed
            </p>
          </div>
          <button id="new-task-btn" className="dashboard__add-btn" onClick={openCreate}>
            + New Task
          </button>
        </div>

        {/* Filters */}
        <div className="dashboard__filters">
          {(['all', 'pending', 'done'] as FilterType[]).map((f) => (
            <button
              key={f}
              id={`filter-${f}`}
              className={`dashboard__filter-btn ${filter === f ? 'dashboard__filter-btn--active' : ''}`}
              onClick={() => setFilter(f)}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}{' '}
              <span className="dashboard__filter-count">{counts[f]}</span>
            </button>
          ))}
        </div>

        {/* Errors */}
        {(error || actionError) && (
          <div className="dashboard__error">{error ?? actionError}</div>
        )}

        {/* Task list */}
        {loading ? (
          <div className="dashboard__loading">
            <div className="spinner" />
            <p>Loading tasks...</p>
          </div>
        ) : filteredTasks.length === 0 ? (
          <div className="dashboard__empty">
            <span className="dashboard__empty-icon">📋</span>
            <p>
              {filter === 'all'
                ? 'No tasks yet. Create your first task!'
                : `No ${filter} tasks.`}
            </p>
          </div>
        ) : (
          <div className="dashboard__task-list">
            {filteredTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={openEdit}
                onDelete={handleDelete}
                onToggle={handleToggle}
              />
            ))}
          </div>
        )}
      </main>

      {/* Modal form */}
      {showForm && (
        <TaskForm
          initialData={editingTask}
          onSubmit={handleFormSubmit}
          onCancel={closeForm}
        />
      )}
    </div>
  );
}

export default DashboardPage;
