# Folders API

## Overview

The Folders API allows you to create, manage, and organize folders in your CloudSync storage hierarchy.

## Endpoints

### Create Folder

Create a new folder in your storage.

```http
POST /v1/folders
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "Project Documents",
  "parent_id": "folder_root",
  "description": "All documents related to the current project"
}
```

**Response:**
```json
{
  "id": "folder_xyz789",
  "name": "Project Documents",
  "parent_id": "folder_root",
  "description": "All documents related to the current project",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "file_count": 0,
  "folder_count": 0,
  "total_size": 0,
  "path": "/Project Documents",
  "permissions": {
    "can_edit": true,
    "can_delete": true,
    "can_share": true
  }
}
```

### Get Folder Details

Retrieve information about a specific folder.

```http
GET /v1/folders/{folder_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "id": "folder_xyz789",
  "name": "Project Documents",
  "parent_id": "folder_root",
  "description": "All documents related to the current project",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "file_count": 25,
  "folder_count": 3,
  "total_size": 52428800,
  "path": "/Project Documents",
  "shared": false,
  "permissions": {
    "can_edit": true,
    "can_delete": true,
    "can_share": true
  }
}
```

### List Folders

Get a list of folders, optionally filtered by parent folder.

```http
GET /v1/folders?parent_id=folder_root&limit=50
Authorization: Bearer YOUR_API_KEY
```

**Query Parameters:**
- `parent_id` (optional): Filter by parent folder (default: root)
- `limit` (optional): Number of folders to return (default: 50, max: 100)
- `offset` (optional): Number of folders to skip (default: 0)
- `search` (optional): Search folders by name
- `sort` (optional): Sort by `name`, `created_at`, or `updated_at`
- `order` (optional): `asc` or `desc` (default: `asc`)

**Response:**
```json
{
  "folders": [
    {
      "id": "folder_xyz789",
      "name": "Project Documents",
      "parent_id": "folder_root",
      "created_at": "2024-01-15T10:30:00Z",
      "file_count": 25,
      "folder_count": 3,
      "total_size": 52428800
    }
  ],
  "total": 10,
  "has_more": false
}
```

### Update Folder

Update folder metadata.

```http
PUT /v1/folders/{folder_id}
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "Updated Project Documents",
  "description": "Updated description for project documents",
  "parent_id": "folder_archive"
}
```

### Delete Folder

Delete a folder and optionally all its contents.

```http
DELETE /v1/folders/{folder_id}?recursive=true
Authorization: Bearer YOUR_API_KEY
```

**Query Parameters:**
- `recursive` (optional): Delete folder contents recursively (default: false)

**Response:**
```json
{
  "message": "Folder deleted successfully",
  "deleted_files": 25,
  "deleted_folders": 3,
  "deleted_at": "2024-01-15T11:45:00Z"
}
```

### Get Folder Contents

Get both files and subfolders within a folder.

```http
GET /v1/folders/{folder_id}/contents
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "folder": {
    "id": "folder_xyz789",
    "name": "Project Documents",
    "path": "/Project Documents"
  },
  "folders": [
    {
      "id": "folder_sub1",
      "name": "Contracts",
      "file_count": 5,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "files": [
    {
      "id": "file_abc123",
      "name": "project-plan.pdf",
      "size": 2048576,
      "mime_type": "application/pdf",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Move Folder

Move a folder to a different parent folder.

```http
POST /v1/folders/{folder_id}/move
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "parent_id": "folder_archive"
}
```

### Copy Folder

Create a copy of a folder and its contents.

```http
POST /v1/folders/{folder_id}/copy
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "Copy of Project Documents",
  "parent_id": "folder_backup"
}
```

## Folder Hierarchy

### Get Folder Path

Get the full path hierarchy for a folder.

```http
GET /v1/folders/{folder_id}/path
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "path": [
    {
      "id": "folder_root",
      "name": "Root"
    },
    {
      "id": "folder_projects",
      "name": "Projects"
    },
    {
      "id": "folder_xyz789",
      "name": "Project Documents"
    }
  ],
  "full_path": "/Projects/Project Documents"
}
```

## Error Responses

### Folder Not Found
```json
{
  "error": "folder_not_found",
  "message": "The requested folder does not exist",
  "code": 404
}
```

### Folder Not Empty
```json
{
  "error": "folder_not_empty",
  "message": "Cannot delete folder that contains files or subfolders",
  "code": 409
}
```

### Invalid Parent Folder
```json
{
  "error": "invalid_parent",
  "message": "Cannot move folder to its own subfolder",
  "code": 400
}
```