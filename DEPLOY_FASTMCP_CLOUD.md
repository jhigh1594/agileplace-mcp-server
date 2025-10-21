# Deploying to FastMCP Cloud

This guide walks you through deploying the AgilePlace MCP Server to [FastMCP Cloud](https://fastmcp.cloud), the fastest way to host your MCP server.

## Why FastMCP Cloud?

FastMCP Cloud is a managed hosting platform specifically built for MCP servers. Benefits include:

- ⚡ **Instant Deployment** - Deploy from GitHub in seconds
- 🔄 **Auto-Updates** - Automatic redeployment on every push to main
- 🧪 **PR Previews** - Test changes with unique URLs for each pull request
- 🔒 **Built-in Auth** - Optional authentication for private servers
- 🆓 **Free Beta** - Completely free while in beta!

## Prerequisites

1. **GitHub Account** - Sign in to FastMCP Cloud with GitHub
2. **AgilePlace Credentials**:
   - Your AgilePlace subdomain (e.g., `yourcompany.agileplace.com`)
   - API token from: `https://yourcompany.agileplace.com/account/api`

## Deployment Steps

### Step 1: Fork or Clone the Repository

If you haven't already, ensure the AgilePlace MCP Server is in a GitHub repository:

```bash
git clone https://github.com/jhigh1594/agileplace-mcp-server.git
cd agileplace-mcp-server
```

Or fork the repository to your own GitHub account.

### Step 2: Sign In to FastMCP Cloud

1. Visit [fastmcp.cloud](https://fastmcp.cloud)
2. Click **Sign in with GitHub**
3. Authorize FastMCP Cloud to access your repositories

### Step 3: Create a New Project

1. Click **Create Project**
2. Select your repository:
   - Choose from your own repos
   - Or use `jhigh1594/agileplace-mcp-server` as a starting point

### Step 4: Configure Your Project

Fill in the configuration settings:

#### **Name**
Choose a unique name for your project (e.g., `agileplace-prod`)
- This generates your server URL: `https://your-name.fastmcp.app/mcp`

#### **Entrypoint**
```
src/server.py:mcp
```
This tells FastMCP Cloud:
- File: `src/server.py`
- Object: `mcp` (the FastMCP instance)

#### **Environment Variables**
FastMCP Cloud will prompt you to set environment variables. Add:

| Variable | Value | Example |
|----------|-------|---------|
| `AGILEPLACE_DOMAIN` | Your AgilePlace subdomain | `yourcompany.agileplace.com` |
| `AGILEPLACE_API_TOKEN` | Your API token | `abc123...` |
| `LOG_LEVEL` (optional) | Logging level | `INFO` |

#### **Authentication**
- **Disabled (Public)**: Anyone with the URL can connect
- **Enabled (Private)**: Only your FastMCP Cloud organization members can connect

Recommendation: Enable authentication if your AgilePlace data is sensitive.

### Step 5: Deploy

1. Click **Create Project**
2. FastMCP Cloud will:
   - Clone your repository
   - Install dependencies from `requirements.txt` or `pyproject.toml`
   - Build and deploy your server
   - Generate a unique URL

Your server will be live at:
```
https://your-project-name.fastmcp.app/mcp
```

## Connecting to Your Server

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agileplace": {
      "url": "https://your-project-name.fastmcp.app/mcp"
    }
  }
}
```

**Note**: No `env` section needed! Environment variables are configured on FastMCP Cloud.

### Other MCP Clients

Use the server URL directly:
```
https://your-project-name.fastmcp.app/mcp
```

## Automatic Updates

FastMCP Cloud monitors your GitHub repository:

- **Main Branch**: Every push to `main` triggers automatic redeployment
- **Pull Requests**: Each PR gets its own preview URL for testing
- **No Downtime**: Deployments are seamless with zero downtime

## Testing Your Deployment

1. Open Claude Desktop
2. Start a new conversation
3. Try a command:
   > "List all my AgilePlace boards"

If successful, you'll see your boards! 🎉

## Verifying Server Configuration

Before deploying, you can inspect your server locally:

```bash
# Install FastMCP CLI
pip install fastmcp

# Inspect your server configuration
fastmcp inspect src/server.py:mcp
```

This shows exactly what FastMCP Cloud will see when it runs your server.

## Managing Your Deployment

### View Logs

In FastMCP Cloud:
1. Go to your project
2. Click **Logs** tab
3. View real-time server logs

### Update Environment Variables

1. Go to your project settings
2. Update environment variables
3. Server automatically redeploys

### Roll Back

1. View deployment history
2. Select a previous deployment
3. Click **Rollback**

## Troubleshooting

### "Authentication failed"
- Verify `AGILEPLACE_DOMAIN` is correct (no `https://`)
- Check that your API token is valid
- Ensure environment variables are set in FastMCP Cloud

### "Server not responding"
- Check deployment logs in FastMCP Cloud
- Verify all dependencies are in `requirements.txt` or `pyproject.toml`
- Ensure Python 3.10+ is specified in your project

### "Rate limit exceeded"
- The server has built-in rate limit handling
- Check if you're making too many requests
- Consider implementing request caching in your client

### "Module not found"
- Ensure all dependencies are listed in `requirements.txt`
- Check that the entrypoint path is correct: `src/server.py:mcp`
- Verify the project structure matches the repository

## Development Workflow

### Testing Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/new-tool
   ```

2. Make your changes to the code

3. Commit and push:
   ```bash
   git add .
   git commit -m "feat: Add new tool for X"
   git push origin feature/new-tool
   ```

4. Open a pull request on GitHub

5. FastMCP Cloud creates a preview URL:
   ```
   https://your-project-name-pr-123.fastmcp.app/mcp
   ```

6. Test the preview URL with your changes

7. Merge to main when ready
   - FastMCP Cloud automatically deploys to production

### Local Development

Test locally before pushing:

```bash
# Set environment variables
export AGILEPLACE_DOMAIN="yourcompany.agileplace.com"
export AGILEPLACE_API_TOKEN="your_token"

# Run the server
python -m agileplace_mcp.server
```

## Multiple Environments

You can deploy multiple instances for different purposes:

| Project Name | Branch | Environment | Use Case |
|-------------|--------|-------------|----------|
| `agileplace-prod` | `main` | Production | Live server for daily use |
| `agileplace-staging` | `staging` | Staging | Testing before production |
| `agileplace-dev` | `develop` | Development | Experimental features |

Each gets its own URL and environment variables.

## Best Practices

1. **Use Authentication** - Enable auth for production deployments
2. **Separate Tokens** - Use different API tokens for dev/staging/prod
3. **Monitor Logs** - Regularly check FastMCP Cloud logs
4. **Tag Releases** - Use git tags for important versions
5. **Test in PRs** - Use preview URLs to test before merging
6. **Document Changes** - Keep CHANGELOG.md updated

## Cost & Limits

FastMCP Cloud is currently **free during beta**!

Current limits (subject to change):
- Unlimited requests
- No bandwidth caps
- Generous rate limits
- Free for personal and commercial use

## Support

- **FastMCP Cloud**: [Discord Community](https://discord.gg/fastmcp)
- **AgilePlace MCP**: [GitHub Issues](https://github.com/jhigh1594/agileplace-mcp-server/issues)
- **FastMCP Docs**: [gofastmcp.com](https://gofastmcp.com)

## Next Steps

- ✅ Deploy to FastMCP Cloud
- 📊 Monitor your deployment
- 🔄 Set up automatic updates
- 🧪 Test with preview URLs
- 🚀 Share your server with your team

Happy deploying! 🎉

