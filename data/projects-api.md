# Projects API

## Overview

The Projects API allows you to create, manage, and organize projects in your Julio workspace.

## Endpoints

### Create Project

Create a new project in your workspace.

```http
POST /v1/projects
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "Q4 Product Launch",
  "description": "Launch the new product features for Q4 2024",
  "status": "active",
  "start_date": "2024-01-15T00:00:00Z",
  "end_date": "2024-03-31T23:59:59Z",
  "team_members": ["user_123", "user_456", "user_789"],
  "tags": ["product", "launch", "q4"]
}
```

**Response:**
```json
{
  "id": "proj_abc123",
  "name": "Q4 Product Launch",
  "description": "Launch the new product features for Q4 2024",
  "status": "active",
  "start_date": "2024-01-15T00:00:00Z",
  "end_date": "2024-03-31T23:59:59Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "owner_id": "user_789",
  "team_members": [
    {
      "id": "user_123",
      "name": "Alice Johnson",
      "role": "developer"
    },
    {
      "id": "user_456", 
      "name": "Bob Wilson",
      "role": "designer"
    }
  ],
  "tags": ["product", "launch", "q4"],
  "task_count": 0,
  "completed_tasks": 0,
  "progress_percentage": 0
}
```

### Get Project Details

Retrieve information about a specific project.

```http
GET /v1/projects/{project_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "id": "proj_abc123",
  "name": "Q4 Product Launch",
  "description": "Launch the new product features for Q4 2024",
  "status": "active",
  "start_date": "2024-01-15T00:00:00Z",
  "end_date": "2024-03-31T23:59:59Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z",
  "owner": {
    "id": "user_789",
    "name": "Carol Davis",
    "email": "carol@company.com"
  },
  "team_members": [
    {
      "id": "user_123",
      "name": "Alice Johnson",
      "email": "alice@company.com",
      "role": "developer"
    }
  ],
  "tags": ["product", "launch", "q4"],
  "task_count": 15,
  "completed_tasks": 8,
  "progress_percentage": 53.3,
  "budget": {
    "allocated": 50000,
    "spent": 23500,
    "currency": "USD"
  }
}
```

### List Projects

Get a list of projects with optional filtering.

```http
GET /v1/projects?status=active&limit=20
Authorization: Bearer YOUR_API_KEY
```

**Query Parameters:**
- `status` (optional): Filter by status (`active`, `completed`, `on_hold`, `cancelled`)
- `owner_id` (optional): Filter by project owner
- `team_member_id` (optional): Filter projects where user is a team member
- `tags` (optional): Filter by tags (comma-separated)
- `start_after` (optional): Filter projects starting after date (ISO 8601)
- `end_before` (optional): Filter projects ending before date (ISO 8601)
- `limit` (optional): Number of projects to return (default: 20, max: 100)
- `offset` (optional): Number of projects to skip (default: 0)
- `sort` (optional): Sort by `created_at`, `updated_at`, `start_date`, or `name`
- `order` (optional): `asc` or `desc` (default: `desc`)

**Response:**
```json
{
  "projects": [
    {
      "id": "proj_abc123",
      "name": "Q4 Product Launch",
      "status": "active",
      "start_date": "2024-01-15T00:00:00Z",
      "end_date": "2024-03-31T23:59:59Z",
      "owner": {
        "id": "user_789",
        "name": "Carol Davis"
      },
      "task_count": 15,
      "progress_percentage": 53.3
    }
  ],
  "total": 8,
  "has_more": false
}
```

### Update Project

Update project information.

```http
PUT /v1/projects/{project_id}
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "Q4 Product Launch - Updated",
  "status": "on_hold",
  "end_date": "2024-04-15T23:59:59Z",
  "team_members": ["user_123", "user_456", "user_789", "user_999"]
}
```

### Delete Project

Delete a project and optionally all its tasks.

```http
DELETE /v1/projects/{project_id}?delete_tasks=true
Authorization: Bearer YOUR_API_KEY
```

**Query Parameters:**
- `delete_tasks` (optional): Delete all project tasks (default: false)

**Response:**
```json
{
  "message": "Project deleted successfully",
  "deleted_tasks": 15,
  "deleted_at": "2024-01-15T11:45:00Z"
}
```

## Project Status Types

- **active** - Project is currently being worked on
- **completed** - Project has been finished successfully
- **on_hold** - Project is temporarily paused
- **cancelled** - Project has been cancelled

## Team Member Roles

- **owner** - Full project control and management
- **manager** - Can manage tasks and team members
- **developer** - Can work on tasks and update progress
- **viewer** - Read-only access to project information

## Error Responses

### Project Not Found
```json
{
  "error": "project_not_found",
  "message": "The requested project does not exist",
  "code": 404
}
```

### Insufficient Permissions
```json
{
  "error": "insufficient_permissions",
  "message": "You don't have permission to modify this project",
  "code": 403
}
```

### Invalid Team Member
```json
{
  "error": "invalid_team_member",
  "message": "One or more team member IDs are invalid",
  "code": 400
}
```