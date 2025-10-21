# AgilePlace MCP Server

A comprehensive Model Context Protocol (MCP) server for the AgilePlace API, built with FastMCP. This server enables AI assistants like Claude to interact with AgilePlace for project management tasks.

## Features

### Core Capabilities

- **Board Management**: List, view, create, and manage boards
- **Card Operations**: Full CRUD operations on cards with rich metadata
- **Parent-Child Connections**: Manage hierarchical card relationships
- **Dependencies**: Create and manage card dependencies with multiple types
- **Bulk Operations**: Efficiently update, move, or delete multiple cards
- **User & Team Queries**: Search and retrieve user and team information
- **Comments & Attachments**: Manage card comments and attachments
- **Rate Limiting**: Automatic handling with exponential backoff

### Supported Operations

#### Boards
- List boards with search and filtering
- Get detailed board information
- Create new boards from scratch or templates
- Get board cards, lanes, and members
- View board activity history

#### Cards
- List and search cards across boards
- Get full card details
- Create, update, move, and delete cards
- Manage card metadata (tags, priorities, sizes)
- View card activity history
- Assign users and teams to cards

#### Connections
- Get card children and parents
- Create and delete parent-child connections
- Bulk connection operations
- View connection statistics

#### Dependencies
- Create card dependencies (finish-to-start, start-to-start, etc.)
- View all card dependencies
- Update and delete dependencies

#### Bulk Operations
- Update multiple cards at once
- Move cards in bulk
- Delete multiple cards
- Assign members to multiple boards

## Installation

### Prerequisites

- Python 3.10 or higher
- AgilePlace account with API access
- API token (create at: `https://your-subdomain.agileplace.com/account/api`)

### Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd agileplace_mcp

# Install dependencies
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Configuration

### Environment Variables

Create a `.env` file in your project directory or set environment variables:

```bash
# Your AgilePlace subdomain (e.g., mycompany.agileplace.com)
AGILEPLACE_DOMAIN=your-subdomain.agileplace.com

# Your AgilePlace API token
AGILEPLACE_API_TOKEN=your_token_here

# Optional: Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO
```

### MCP Client Configuration

#### Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "agileplace": {
      "command": "python",
      "args": ["-m", "agileplace_mcp.server"],
      "env": {
        "AGILEPLACE_DOMAIN": "your-subdomain.agileplace.com",
        "AGILEPLACE_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Other MCP Clients

For other MCP clients, use the same configuration pattern with the appropriate format for that client.

## Usage Examples

### Basic Board Operations

```python
# List all boards
boards = await list_boards(search="project")

# Get board details
board = await get_board(board_id="123456")

# Get cards on a board
cards = await get_board_cards(board_id="123456", limit=50)
```

### Card Operations

```python
# Create a new card
card = await create_card(
    board_id="123456",
    lane_id="lane789",
    title="Implement new feature",
    description="Detailed description here",
    priority="high",
    size=5,
    tags=["backend", "api"]
)

# Update a card
updated = await update_card(
    card_id="card123",
    title="Updated title",
    priority="critical"
)

# Move a card to a different lane
moved = await move_card(
    card_id="card123",
    lane_id="lane456",
    position=0  # Top of the lane
)

# Delete a card
await delete_card(card_id="card123")
```

### Parent-Child Connections

```python
# Create a parent-child relationship
connection = await create_connection(
    parent_id="parent123",
    child_id="child456"
)

# Get all children of a card
children = await get_card_children(card_id="parent123")

# Get connection statistics
stats = await get_connection_statistics(card_id="parent123")
print(f"Total children: {stats['totalCount']}")
print(f"Completed: {stats['completedCount']}")
```

### Card Dependencies

```python
# Create a dependency (card456 depends on card123 finishing)
dependency = await create_dependency(
    card_id="card456",
    depends_on_card_id="card123",
    dependency_type="finish_to_start"
)

# Get all dependencies for a card
deps = await get_card_dependencies(card_id="card456")

# Delete a dependency
await delete_dependency(dependency_id="dep123")
```

### Bulk Operations

```python
# Update multiple cards at once
result = await update_cards_bulk(
    card_ids=["card1", "card2", "card3"],
    updates={
        "priority": "high",
        "tags": "urgent,review"
    }
)

# Move multiple cards
moves = [
    {"cardId": "card1", "laneId": "lane1"},
    {"cardId": "card2", "laneId": "lane2"},
    {"cardId": "card3", "laneId": "lane1"}
]
await move_cards_bulk(moves)

# Assign users to multiple boards
await assign_members_bulk(
    board_ids=["board1", "board2"],
    user_ids=["user1", "user2"],
    board_role="boardUser"
)
```

### User and Team Queries

```python
# Search for users
users = await list_users(search="john", limit=10)

# Get current user info
me = await get_current_user()

# List teams
teams = await list_teams(search="engineering")

# Get team details
team = await get_team(team_id="team123")
```

## AI Assistant Usage

When using with Claude or other AI assistants, you can ask natural language questions:

- "List all boards in AgilePlace"
- "Show me cards on the 'Q1 Projects' board"
- "Create a new card titled 'Fix login bug' in the Backlog lane on board 123"
- "Move card 456 to the 'In Progress' lane"
- "What are the children of card 789?"
- "Create a dependency where card 456 depends on card 123 finishing"
- "Update all cards with tag 'urgent' to high priority"

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_cards.py
```

### Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Type checking
mypy src
```

## Rate Limiting

The AgilePlace API implements rate limiting. This server automatically handles rate limits with:

- Exponential backoff on 429 responses
- Configurable retry attempts (default: 3)
- Rate limit header monitoring
- Automatic retry after cooldown period

## Error Handling

The server provides comprehensive error handling:

- **Authentication Errors**: Clear messages for missing or invalid credentials
- **Rate Limit Errors**: Automatic retry with cooldown
- **API Errors**: Detailed error messages with status codes
- **Network Errors**: Retry logic for transient failures

## Security Best Practices

1. **Store credentials securely**: Use environment variables, never commit API tokens
2. **Use Bearer tokens**: Prefer API tokens over basic authentication
3. **Rotate tokens regularly**: Create new tokens and revoke old ones periodically
4. **Limit token scope**: Use separate tokens for different integrations
5. **Monitor usage**: Review API usage and rate limit metrics

## API Documentation

For detailed AgilePlace API documentation, see:
- [AgilePlace API Docs](https://success.planview.com/Planview_AgilePlace/API)

## Troubleshooting

### Authentication Errors

```
AgilePlaceAuthError: AGILEPLACE_DOMAIN environment variable is required
```

**Solution**: Ensure environment variables are set correctly. Check `.env` file or MCP client configuration.

### Rate Limiting

```
Rate limit exceeded. Please try again later.
```

**Solution**: The server will automatically retry. If persistent, reduce request frequency or contact AgilePlace support to increase limits.

### Connection Errors

```
API Error (500): Internal server error
```

**Solution**: Check AgilePlace service status. If persistent, verify your domain and API token are correct.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run the test suite and linters
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [repository-url]/issues
- AgilePlace Support: https://success.planview.com/

## Changelog

### Version 0.1.0 (Initial Release)

- Board management operations
- Full card CRUD operations
- Parent-child connection management
- Dependency management
- Bulk operations
- User and team queries
- Comprehensive error handling
- Rate limiting with automatic retry
- FastMCP integration

