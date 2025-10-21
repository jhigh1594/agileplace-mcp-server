"""Dependency management tools for AgilePlace MCP Server."""

from typing import Optional

from ..client import AgilePlaceClient


async def get_card_dependencies(client: AgilePlaceClient, card_id: str) -> list[dict]:
    """
    Get all dependencies for a card.

    Returns both dependencies where this card depends on others,
    and dependencies where other cards depend on this card.

    Args:
        client: AgilePlace API client
        card_id: ID of the card

    Returns:
        List of dependency objects

    Example:
        dependencies = await get_card_dependencies(client, "123456")
        for dep in dependencies:
            print(f"Card {dep['cardId']} depends on {dep['dependsOnCardId']}")
    """
    response = await client.get(f"/card/{card_id}/dependencies")
    return response.get("dependencies", [])


async def create_dependency(
    client: AgilePlaceClient,
    card_id: str,
    depends_on_card_id: str,
    dependency_type: str = "finish_to_start",
) -> dict:
    """
    Create a dependency between two cards.

    Args:
        client: AgilePlace API client
        card_id: ID of the dependent card (the card that depends on another)
        depends_on_card_id: ID of the card that is depended upon
        dependency_type: Type of dependency (default: 'finish_to_start')
            - 'finish_to_start': Predecessor must finish before successor can start
            - 'start_to_start': Predecessor must start before successor can start
            - 'finish_to_finish': Predecessor must finish before successor can finish
            - 'start_to_finish': Predecessor must start before successor can finish

    Returns:
        Created dependency object

    Example:
        # Card 456 depends on card 123 finishing
        dependency = await create_dependency(
            client,
            card_id="456",
            depends_on_card_id="123",
            dependency_type="finish_to_start"
        )
    """
    payload = {
        "cardId": card_id,
        "dependsOnCardId": depends_on_card_id,
        "dependencyType": dependency_type,
    }
    response = await client.post("/card/dependency", json=payload)
    return response


async def update_dependency(
    client: AgilePlaceClient,
    dependency_id: str,
    dependency_type: Optional[str] = None,
) -> dict:
    """
    Update an existing dependency.

    Args:
        client: AgilePlace API client
        dependency_id: ID of the dependency to update
        dependency_type: New dependency type (optional)
            - 'finish_to_start'
            - 'start_to_start'
            - 'finish_to_finish'
            - 'start_to_finish'

    Returns:
        Updated dependency object

    Example:
        dependency = await update_dependency(
            client,
            "dep123",
            dependency_type="start_to_start"
        )
    """
    payload = {}
    if dependency_type:
        payload["dependencyType"] = dependency_type

    response = await client.patch(f"/card/dependency/{dependency_id}", json=payload)
    return response


async def delete_dependency(client: AgilePlaceClient, dependency_id: str) -> None:
    """
    Delete a dependency.

    Args:
        client: AgilePlace API client
        dependency_id: ID of the dependency to delete

    Example:
        await delete_dependency(client, "dep123")
    """
    await client.delete(f"/card/dependency/{dependency_id}")

