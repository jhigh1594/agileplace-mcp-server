# Changelog

All notable changes to the AgilePlace MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-10-21

### Added

#### Core Infrastructure
- FastMCP-based server implementation with 40+ tools
- Environment variable-based authentication (Bearer token)
- Async HTTP client with automatic rate limiting
- Exponential backoff for 429 responses (up to 3 retries)
- Comprehensive error handling with user-friendly messages
- 20+ Pydantic v2 models for type-safe validation

#### Board Operations
- `list_boards` - List all accessible boards with search
- `get_board` - Get detailed board information
- `get_board_cards` - Get card faces on a board
- `get_leaf_lanes` - Get lanes that can hold cards
- `create_board` - Create new boards
- `get_board_members` - Get assigned members
- Board archive/unarchive support

#### Card Operations
- `list_cards` - List and filter cards
- `get_card` - Get full card details
- `get_card_activity` - View card history
- `create_card` - Create new cards
- `update_card` - Update card fields
- `move_card` - Move cards between lanes
- `delete_card` - Delete cards
- Comment management (get, create, update, delete)
- Attachment management (list, delete)
- User and team assignment to cards

#### Parent-Child Connections
- `get_card_children` - Get child cards with pagination
- `get_card_parents` - Get parent cards with pagination
- `create_connection` - Connect two cards
- `delete_connection` - Remove connections
- `get_connection_statistics` - View connection stats
- `connect_cards_bulk` - Bulk connection creation
- Cross-board connection support

#### Dependencies
- `get_card_dependencies` - List all card dependencies
- `create_dependency` - Create dependencies with multiple types
  - finish-to-start
  - start-to-start
  - finish-to-finish
  - start-to-finish
- `delete_dependency` - Remove dependencies

#### User & Team Queries
- `list_users` - Search and list users
- `get_user` - Get user details
- `get_current_user` - Get authenticated user info
- `list_teams` - Search and list teams
- `get_team` - Get team details

#### Bulk Operations
- `update_cards_bulk` - Update multiple cards at once
- `move_cards_bulk` - Move multiple cards
- `delete_cards_bulk` - Delete multiple cards
- `assign_members_bulk` - Assign users/teams to multiple boards

#### Documentation
- Comprehensive README with examples
- Quick start guide (5-minute setup)
- Implementation summary
- Contributing guidelines
- Claude Desktop configuration example

#### Testing
- pytest configuration with async support
- Test fixtures for common data
- Unit tests for auth and client
- Coverage reporting setup

### Technical Details
- Python 3.10+ support
- Dependencies: FastMCP, httpx, Pydantic v2, python-dotenv
- MIT License
- Full async/await implementation

[0.1.0]: https://github.com/jhigh1594/agileplace-mcp-server/releases/tag/v0.1.0

