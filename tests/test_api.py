"""Integration tests for content and credentials API endpoints."""

from __future__ import annotations

from uuid import uuid4

from httpx import AsyncClient

# ---------------------------------------------------------------------------
# Content endpoints
# ---------------------------------------------------------------------------


async def test_content_sync_returns_items(client: AsyncClient) -> None:
    """Sync with a past timestamp should return the seeded content item."""
    response = await client.get("/api/v1/content/sync?since=2020-01-01T00:00:00")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "count" in data
    assert data["count"] == len(data["items"])
    assert data["count"] >= 1


async def test_content_sync_future_since_returns_empty(client: AsyncClient) -> None:
    """Sync with a future timestamp should return an empty item list."""
    response = await client.get("/api/v1/content/sync?since=2099-01-01T00:00:00")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["items"] == []


async def test_content_sync_missing_since_returns_422(client: AsyncClient) -> None:
    """Omitting the required `since` param should yield a validation error."""
    response = await client.get("/api/v1/content/sync")
    assert response.status_code == 422


async def test_create_content(client: AsyncClient) -> None:
    """POST /content should create and return a new content item."""
    payload = {
        "title": "Test Lesson Video",
        "content_type": "video",
        "asset_url": "https://cdn.example.com/test.mp4",
    }
    response = await client.post("/api/v1/content", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Lesson Video"
    assert data["content_type"] == "video"
    assert "id" in data


async def test_get_content_found(client: AsyncClient) -> None:
    """GET /content/{id} should return the item after it is created."""
    payload = {
        "title": "Fetchable Content",
        "content_type": "document",
        "asset_url": "https://cdn.example.com/doc.pdf",
    }
    create_resp = await client.post("/api/v1/content", json=payload)
    assert create_resp.status_code == 201
    content_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/content/{content_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == content_id
    assert data["title"] == "Fetchable Content"


async def test_get_content_not_found(client: AsyncClient) -> None:
    """GET /content/{unknown-id} should return 404."""
    response = await client.get(f"/api/v1/content/{uuid4()}")
    assert response.status_code == 404


async def test_list_lessons(client: AsyncClient) -> None:
    """GET /lessons should return a non-empty list."""
    response = await client.get("/api/v1/lessons")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "title" in data[0]


# ---------------------------------------------------------------------------
# Credentials endpoints
# ---------------------------------------------------------------------------

_VALID_WALLET = "0x" + "a" * 40


async def test_issue_credential(client: AsyncClient) -> None:
    """POST /credentials/issue should create a PENDING credential."""
    payload = {
        "learner_id": str(uuid4()),
        "learner_wallet_address": _VALID_WALLET,
        "credential_type": "course_completion",
        "course_id": str(uuid4()),
    }
    response = await client.post("/api/v1/credentials/issue", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "pending"
    assert "credential_id" in data
    assert "tx_hash" in data


async def test_verify_credential(client: AsyncClient) -> None:
    """GET /credentials/{id}/verify should return the stored credential."""
    payload = {
        "learner_id": str(uuid4()),
        "learner_wallet_address": _VALID_WALLET,
        "credential_type": "skill_badge",
        "course_id": str(uuid4()),
    }
    create_resp = await client.post("/api/v1/credentials/issue", json=payload)
    assert create_resp.status_code == 202
    cred_id = create_resp.json()["credential_id"]

    response = await client.get(f"/api/v1/credentials/{cred_id}/verify")
    assert response.status_code == 200
    data = response.json()
    assert data["credential_id"] == cred_id
    assert data["on_chain_verified"] is True


async def test_verify_credential_not_found(client: AsyncClient) -> None:
    """GET /credentials/{unknown-id}/verify should return 404."""
    response = await client.get(f"/api/v1/credentials/{uuid4()}/verify")
    assert response.status_code == 404


async def test_issue_credential_invalid_wallet(client: AsyncClient) -> None:
    """POST /credentials/issue with a bad wallet address should return 422."""
    payload = {
        "learner_id": str(uuid4()),
        "learner_wallet_address": "not-a-valid-address",
        "credential_type": "course_completion",
        "course_id": str(uuid4()),
    }
    response = await client.post("/api/v1/credentials/issue", json=payload)
    assert response.status_code == 422
