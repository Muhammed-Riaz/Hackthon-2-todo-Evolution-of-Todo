# Modern Form Component Next.js Skill

**Name:** `modern-form-component-nextjs`
**Description:** Clean, modern, accessible form pattern for Phase 2 Todo app (Next.js + Tailwind)
**Version:** `1.0-phase2`

## Instructions

Use this pattern for all forms in Phase 2 Todo app (create task, update task, login, signup).

## Preferred Stack

- **Form Management**: `react-hook-form`
- **Validation**: `zod` for schema validation
- **Styling**: `tailwindcss` with glassmorphism/neumorphism
- **Accessibility**: Full ARIA support

## Form Structure Pattern

```tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

// 1. Define validation schema with Zod
const formSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  description: z.string().max(2000, 'Description too long').optional(),
});

type FormValues = z.infer<typeof formSchema>;

export function TaskForm({ onSubmit, initialData = null }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: initialData || {
      title: '',
      description: '',
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      {/* Form fields go here */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="btn-primary"
      >
        {isSubmitting ? 'Saving...' : 'Save Task'}
      </button>
    </form>
  );
}
```

## Field Component Pattern

```tsx
function FormField({
  id,
  label,
  type = "text",
  placeholder = "",
  error,
  register,
  required = false,
}) {
  const fieldId = `${id}-field`;
  const errorId = `${id}-error`;

  return (
    <div className="space-y-2">
      <label
        htmlFor={fieldId}
        className="block text-sm font-medium text-gray-700 dark:text-gray-300"
      >
        {label} {required && <span className="text-red-500">*</span>}
      </label>

      <input
        id={fieldId}
        type={type}
        placeholder={placeholder}
        aria-invalid={!!error}
        aria-describedby={error ? errorId : undefined}
        className={`form-input ${error ? 'border-red-500' : 'border-gray-300'}`}
        {...register(id)}
      />

      {error && (
        <p
          id={errorId}
          className="text-sm text-red-600 dark:text-red-400"
          role="alert"
        >
          {error.message}
        </p>
      )}
    </div>
  );
}
```

## Complete Form Example

```tsx
function TaskCreateForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
  });

  async function handleFormSubmit(data: FormValues) {
    try {
      await createTask(data);
      toast.success('Task created successfully!');
    } catch (error) {
      toast.error('Failed to create task');
    }
  }

  return (
    <div className="form-card">
      <h2 className="form-title">Create New Task</h2>

      <form onSubmit={form.handleSubmit(handleFormSubmit)} className="space-y-6">
        <FormField
          id="title"
          label="Title"
          placeholder="What needs to be done?"
          error={form.formState.errors.title}
          register={form.register}
          required
        />

        <FormField
          id="description"
          label="Description"
          placeholder="Add more details..."
          error={form.formState.errors.description}
          register={form.register}
          type="textarea"
        />

        <button
          type="submit"
          disabled={form.formState.isSubmitting}
          className="btn-primary w-full"
        >
          {form.formState.isSubmitting ? (
            <>
              <span className="spinner"></span> Creating...
            </>
          ) : (
            'Create Task'
          )}
        </button>
      </form>
    </div>
  );
}
```

## Styling Guidelines

### Glassmorphism Card
```css
.form-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

### Neumorphism Input
```css
.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05),
              -2px -2px 4px rgba(255, 255, 255, 0.7);
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}
```

## Accessibility Features

- **ARIA attributes**: `aria-invalid`, `aria-describedby`
- **Semantic HTML**: Proper use of `<label>`, `<form>`, `<button>`
- **Keyboard navigation**: Full keyboard support
- **Screen reader support**: Proper labels and error messages
- **Focus states**: Visible focus indicators

## Responsive Design

- **Mobile first**: Design for small screens first
- **Stacked layout**: Form fields stack vertically
- **Full-width buttons**: Easy tapping on mobile
- **Proper spacing**: `space-y-*` for consistent gaps

## Benefits

- **Consistent UI**: Same pattern across all forms
- **Type safety**: Zod validation with TypeScript
- **Performance**: Efficient form handling with react-hook-form
- **Accessibility**: Full ARIA compliance
- **Modern design**: Glassmorphism/neumorphism styling
- **Responsive**: Works on all screen sizes