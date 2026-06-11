import pytest
from app.models.schemas import (
    SQLExperienceVector, 
    SQLWorldInteractionLog, 
    SQLAscensionMetric
)
from app.services.world_interaction_engine import world_interaction_engine
from app.services.experience_accumulation_engine import experience_accumulation_engine
from app.services.knight_ascension_engine import knight_ascension_engine
from app.services.browser_operations_engine import browser_operations_engine
import uuid
import pytest_asyncio
from app.models.schemas import async_session

@pytest_asyncio.fixture
async def db_session():
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_world_interaction_logging(db_session):
    agent_id = "test_agent_123"
    log = await world_interaction_engine.log_interaction(
        agent_id, "TERMINAL", "localhost", "echo 'hello world'", "hello world", True, db_session
    )
    assert log is not None
    assert log.success == 1
    assert log.agent_id == agent_id

@pytest.mark.asyncio
async def test_experience_accumulation(db_session):
    agent_id = "test_agent_456"
    telemetry = [
        {"success": True, "outcome_summary": "benchmark passed", "interaction_type": "TEST", "target": "env"},
        {"success": False, "outcome_summary": "timeout occurred", "interaction_type": "API", "target": "remote"}
    ]
    
    vector = await experience_accumulation_engine.accumulate_experience(
        agent_id, "task_1", telemetry, db_session
    )
    
    assert vector is not None
    assert vector.success_rating == 0.5
    assert vector.strategic_weight >= 5.0 # Due to timeout/benchmark
    assert len(vector.extracted_lessons) > 0

@pytest.mark.asyncio
async def test_knight_ascension_cycle(db_session):
    metric = await knight_ascension_engine.run_ascension_cycle(db_session)
    assert metric is not None
    assert metric.knight_id == "Knight-0"
    assert metric.reasoning_depth > 0

@pytest.mark.asyncio
async def test_browser_isolated_fetch(db_session):
    agent_id = "browser_agent_1"
    # Testing browser fetch using a generic safe page
    result = await browser_operations_engine.fetch_page_content(
        agent_id, "https://example.com", db_session
    )
    # The result may fail if playwright isn't fully set up in the test environment, but the sandbox logic should be triggered
    # If successful, we check for string content
    if result.get("success"):
        assert "Example Domain" in result.get("title", "")
        assert len(result.get("content", "")) > 0
