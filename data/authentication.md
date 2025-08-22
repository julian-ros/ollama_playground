# Authentication

## API Key Authentication

CloudSync API uses API keys for authentication. You can generate and manage your API keys from the CloudSync dashboard.

### Obtaining an API Key

1. Log in to your CloudSync dashboard
2. Navigate to Settings > API Keys
3. Click "Generate New Key"
4. Copy and securely store your API key

### Using API Keys

Include your API key in the `Authorization` header of every request:

```http
GET /v1/files
Authorization: Bearer cs_live_1234567890abcdef
Content-Type: application/json
```

### API Key Types

#### Development Keys
- Prefix: `cs_dev_`
- Limited to 100 requests per hour
- Only work with test data
- Cannot access production files

#### Production Keys
- Prefix: `cs_live_`
- Full rate limits apply
- Access to all account data
- Should be kept secure

### Security Best Practices

1. **Never expose API keys in client-side code**
2. **Use environment variables** to store keys
3. **Rotate keys regularly** (recommended every 90 days)
4. **Use different keys** for different environments
5. **Monitor key usage** in the dashboard

### Key Permissions

API keys can have different permission levels:

- **Read Only**: Can only retrieve data
- **Read/Write**: Can create, update, and delete files
- **Admin**: Full access including user management

### Error Responses

#### Invalid API Key
```json
{
  "error": "invalid_api_key",
  "message": "The provided API key is invalid or has been revoked",
  "code": 401
}
```

#### Expired API Key
```json
{
  "error": "expired_api_key", 
  "message": "The API key has expired. Please generate a new one",
  "code": 401
}
```

#### Rate Limit Exceeded
```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Try again in 3600 seconds",
  "code": 429,
  "retry_after": 3600
}
```