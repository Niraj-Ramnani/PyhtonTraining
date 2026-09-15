import type { Task } from '../../types/types';
import './TaskCard.css';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
  onToggle: (task: Task) => void;
}

function TaskCard({ task, onEdit, onDelete, onToggle }: TaskCardProps) {
  return (
    <div className={`task-card ${task.is_completed ? 'task-card--done' : ''}`}>
      <div className="task-card__left">
        <button
          id={`toggle-task-${task.id}`}
          className={`task-card__checkbox ${task.is_completed ? 'task-card__checkbox--checked' : ''}`}
          onClick={() => onToggle(task)}
          aria-label="Toggle task completion"
        >
          {task.is_completed && <span>✓</span>}
        </button>
      </div>

      <div className="task-card__body">
        <h3 className="task-card__title">{task.title}</h3>
        <p className="task-card__description">{task.description}</p>
      </div>

      <div className="task-card__actions">
        <span className={`task-card__badge ${task.is_completed ? 'task-card__badge--done' : 'task-card__badge--pending'}`}>
          {task.is_completed ? 'Done' : 'Pending'}
        </span>
        <button
          id={`edit-task-${task.id}`}
          className="task-card__btn task-card__btn--edit"
          onClick={() => onEdit(task)}
        >
          Edit
        </button>
        <button
          id={`delete-task-${task.id}`}
          className="task-card__btn task-card__btn--delete"
          onClick={() => onDelete(task.id)}
        >
          Delete
        </button>
      </div>
    </div>
  );
}

export default TaskCard;
