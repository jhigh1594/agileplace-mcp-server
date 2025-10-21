"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def mock_board_data():
    """Sample board data for testing."""
    return {
        "id": "123456",
        "title": "Test Board",
        "description": "A test board",
        "version": "1",
        "lanes": [
            {
                "id": "lane1",
                "name": "Backlog",
                "laneType": "backlog",
            },
            {
                "id": "lane2",
                "name": "In Progress",
                "laneType": "inProcess",
            },
        ],
        "cardTypes": [
            {
                "id": "type1",
                "name": "Feature",
                "colorHex": "#FFFFFF",
            }
        ],
        "tags": ["tag1", "tag2"],
    }


@pytest.fixture
def mock_card_data():
    """Sample card data for testing."""
    return {
        "id": "card123",
        "title": "Test Card",
        "description": "Test description",
        "laneId": "lane1",
        "boardId": "123456",
        "priority": "high",
        "size": 5,
        "tags": ["tag1"],
    }


@pytest.fixture
def mock_user_data():
    """Sample user data for testing."""
    return {
        "id": "user123",
        "emailAddress": "test@example.com",
        "firstName": "Test",
        "lastName": "User",
        "fullName": "Test User",
    }


@pytest.fixture
def mock_connection_data():
    """Sample connection data for testing."""
    return {
        "parentCardId": "parent123",
        "childCardId": "child456",
        "createdOn": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_dependency_data():
    """Sample dependency data for testing."""
    return {
        "id": "dep123",
        "cardId": "card456",
        "dependsOnCardId": "card123",
        "dependencyType": "finish_to_start",
    }

