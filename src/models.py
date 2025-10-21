"""Pydantic models for AgilePlace API entities."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# User and Team Models
class User(BaseModel):
    """User entity."""

    id: str
    email_address: Optional[str] = Field(None, alias="emailAddress")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    full_name: Optional[str] = Field(None, alias="fullName")
    avatar: Optional[str] = None
    enabled: Optional[bool] = None


class Team(BaseModel):
    """Team entity."""

    id: str
    name: str
    description: Optional[str] = None


# Board Models
class Lane(BaseModel):
    """Board lane entity."""

    id: str
    name: str
    description: Optional[str] = None
    card_status: Optional[str] = Field(None, alias="cardStatus")
    orientation: Optional[str] = None
    lane_type: Optional[str] = Field(None, alias="laneType")
    lane_class_type: Optional[str] = Field(None, alias="laneClassType")
    index: Optional[int] = None
    parent_lane_id: Optional[str] = Field(None, alias="parentLaneId")
    wip_limit: Optional[int] = Field(None, alias="wipLimit")
    card_count: Optional[int] = Field(None, alias="cardCount")
    card_size: Optional[int] = Field(None, alias="cardSize")
    is_collapsed: Optional[bool] = Field(None, alias="isCollapsed")
    is_connection_done_lane: Optional[bool] = Field(None, alias="isConnectionDoneLane")
    is_default_drop_lane: Optional[bool] = Field(None, alias="isDefaultDropLane")


class CardType(BaseModel):
    """Card type entity."""

    id: str
    name: str
    color_hex: Optional[str] = Field(None, alias="colorHex")
    is_card_type: Optional[bool] = Field(None, alias="isCardType")
    is_task_type: Optional[bool] = Field(None, alias="isTaskType")


class CustomIcon(BaseModel):
    """Custom icon (class of service) entity."""

    id: str
    name: str
    icon_path: Optional[str] = Field(None, alias="iconPath")
    icon_color: Optional[str] = Field(None, alias="iconColor")
    card_color: Optional[str] = Field(None, alias="cardColor")
    policy: Optional[str] = None


class CustomField(BaseModel):
    """Custom field definition."""

    id: str
    label: str
    type: str  # text, number, date, dropdown, multi
    index: Optional[int] = None
    help_text: Optional[str] = Field(None, alias="helpText")


class PlanningSeries(BaseModel):
    """Planning series entity."""

    id: str
    label: str


class Board(BaseModel):
    """Board entity."""

    id: str
    title: str
    description: Optional[str] = None
    version: Optional[str] = None
    organization_id: Optional[str] = Field(None, alias="organizationId")
    is_archived: Optional[bool] = Field(None, alias="isArchived")
    is_shared: Optional[bool] = Field(None, alias="isShared")
    shared_board_role: Optional[str] = Field(None, alias="sharedBoardRole")
    board_role: Optional[str] = Field(None, alias="boardRole")
    lanes: Optional[list[Lane]] = None
    card_types: Optional[list[CardType]] = Field(None, alias="cardTypes")
    classes_of_service: Optional[list[CustomIcon]] = Field(None, alias="classesOfService")
    custom_fields: Optional[list[CustomField]] = Field(None, alias="customFields")
    tags: Optional[list[str]] = None
    users: Optional[list[User]] = None
    planning_series: Optional[list[PlanningSeries]] = Field(None, alias="planningSeries")


# Card Models
class BlockedStatus(BaseModel):
    """Card blocked status."""

    is_blocked: bool = Field(alias="isBlocked")
    reason: Optional[str] = None


class CustomHeader(BaseModel):
    """Card custom header."""

    value: Optional[str] = None
    header: Optional[str] = None
    url: Optional[str] = None


class CustomId(BaseModel):
    """Card custom ID."""

    value: Optional[str] = None
    prefix: Optional[str] = None
    url: Optional[str] = None


class ExternalLink(BaseModel):
    """External link on a card."""

    label: str
    url: str


class ConnectedCardStats(BaseModel):
    """Statistics for connected cards."""

    total_count: Optional[int] = Field(None, alias="totalCount")
    total_size: Optional[int] = Field(None, alias="totalSize")
    started_count: Optional[int] = Field(None, alias="startedCount")
    started_size: Optional[int] = Field(None, alias="startedSize")
    not_started_count: Optional[int] = Field(None, alias="notStartedCount")
    not_started_size: Optional[int] = Field(None, alias="notStartedSize")
    completed_count: Optional[int] = Field(None, alias="completedCount")
    completed_size: Optional[int] = Field(None, alias="completedSize")
    blocked_count: Optional[int] = Field(None, alias="blockedCount")
    planned_start: Optional[str] = Field(None, alias="plannedStart")
    planned_finish: Optional[str] = Field(None, alias="plannedFinish")
    actual_start: Optional[str] = Field(None, alias="actualStart")
    actual_finish: Optional[str] = Field(None, alias="actualFinish")
    past_due_count: Optional[int] = Field(None, alias="pastDueCount")
    projected_late_count: Optional[int] = Field(None, alias="projectedLateCount")


class TaskBoardStats(BaseModel):
    """Statistics for task board."""

    total_count: Optional[int] = Field(None, alias="totalCount")
    completed_count: Optional[int] = Field(None, alias="completedCount")
    total_size: Optional[int] = Field(None, alias="totalSize")
    completed_size: Optional[int] = Field(None, alias="completedSize")


class ParentCard(BaseModel):
    """Parent card reference."""

    id: str
    title: str


class Card(BaseModel):
    """Card entity."""

    id: str
    title: str
    description: Optional[str] = None
    lane_id: str = Field(alias="laneId")
    board_id: Optional[str] = Field(None, alias="boardId")
    index: Optional[int] = None
    color: Optional[str] = None
    size: Optional[int] = None
    priority: Optional[str] = None  # low, normal, high, critical
    tags: Optional[list[str]] = None
    planned_start: Optional[str] = Field(None, alias="plannedStart")
    planned_finish: Optional[str] = Field(None, alias="plannedFinish")
    actual_start: Optional[str] = Field(None, alias="actualStart")
    actual_finish: Optional[str] = Field(None, alias="actualFinish")
    is_done: Optional[bool] = Field(None, alias="isDone")
    moved_on: Optional[str] = Field(None, alias="movedOn")
    updated_on: Optional[str] = Field(None, alias="updatedOn")
    created_on: Optional[str] = Field(None, alias="createdOn")
    external_links: Optional[list[ExternalLink]] = Field(None, alias="externalLinks")
    blocked_status: Optional[BlockedStatus] = Field(None, alias="blockedStatus")
    custom_icon: Optional[CustomIcon] = Field(None, alias="customIcon")
    custom_header: Optional[CustomHeader] = Field(None, alias="customHeader")
    custom_id: Optional[CustomId] = Field(None, alias="customId")
    card_type: Optional[CardType] = Field(None, alias="cardType")
    assigned_users: Optional[list[User]] = Field(None, alias="assignedUsers")
    parent_cards: Optional[list[ParentCard]] = Field(None, alias="parentCards")
    connected_card_stats: Optional[ConnectedCardStats] = Field(None, alias="connectedCardStats")
    task_board_stats: Optional[TaskBoardStats] = Field(None, alias="taskBoardStats")
    containing_card_id: Optional[str] = Field(None, alias="containingCardId")
    custom_fields: Optional[dict[str, Any]] = Field(None, alias="customFields")


# Connection Models
class Connection(BaseModel):
    """Card connection (parent/child relationship)."""

    parent_card_id: str = Field(alias="parentCardId")
    child_card_id: str = Field(alias="childCardId")
    created_on: Optional[str] = Field(None, alias="createdOn")


# Dependency Models
class Dependency(BaseModel):
    """Card dependency."""

    id: str
    card_id: str = Field(alias="cardId")
    depends_on_card_id: str = Field(alias="dependsOnCardId")
    dependency_type: Optional[str] = Field(None, alias="dependencyType")
    created_on: Optional[str] = Field(None, alias="createdOn")
    created_by: Optional[User] = Field(None, alias="createdBy")


# Comment Models
class Comment(BaseModel):
    """Card comment."""

    id: str
    text: str
    card_id: Optional[str] = Field(None, alias="cardId")
    created_on: Optional[str] = Field(None, alias="createdOn")
    created_by: Optional[User] = Field(None, alias="createdBy")
    updated_on: Optional[str] = Field(None, alias="updatedOn")
    changed_by: Optional[User] = Field(None, alias="changedBy")


# Attachment Models
class Attachment(BaseModel):
    """Card attachment."""

    id: str
    name: str
    description: Optional[str] = None
    attachment_size: Optional[int] = Field(None, alias="attachmentSize")
    storage_id: Optional[str] = Field(None, alias="storageId")
    created_on: Optional[str] = Field(None, alias="createdOn")
    created_by: Optional[User] = Field(None, alias="createdBy")
    updated_on: Optional[str] = Field(None, alias="updatedOn")
    changed_by: Optional[User] = Field(None, alias="changedBy")


# Activity Models
class ActivityEvent(BaseModel):
    """Board or card activity event."""

    id: str
    type: str
    timestamp: str
    user: Optional[User] = None
    data: Optional[dict[str, Any]] = None


# Pagination Models
class PageMeta(BaseModel):
    """Pagination metadata."""

    total_records: int = Field(alias="totalRecords")
    offset: int
    limit: int
    start_row: int = Field(alias="startRow")
    end_row: int = Field(alias="endRow")


# Response Models
class BoardListResponse(BaseModel):
    """Response for board list."""

    boards: list[Board]
    page_meta: Optional[PageMeta] = Field(None, alias="pageMeta")


class CardListResponse(BaseModel):
    """Response for card list."""

    cards: list[Card]
    page_meta: Optional[PageMeta] = Field(None, alias="pageMeta")


class ConnectionListResponse(BaseModel):
    """Response for connection list."""

    connections: list[Connection]


class UserListResponse(BaseModel):
    """Response for user list."""

    users: list[User]
    page_meta: Optional[PageMeta] = Field(None, alias="pageMeta")


class TeamListResponse(BaseModel):
    """Response for team list."""

    teams: list[Team]


class CommentListResponse(BaseModel):
    """Response for comment list."""

    comments: list[Comment]


class AttachmentListResponse(BaseModel):
    """Response for attachment list."""

    attachments: list[Attachment]

