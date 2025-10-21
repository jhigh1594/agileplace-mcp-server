# FastMCP Cloud Deployment Checklist

Use this checklist to deploy the AgilePlace MCP Server to FastMCP Cloud.

## Pre-Deployment Verification

- [x] FastMCP server object created: `mcp = FastMCP("AgilePlace")`
- [x] Tools registered with `@mcp.tool()` decorator
- [x] Dependencies listed in `requirements.txt`
- [x] Environment variables documented
- [x] Repository pushed to GitHub
- [x] README includes deployment instructions

## Server Configuration

| Setting | Value | Status |
|---------|-------|--------|
| **Entrypoint** | `server.py:mcp` | ✅ Configured |
| **FastMCP Version** | `>=0.1.0` | ✅ Compatible |
| **Python Version** | `>=3.10` | ✅ Compatible |
| **Dependencies** | `requirements.txt` | ✅ Available |
| **Main Branch** | `main` | ✅ Set |

## Required Environment Variables

Set these in your FastMCP Cloud project:

| Variable | Description | Example |
|----------|-------------|---------|
| `AGILEPLACE_DOMAIN` | Your AgilePlace domain | `yourcompany.leankit.com` |
| `AGILEPLACE_API_TOKEN` | API token from AgilePlace | `abc123...` |

## Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging verbosity | `INFO` |

## Deployment Steps

### 1. Get AgilePlace API Token
- [ ] Log in to AgilePlace
- [ ] Navigate to: `https://your-subdomain.leankit.com/account/api`
- [ ] Create new API token
- [ ] Copy token to secure location

### 2. Deploy to FastMCP Cloud
- [ ] Visit [fastmcp.cloud](https://fastmcp.cloud)
- [ ] Sign in with GitHub
- [ ] Click **Create Project**
- [ ] Select repository: `jhigh1594/agileplace-mcp-server`
- [ ] Configure project:
  - **Name**: Choose unique name
  - **Entrypoint**: `src/server.py:mcp`
  - **Environment Variables**: Add from step 1
  - **Authentication**: Enable for private use
- [ ] Click **Create Project**
- [ ] Wait for deployment to complete

### 3. Verify Deployment
- [ ] Check deployment logs in FastMCP Cloud
- [ ] Note your server URL: `https://your-project-name.fastmcp.app/mcp`
- [ ] Verify server status shows "Running"

### 4. Connect Claude Desktop
- [ ] Open `claude_desktop_config.json`
- [ ] Add server configuration:
  ```json
  {
    "mcpServers": {
      "agileplace": {
        "url": "https://your-project-name.fastmcp.app/mcp"
      }
    }
  }
  ```
- [ ] Save and restart Claude Desktop

### 5. Test the Server
- [ ] Open Claude Desktop
- [ ] Try command: "List all my AgilePlace boards"
- [ ] Verify boards are returned
- [ ] Test card operations
- [ ] Test connection operations

## Troubleshooting

### Deployment Failed

**Symptom**: Build fails in FastMCP Cloud

**Solutions**:
1. Check deployment logs for specific error
2. Verify `requirements.txt` includes all dependencies
3. Ensure entrypoint is correct: `src/server.py:mcp`
4. Check that environment variables are set

### Authentication Errors

**Symptom**: "Authentication failed" in logs

**Solutions**:
1. Verify `AGILEPLACE_DOMAIN` is correct (no `https://`)
2. Check that `AGILEPLACE_API_TOKEN` is valid
3. Regenerate API token if needed
4. Ensure token has proper permissions

### Connection Issues

**Symptom**: Claude can't connect to server

**Solutions**:
1. Verify server URL in config
2. Check server status in FastMCP Cloud
3. Restart Claude Desktop
4. Check authentication settings

### Rate Limiting

**Symptom**: "Rate limit exceeded" errors

**Solutions**:
1. Server has automatic retry logic
2. Wait 60 seconds between large operations
3. Use bulk operations when possible

## Post-Deployment

### Monitor Your Server
- [ ] Check logs regularly in FastMCP Cloud
- [ ] Monitor error rates
- [ ] Review API usage

### Enable Automatic Updates
- [x] Main branch deployment enabled
- [x] PR preview URLs enabled

### Share with Team
- [ ] Document your server URL
- [ ] Share connection instructions
- [ ] Provide AgilePlace workspace info

## Success Criteria

✅ **Deployment Complete** when:
- Server shows "Running" status in FastMCP Cloud
- Claude Desktop successfully connects
- Can list boards from AgilePlace
- Can create and update cards
- No authentication errors

## Next Steps

After successful deployment:

1. **Test Core Features**
   - Board operations
   - Card CRUD
   - Parent-child connections
   - Dependencies
   - Bulk operations

2. **Document Usage**
   - Share examples with team
   - Document common workflows
   - Create custom prompts

3. **Optimize Performance**
   - Monitor API rate limits
   - Use bulk operations
   - Cache frequently accessed data

4. **Set Up Monitoring**
   - Enable error notifications
   - Track usage patterns
   - Monitor server health

## Support

- FastMCP Cloud: [Discord](https://discord.gg/fastmcp)
- Documentation: [DEPLOY_FASTMCP_CLOUD.md](DEPLOY_FASTMCP_CLOUD.md)
- Issues: [GitHub Issues](https://github.com/jhigh1594/agileplace-mcp-server/issues)

---

**Note**: FastMCP Cloud is free during beta. Take advantage of all features including:
- Automatic updates on push
- PR preview URLs
- Built-in authentication
- Zero server management

