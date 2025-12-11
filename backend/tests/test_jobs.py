"""
职位相关单元测试
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_jobs_list(client: AsyncClient):
    """测试获取职位列表"""
    response = await client.get("/api/v1/jobs?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data


@pytest.mark.asyncio
async def test_get_jobs_with_keyword(client: AsyncClient):
    """测试关键词搜索"""
    response = await client.get("/api/v1/jobs?keyword=开发&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_get_jobs_with_location(client: AsyncClient):
    """测试地点过滤"""
    response = await client.get("/api/v1/jobs?location=北京&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_get_job_detail(client: AsyncClient):
    """测试获取职位详情"""
    # 先获取职位列表，取第一个职位ID
    list_response = await client.get("/api/v1/jobs?page=1&page_size=1")
    if list_response.status_code == 200:
        data = list_response.json()
        if data.get("items") and len(data["items"]) > 0:
            job_id = data["items"][0]["id"]
            response = await client.get(f"/api/v1/jobs/{job_id}")
            assert response.status_code == 200
            assert "id" in response.json()


@pytest.mark.asyncio
async def test_get_job_not_found(client: AsyncClient):
    """测试获取不存在的职位"""
    response = await client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

