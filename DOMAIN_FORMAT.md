# AgilePlace Domain Format

## Correct Domain Structure

All AgilePlace domains follow this structure:

```
https://yourcompany.leankit.com
```

## Examples

| Company | Correct Domain |
|---------|----------------|
| Acme Corp | `acme.leankit.com` |
| Tech Startup | `techstartup.leankit.com` |
| Enterprise Inc | `enterprise.leankit.com` |

## Environment Variable

When configuring the AgilePlace MCP Server, use:

```bash
AGILEPLACE_DOMAIN=yourcompany.leankit.com
```

**Important Notes:**
- ❌ **DO NOT** use: `yourcompany.agileplace.com`
- ✅ **DO** use: `yourcompany.leankit.com`
- 🔒 Omit the `https://` protocol (it's added automatically)

## API Token Location

Create your API token at:

```
https://yourcompany.leankit.com/account/api
```

## FastMCP Cloud Configuration

When deploying to FastMCP Cloud, set:

| Variable | Example Value |
|----------|---------------|
| `AGILEPLACE_DOMAIN` | `yourcompany.leankit.com` |
| `AGILEPLACE_API_TOKEN` | Your API token from the link above |

## Full Example Configuration

### Local (.env file)
```bash
AGILEPLACE_DOMAIN=acme.leankit.com
AGILEPLACE_API_TOKEN=abc123xyz789...
LOG_LEVEL=INFO
```

### Claude Desktop (local)
```json
{
  "mcpServers": {
    "agileplace": {
      "command": "python",
      "args": ["-m", "agileplace_mcp.server"],
      "env": {
        "AGILEPLACE_DOMAIN": "acme.leankit.com",
        "AGILEPLACE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

### Claude Desktop (FastMCP Cloud)
```json
{
  "mcpServers": {
    "agileplace": {
      "url": "https://your-project-name.fastmcp.app/mcp"
    }
  }
}
```
*(Environment variables configured in FastMCP Cloud project settings)*

## Why leankit.com?

AgilePlace (formerly LeanKit) uses the `leankit.com` domain for all instances. This is the correct and only domain format supported by the AgilePlace API.

## Troubleshooting

If you see authentication errors, verify:
1. ✅ Domain format is `company.leankit.com` (not `company.agileplace.com`)
2. ✅ No `https://` prefix in the environment variable
3. ✅ No trailing slashes
4. ✅ API token is valid and active

## Valid Domain Formats

```bash
# ✅ Correct formats
AGILEPLACE_DOMAIN=mycompany.leankit.com
AGILEPLACE_DOMAIN=my-company.leankit.com
AGILEPLACE_DOMAIN=mycompany123.leankit.com

# ❌ Incorrect formats
AGILEPLACE_DOMAIN=https://mycompany.leankit.com  # No protocol
AGILEPLACE_DOMAIN=mycompany.leankit.com/         # No trailing slash
AGILEPLACE_DOMAIN=mycompany.agileplace.com       # Wrong domain
AGILEPLACE_DOMAIN=mycompany                      # Must include .leankit.com
```

## Getting Your Domain

Your AgilePlace domain is the URL you use to access your AgilePlace workspace:

1. Open your AgilePlace in a browser
2. Look at the URL bar
3. Your domain is everything between `https://` and the next `/`

Example: If you access AgilePlace at `https://acme.leankit.com/board/123`, your domain is `acme.leankit.com`.

