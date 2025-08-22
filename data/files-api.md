# Files API

## Overview

The Files API allows you to upload, download, manage, and organize files in your CloudSync storage.

## Endpoints

### Upload File

Upload a new file to CloudSync storage.

```http
POST /v1/files
Authorization: Bearer YOUR_API_KEY
Content-Type: multipart/form-data

{
  "file": [binary file data],
  "folder_id": "folder_123",
  "description": "Monthly report for Q4"
}
```

**Response:**
```json
{
  "id": "file_abc123",
  "name": "report.pdf",
  "size": 2048576,
  "mime_type": "application/pdf",
  "folder_id": "folder_123",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "download_url": "https://cdn.cloudsync.com/files/file_abc123",
  "thumbnail_url": "https://cdn.cloudsync.com/thumbnails/file_abc123"
}
```

### Get File Details

Retrieve metadata for a specific file.

```http
GET /v1/files/{file_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "id": "file_abc123",
  "name": "report.pdf",
  "size": 2048576,
  "mime_type": "application/pdf",
  "folder_id": "folder_123",
  "description": "Monthly report for Q4",
  "tags": ["report", "q4", "finance"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "version": 1,
  "download_url": "https://cdn.cloudsync.com/files/file_abc123",
  "thumbnail_url": "https://cdn.cloudsync.com/thumbnails/file_abc123",
  "shared": false,
  "permissions": {
    "can_edit": true,
    "can_delete": true,
    "can_share": true
  }
}
```

### List Files

Get a list of files in your storage or a specific folder.

```http
GET /v1/files?folder_id=folder_123&limit=50&offset=0
Authorization: Bearer YOUR_API_KEY
```

**Query Parameters:**
- `folder_id` (optional): Filter files by folder
- `limit` (optional): Number of files to return (default: 50, max: 100)
- `offset` (optional): Number of files to skip (default: 0)
- `search` (optional): Search files by name or content
- `mime_type` (optional): Filter by file type
- `sort` (optional): Sort by `name`, `size`, `created_at`, or `updated_at`
- `order` (optional): `asc` or `desc` (default: `desc`)

**Response:**
```json
{
  "files": [
    {
      "id": "file_abc123",
      "name": "report.pdf",
      "size": 2048576,
      "mime_type": "application/pdf",
      "created_at": "2024-01-15T10:30:00Z",
      "thumbnail_url": "https://cdn.cloudsync.com/thumbnails/file_abc123"
    }
  ],
  "total": 150,
  "has_more": true,
  "next_offset": 50
}
```

### Update File

Update file metadata or replace file content.

```http
PUT /v1/files/{file_id}
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "name": "updated-report.pdf",
  "description": "Updated monthly report for Q4",
  "tags": ["report", "q4", "finance", "updated"],
  "folder_id": "folder_456"
}
```

### Delete File

Permanently delete a file.

```http
DELETE /v1/files/{file_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "message": "File deleted successfully",
  "deleted_at": "2024-01-15T11:45:00Z"
}
```

### Download File

Get a temporary download URL for a file.

```http
GET /v1/files/{file_id}/download
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "download_url": "https://cdn.cloudsync.com/download/temp_xyz789?expires=1642248300",
  "expires_at": "2024-01-15T12:45:00Z"
}
```

## File Versions

### List File Versions

```http
GET /v1/files/{file_id}/versions
Authorization: Bearer YOUR_API_KEY
```

### Restore File Version

```http
POST /v1/files/{file_id}/versions/{version_id}/restore
Authorization: Bearer YOUR_API_KEY
```

## Error Responses

### File Not Found
```json
{
  "error": "file_not_found",
  "message": "The requested file does not exist",
  "code": 404
}
```

### File Too Large
```json
{
  "error": "file_too_large",
  "message": "File size exceeds the maximum limit of 5GB",
  "code": 413
}
```

### Insufficient Storage
```json
{
  "error": "insufficient_storage",
  "message": "Not enough storage space available",
  "code": 507
}
```