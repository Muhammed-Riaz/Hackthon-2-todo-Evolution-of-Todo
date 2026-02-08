# Loading Error State Pattern

**Name:** `loading-error-state-pattern`
**Description:** Standard data fetching states pattern for Next.js components in Phase 2
**Version:** `1.0-phase2`

## Instructions

For any component that fetches data, use one of these patterns (prefer Server Components when possible):

1. **Server Component + Suspense** (recommended)
2. **Client Component with useSWR / tanstack-query**
3. **Manual states: loading, error, data**

Always show:
- Loading skeleton / spinner
- Error message + retry button
- Empty state when no data

## Pattern 1: Server Component + Suspense (Recommended)

```tsx
// app/tasks/page.tsx
import { Suspense } from 'react';
import TaskList from './TaskList';
import Loading from './loading';

export default function TasksPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Your Tasks</h1>

      <Suspense fallback={<Loading />}>
        <TaskList />
      </Suspense>
    </div>
  );
}
```

## Pattern 2: Client Component with useSWR

```tsx
'use client';

import useSWR from 'swr';
import TaskList from './TaskList';
import TaskListSkeleton from './TaskListSkeleton';
import ErrorMessage from './ErrorMessage';
import EmptyState from './EmptyState';

export default function TasksClient() {
  const { data, error, isLoading, mutate } = useSWR('/api/tasks', fetcher);

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorMessage retry={mutate} />;
  if (!data?.length) return <EmptyState />;

  return <TaskList tasks={data} />;
}
```

## Pattern 3: Manual State Management

```tsx
'use client';

import { useState, useEffect } from 'react';
import TaskList from './TaskList';
import TaskListSkeleton from './TaskListSkeleton';
import ErrorMessage from './ErrorMessage';
import EmptyState from './EmptyState';

export default function TasksManual() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/tasks');
      const data = await response.json();
      setTasks(data);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  if (loading) return <TaskListSkeleton />;
  if (error) return <ErrorMessage retry={fetchTasks} />;
  if (!tasks?.length) return <EmptyState />;

  return <TaskList tasks={tasks} />;
}
```

## Component Examples

### TaskListSkeleton.tsx
```tsx
import { Skeleton } from '@/components/ui/skeleton';

export default function TaskListSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div key={i} className="flex items-center space-x-4 p-4 border rounded-lg">
          <Skeleton className="h-4 w-4 rounded-full" />
          <Skeleton className="h-4 flex-1" />
          <Skeleton className="h-8 w-20" />
        </div>
      ))}
    </div>
  );
}
```

### ErrorMessage.tsx
```tsx
export default function ErrorMessage({ retry }: { retry: () => void }) {
  return (
    <div className="text-center py-8">
      <div className="text-red-500 mb-4">
        <AlertCircle className="mx-auto h-8 w-8" />
      </div>
      <h3 className="text-lg font-medium mb-2">Failed to load tasks</h3>
      <p className="text-gray-500 mb-4">Please check your connection and try again</p>
      <button
        onClick={retry}
        className="btn-secondary"
      >
        Retry
      </button>
    </div>
  );
}
```

### EmptyState.tsx
```tsx
export default function EmptyState() {
  return (
    <div className="text-center py-12">
      <div className="text-gray-400 mb-4">
        <Inbox className="mx-auto h-12 w-12" />
      </div>
      <h3 className="text-lg font-medium mb-2">No tasks found</h3>
      <p className="text-gray-500">Create your first task to get started</p>
    </div>
  );
}
```

## Best Practices

### State Order Matters
Always check states in this order:
1. **Loading** - Show skeleton first
2. **Error** - Handle errors before rendering data
3. **Empty** - Check for empty data after successful load
4. **Success** - Render actual data

### Error Handling
- Provide clear error messages
- Include retry functionality
- Log errors for debugging
- Consider error boundaries for critical components

### Loading States
- Use skeletons that match content layout
- Add subtle animations for better UX
- Consider progressive loading for large datasets

### Empty States
- Provide helpful guidance
- Include call-to-action when appropriate
- Keep design consistent with app style

## Recommended Libraries

- **useSWR**: Simple data fetching with caching
- **tanstack-query**: Advanced data management
- **React Suspense**: Built-in loading states
- **Next.js App Router**: Server components

## Benefits

- **Consistent UX**: Same pattern across all components
- **Better UX**: Users always know what's happening
- **Error resilience**: Graceful degradation
- **Performance**: Optimized loading states
- **Maintainability**: Standardized approach