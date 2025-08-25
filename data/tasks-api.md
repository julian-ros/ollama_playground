# Tasks API

## Overview

The Tasks API allows you to create, manage, and organize tasks in your Julio workspace.

## Endpoints

### Create Task

Create a new task in your workspace.

```http
POST /v1/tasks
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "title": "Complete project proposal",
  "description": "Write and review the Q4 project proposal document",
  "priority": "high",
  "due_date": "2024-02-15T17:00:00Z",
  "project_id": "proj_123",
  "assignee_id": "user_456",
  "tags": ["proposal", "q4", "urgent"]
}
```

**Response:**
```json
{
  "id": "task_abc123",
  "title": "Complete project proposal",
  "description": "Write and review the Q4 project proposal document",
  "status": "todo",
  "priority": "high",
  "due_date": "2024-02-15T17:00:00Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "project_id": "proj_123",
  "assignee_id": "user_456",
  "creator_id": "user_789",
  "tags": ["proposal", "q4", "urgent"],
  "estimated_hours": null,
  "actual_hours": 0
}
```

### Get Task Details

Retrieve information about a specific task.

```http
GET /v1/tasks/{task_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "id": "task_abc123",
  "title": "Complete project proposal",
  "description": "Write and review the Q4 project proposal document",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2024-02-15T17:00:00Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T09:15:00Z",
  "project_id": "proj_123",
  "assignee": {
    "id": "user_456",
    "name": "John Doe",
    "email": "john@company.com"
  },
  "creator": {
    "id": "user_789",
    "name": "Jane Smith",
    "email": "jane@company.com"
  },
  "tags": ["proposal", "q4", "urgent"],
  "estimated_hours": 8,
  "actual_hours": 3.5,
  "comments_count": 2,
  "attachments_count": 1
}
```

### List Tasks

Get a list of tasks with optional filtering.

```http
GET /v1/tasks?status=todo&assignee_id=user_456&limit=50
Authorization: Bearer YOUR_API_KEY
```

**Query Parameters:**
- `status` (optional): Filter by status (`todo`, `in_progress`, `done`, `cancelled`)
- `priority` (optional): Filter by priority (`low`, `medium`, `high`, `urgent`)
- `assignee_id` (optional): Filter by assigned user
- `project_id` (optional): Filter by project
- `due_before` (optional): Filter tasks due before date (ISO 8601)
- `due_after` (optional): Filter tasks due after date (ISO 8601)
- `tags` (optional): Filter by tags (comma-separated)
- `limit` (optional): Number of tasks to return (default: 50, max: 100)
- `offset` (optional): Number of tasks to skip (default: 0)
- `sort` (optional): Sort by `created_at`, `updated_at`, `due_date`, or `priority`
- `order` (optional): `asc` or `desc` (default: `desc`)

**Response:**
```json
{
  "tasks": [
    {
      "id": "task_abc123",
      "title": "Complete project proposal",
      "status": "todo",
      "priority": "high",
      "due_date": "2024-02-15T17:00:00Z",
      "assignee": {
        "id": "user_456",
        "name": "John Doe"
      },
      "project": {
        "id": "proj_123",
        "name": "Q4 Initiative"
      }
    }
  ],
  "total": 25,
  "has_more": false
}
```

### Update Task

Update task information or status.

```http
PUT /v1/tasks/{task_id}
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "status": "in_progress",
  "priority": "urgent",
  "estimated_hours": 8,
  "tags": ["proposal", "q4", "urgent", "review"]
}
```

### Delete Task

Delete a task permanently.

```http
DELETE /v1/tasks/{task_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "message": "Task deleted successfully",
  "deleted_at": "2024-01-15T11:45:00Z"
}
```

## Task Status Workflow

Tasks follow a standard workflow:

1. **todo** - Task is created and ready to be worked on
2. **in_progress** - Task is currently being worked on
3. **done** - Task has been completed
4. **cancelled** - Task has been cancelled and won't be completed

## Priority Levels

- **low** - Nice to have, no urgency
- **medium** - Standard priority, normal workflow
- **high** - Important, should be prioritized
- **urgent** - Critical, needs immediate attention

## Error Responses

### Task Not Found
```json
{
  "error": "task_not_found",
  "message": "The requested task does not exist",
  "code": 404
}
```

### Invalid Status Transition
```json
{
  "error": "invalid_status_transition",
  "message": "Cannot change status from 'done' to 'todo'",
  "code": 400
}
```

### Permission Denied
```json
{
  "error": "permission_denied",
  "message": "You don't have permission to modify this task",
  "code": 403
}
```