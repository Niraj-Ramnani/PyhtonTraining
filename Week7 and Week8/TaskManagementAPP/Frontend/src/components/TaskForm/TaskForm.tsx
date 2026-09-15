import { useState, useEffect } from 'react';
import type { Task, CreateTaskRequest } from '../../types/types';
import './TaskForm.css';

interface TaskFormProps {
  initialData?: Task | null;
  onSubmit: (data: CreateTaskRequest) => Promise<void>;
  onCancel: () => void;
}

function TaskForm({ initialData, onSubmit, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isCompleted, setIsCompleted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title);
      setDescription(initialData.description);
      setIsCompleted(initialData.is_completed);
    }
  }, [initialData]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) {
      setError('Title is required');
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      await onSubmit({ title: title.trim(), description: description.trim(), is_completed: isCompleted });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save task');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="task-form-overlay" onClick={onCancel}>
      <div className="task-form" onClick={(e) => e.stopPropagation()}>
        <div className="task-form__header">
          <h2 className="task-form__title">{initialData ? 'Edit Task' : 'New Task'}</h2>
          <button id="close-form-btn" className="task-form__close" onClick={onCancel}>✕</button>
        </div>

        {error && <p className="task-form__error">{error}</p>}

        <form onSubmit={handleSubmit} className="task-form__body">
          <div className="task-form__field">
            <label htmlFor="task-title" className="task-form__label">Title</label>
            <input
              id="task-title"
              className="task-form__input"
              type="text"
              placeholder="Enter task title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              autoFocus
            />
          </div>

          <div className="task-form__field">
            <label htmlFor="task-description" className="task-form__label">Description</label>
            <textarea
              id="task-description"
              className="task-form__textarea"
              placeholder="Enter task description"
              rows={4}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          <div className="task-form__field task-form__field--inline">
            <input
              id="task-completed"
              type="checkbox"
              checked={isCompleted}
              onChange={(e) => setIsCompleted(e.target.checked)}
              className="task-form__checkbox"
            />
            <label htmlFor="task-completed" className="task-form__label">Mark as completed</label>
          </div>

          <div className="task-form__actions">
            <button
              id="cancel-form-btn"
              type="button"
              className="task-form__btn task-form__btn--cancel"
              onClick={onCancel}
            >
              Cancel
            </button>
            <button
              id="submit-form-btn"
              type="submit"
              className="task-form__btn task-form__btn--submit"
              disabled={submitting}
            >
              {submitting ? 'Saving...' : initialData ? 'Save Changes' : 'Create Task'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default TaskForm;
