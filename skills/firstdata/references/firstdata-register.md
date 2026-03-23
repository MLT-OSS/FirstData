**Base URL:** `https://firstdata.deepminer.com.cn`

## Quick Flow

The registration flow has two steps:

```text
POST /api/agent/register  ->  receive inactive access_token + verification challenge
POST /api/agent/verify    ->  submit answer and activate the token
```

Use the activated `access_token` as `FIRSTDATA_API_KEY` after verification succeeds.

## Step 1: Register

Send a POST request to register the agent and receive a verification challenge:

```http
POST https://firstdata.deepminer.com.cn/api/agent/register
Content-Type: application/json

{
  "agent_id": "my-unique-agent-name",
  "contact_email": "owner@example.com",
  "description": "Data analysis agent for quarterly reports"
}
```

Key fields:

| Field             | Required | Description                                                               |
| ----------------- | -------- | ------------------------------------------------------------------------- |
| `agent_id`      | Yes      | Globally unique identifier (max 100 chars). Acts as the agent's username. |
| `contact_email` | No       | Owner's email for contact purposes                                        |
| `description`   | Yes      | Brief description of the agent's purpose (max 500 chars)                  |

**Success response** (`success: true`):

```json
{
  "success": true,
  "data": {
    "agent_id": "my-unique-agent-name",
    "access_token": "eyJhbGciOi...<JWT>",
    "verification": {
      "verification_code": "a1b2c3d4-...",
      "challenge_text": "...",
      "expires_at": "2025-01-15T10:05:00",
      "instructions": "..."
    }
  }
}
```

Save both `access_token` and `verification.verification_code`. The token is returned immediately but is not usable until verification succeeds.

## Step 2: Solve the Challenge and Verify

Read `verification.challenge_text`, follow `verification.instructions`, solve the math challenge, and submit the answer:

```http
POST https://firstdata.deepminer.com.cn/api/agent/verify
Content-Type: application/json

{
  "verification_code": "a1b2c3d4-...",
  "answer": "your answer here"
}
```

Success response:

```json
{
  "success": true,
  "message": "验证成功，token 已激活",
  "mcp_server_url": "https://mcp.firstdata.deepminer.com.cn"
}
```

After this step, the `access_token` from Step 1 becomes active. If `mcp_server_url` is returned, use it as the MCP endpoint.

## After Activation

- Use the activated `access_token` as `FIRSTDATA_API_KEY`
- Connect with `Authorization: Bearer <FIRSTDATA_API_KEY>`
- The token is a JWT and is valid for **365 days** by default

Rate limits:

- **RPS limit:** 10 requests per second
- **Daily quota:** 5000 requests per day

## Error Handling

| Scenario                                          | What happens                                                 | Action                                                                   |
| ------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `agent_id` already registered with active token | Registration returns `success: false`                      | Choose a different `agent_id` or wait for the existing token to expire |
| Pending verification exists for this `agent_id` | Registration returns `success: false`                      | Complete the existing verification or wait for it to expire              |
| Wrong answer                                      | Verify returns `success: false` with remaining attempts    | Re-read the challenge carefully and try again                            |
| All attempts exhausted                            | Verify returns `success: false`, status becomes `failed` | Start over with a new `/api/agent/register` call                       |
| Challenge expired                                 | Verify returns `success: false`                            | Start over with a new `/api/agent/register` call                       |
| IP rate limited                                   | HTTP 429                                                     | Wait before retrying                                                     |

## MCP Configuration

After activation, configure the MCP connection using either method:

**Option 1: MCPorter CLI (recommended)**

```bash
npx mcporter config add firstdata https://firstdata.deepminer.com.cn/mcp --header 'Authorization=Bearer ${FIRSTDATA_API_KEY}'
```

**Option 2: Manual MCP configuration**

```json
{
  "mcpServers": {
    "firstdata": {
      "type": "streamable-http",
      "url": "https://firstdata.deepminer.com.cn/mcp",
      "headers": {
        "Authorization": "Bearer <FIRSTDATA_API_KEY>"
      }
    }
  }
}
```

`FIRSTDATA_API_KEY` should be set to the activated `access_token`.
