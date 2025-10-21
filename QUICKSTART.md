# Quick Start Guide - AgilePlace MCP Server

Get up and running with the AgilePlace MCP Server in 5 minutes!

## Two Ways to Get Started

1. **FastMCP Cloud** (Recommended) - Deploy in seconds, zero config
2. **Local Installation** - Run on your own machine

## Prerequisites

- Python 3.10 or higher
- AgilePlace account with API access
- Claude Desktop (or another MCP-compatible client)

---

## Option 1: FastMCP Cloud (Fastest) ⚡

### Step 1: Get Your AgilePlace API Token

1. Log in to your AgilePlace account
2. Navigate to: `https://your-subdomain.leankit.com/account/api`
3. Click "Create Token"
4. Give it a description (e.g., "MCP Server")
5. Copy the generated token

### Step 2: Deploy to FastMCP Cloud

1. Visit [fastmcp.cloud](https://fastmcp.cloud)
2. Sign in with GitHub
3. Click **Create Project**
4. Select repository: `jhigh1594/agileplace-mcp-server`
5. Configure:
   - **Name**: `agileplace` (or your choice)
   - **Entrypoint**: `server.py:mcp`
   - **Environment Variables**:
     - `AGILEPLACE_DOMAIN`: `your-subdomain.leankit.com`
     - `AGILEPLACE_API_TOKEN`: *paste your token*
6. Click **Create Project**

Your server will be live at: `https://your-project-name.fastmcp.app/mcp`

### Step 3: Configure Claude Desktop

1. Open `claude_desktop_config.json`
2. Add:

```json
{
  "mcpServers": {
    "agileplace": {
      "url": "https://your-project-name.fastmcp.app/mcp"
    }
  }
}
```

3. Save and restart Claude Desktop

**Done!** Skip to [Step 5: Verify It's Working](#step-5-verify-its-working)

---

## Option 2: Local Installation

### Step 1: Get Your AgilePlace API Token

1. Log in to your AgilePlace account
2. Navigate to: `https://your-subdomain.leankit.com/account/api`
3. Click "Create Token"
4. Give it a description (e.g., "MCP Server")
5. Copy the generated token

### Step 2: Install the MCP Server

```bash
# Clone the repository
git clone https://github.com/jhigh1594/agileplace-mcp-server.git
cd agileplace-mcp-server

# Install the package
pip install -e .
```

### Step 3: Configure Claude Desktop

1. Open your Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the AgilePlace MCP server configuration:

```json
{
  "mcpServers": {
    "agileplace": {
      "command": "python",
      "args": ["-m", "agileplace_mcp.server"],
      "env": {
        "AGILEPLACE_DOMAIN": "your-subdomain.leankit.com",
        "AGILEPLACE_API_TOKEN": "paste_your_token_here"
      }
    }
  }
}
```

3. Replace `your-subdomain` with your actual AgilePlace domain
4. Replace `paste_your_token_here` with your API token from Step 1
5. Save the file

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop to load the new MCP server.

---

## Step 5: Verify It's Working

In Claude Desktop, try asking:

> "List all my AgilePlace boards"

If successful, Claude will show you a list of your boards!

## Example Queries to Try

### View Boards
- "Show me all boards in AgilePlace"
- "Get details about board [board_id]"
- "What are the lanes on board [board_id]?"

### Work with Cards
- "List cards on the 'Q1 Projects' board"
- "Create a new card titled 'Fix login bug' in the Backlog lane on board [board_id]"
- "Show me details of card [card_id]"
- "Move card [card_id] to the 'In Progress' lane"
- "Update card [card_id] to high priority"

### Manage Connections
- "Show me the children of card [card_id]"
- "Create a parent-child connection between card [parent_id] and card [child_id]"
- "What are the parents of card [card_id]?"

### Dependencies
- "Create a dependency where card [card_id] depends on card [other_card_id] finishing"
- "Show me all dependencies for card [card_id]"

### Users and Teams
- "Find users with 'john' in their name"
- "List all teams"
- "Who is assigned to board [board_id]?"

### Bulk Operations
- "Update cards [id1], [id2], [id3] to high priority"
- "Move cards [id1] and [id2] to lane [lane_id]"

## Troubleshooting

### "Authentication failed"
- Check your `AGILEPLACE_DOMAIN` is correct (without https://)
- Verify your API token is valid
- Make sure environment variables are in the correct format

### "Rate limit exceeded"
- The server will automatically retry
- If persistent, reduce request frequency

### "Can't connect to server"
- Restart Claude Desktop
- Check that Python is in your PATH
- Verify the package is installed: `pip list | grep agileplace-mcp`

## Next Steps

- Read the [full README](README.md) for detailed documentation
- Explore the [API documentation](https://success.planview.com/Planview_AgilePlace/API)
- Check out [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details

## Need Help?

- Check the [README](README.md) troubleshooting section
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
- Open an issue on GitHub

Happy project managing! 🚀

