# Sharing API

## Overview

The Sharing API enables you to share files and folders with other users, create public links, and manage access permissions.

## Share Types

### Private Shares
- Share with specific CloudSync users
- Granular permission control
- Access tracking and audit logs

### Public Links
- Generate shareable URLs
- Optional password protection
- Expiration dates
- Download limits

### Team Shares
- Share with entire teams or organizations
- Role-based access control
- Bulk permission management

## Endpoints

### Create Share

Share a file or folder with users or create a public link.

```http
POST /v1/shares
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "resource_type": "file",
  "resource_id": "file_abc123",
  "share_type": "private",
  "recipients": [
    {
      "email": "john@example.com",
      "permission": "read"
    },
    {
      "email": "jane@example.com", 
      "permission": "edit"
    }
  ],
  "message": "Please review this document",
  "expires_at": "2024-02-15T10:30:00Z"
}
```

**Response:**
```json
{
  "id": "share_def456",
  "resource_type": "file",
  "resource_id": "file_abc123",
  "share_type": "private",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-02-15T10:30:00Z",
  "recipients": [
    {
      "email": "john@example.com",
      "permission": "read",
      "status": "pending"
    },
    {
      "email": "jane@example.com",
      "permission": "edit", 
      "status": "accepted"
    }
  ],
  "stats": {
    "views": 0,
    "downloads": 0,
    "last_accessed": null
  }
}
```

### Create Public Link

Generate a public shareable link.

```http
POST /v1/shares/public
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "resource_type": "folder",
  "resource_id": "folder_xyz789",
  "password": "secure123",
  "expires_at": "2024-02-15T10:30:00Z",
  "download_limit": 100,
  "allow_upload": false
}
```

**Response:**
```json
{
  "id": "share_pub789",
  "public_url": "https://cloudsync.com/s/abc123def456",
  "short_url": "https://cs.ly/x7k9m",
  "resource_type": "folder",
  "resource_id": "folder_xyz789",
  "password_protected": true,
  "expires_at": "2024-02-15T10:30:00Z",
  "download_limit": 100,
  "downloads_used": 0,
  "allow_upload": false,
  "created_at": "2024-01-15T10:30:00Z",
  "stats": {
    "views": 0,
    "downloads": 0,
    "unique_visitors": 0
  }
}
```

### List Shares

Get all shares created by the authenticated user.

```http
GET /v1/shares?resource_type=file&status=active
Authorization: Bearer YOUR_API_KEY
```

**Query Parameters:**
- `resource_type` (optional): Filter by `file` or `folder`
- `share_type` (optional): Filter by `private` or `public`
- `status` (optional): Filter by `active`, `expired`, or `revoked`
- `limit` (optional): Number of shares to return (default: 50)
- `offset` (optional): Number of shares to skip (default: 0)

**Response:**
```json
{
  "shares": [
    {
      "id": "share_def456",
      "resource_type": "file",
      "resource_name": "report.pdf",
      "share_type": "private",
      "recipient_count": 2,
      "created_at": "2024-01-15T10:30:00Z",
      "expires_at": "2024-02-15T10:30:00Z",
      "status": "active"
    }
  ],
  "total": 25,
  "has_more": false
}
```

### Get Share Details

Retrieve detailed information about a specific share.

```http
GET /v1/shares/{share_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "id": "share_def456",
  "resource_type": "file",
  "resource_id": "file_abc123",
  "resource_name": "report.pdf",
  "share_type": "private",
  "created_at": "2024-01-15T10:30:00Z",
  "expires_at": "2024-02-15T10:30:00Z",
  "status": "active",
  "recipients": [
    {
      "email": "john@example.com",
      "permission": "read",
      "status": "accepted",
      "accepted_at": "2024-01-15T11:00:00Z",
      "last_accessed": "2024-01-16T09:30:00Z"
    }
  ],
  "stats": {
    "views": 15,
    "downloads": 3,
    "last_accessed": "2024-01-16T09:30:00Z",
    "access_log": [
      {
        "email": "john@example.com",
        "action": "view",
        "timestamp": "2024-01-16T09:30:00Z",
        "ip_address": "192.168.1.100"
      }
    ]
  }
}
```

### Update Share

Modify share settings or permissions.

```http
PUT /v1/shares/{share_id}
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "expires_at": "2024-03-15T10:30:00Z",
  "recipients": [
    {
      "email": "john@example.com",
      "permission": "edit"
    }
  ]
}
```

### Revoke Share

Revoke access to a share.

```http
DELETE /v1/shares/{share_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "message": "Share revoked successfully",
  "revoked_at": "2024-01-15T11:45:00Z"
}
```

## Permission Levels

### File Permissions
- **read**: View and download the file
- **edit**: View, download, and replace file content
- **comment**: View, download, and add comments

### Folder Permissions  
- **read**: View folder contents and download files
- **edit**: Full access to add, edit, and delete files
- **upload**: Can upload new files but not modify existing ones

## Share Settings

### Security Options
- Password protection for public links
- IP address restrictions
- Domain restrictions (enterprise only)
- Two-factor authentication requirements

### Access Controls
- Expiration dates
- Download limits
- View-only restrictions
- Watermarking (enterprise only)

### Notifications
- Email notifications for share access
- Real-time activity alerts
- Weekly access reports

## Error Responses

### Share Not Found
```json
{
  "error": "share_not_found",
  "message": "The requested share does not exist or has been revoked",
  "code": 404
}
```

### Share Expired
```json
{
  "error": "share_expired",
  "message": "This share has expired",
  "code": 410
}
```

### Permission Denied
```json
{
  "error": "permission_denied",
  "message": "You don't have permission to access this resource",
  "code": 403
}
```