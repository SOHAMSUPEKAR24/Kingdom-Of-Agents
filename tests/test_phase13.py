import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.models.schemas import Base
from app.services.persistent_agent_registry import registry
from app.services.executive_response_engine import executive_response_engine

# Use an in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_persistent_agent_lifecycle():
    async with TestingSessionLocal() as session:
        # Create an agent
        agent = await registry.create_agent("Knight-V", "HOUSE_OF_COMMAND", "Planning", session)
        assert agent.id.startswith("agent_")
        assert agent.status == "ALIVE"
        
        # Verify it can be retrieved
        fetched = await registry.get_agent(agent.id, session)
        assert fetched.name == "Knight-V"
        
        # Update status
        await registry.update_agent_status(agent.id, "RETIRED", session)
        fetched = await registry.get_agent(agent.id, session)
        assert fetched.status == "RETIRED"

@pytest.mark.asyncio
async def test_executive_response_synthesis():
    async with TestingSessionLocal() as session:
        resp = await executive_response_engine.generate_response(
            objective_id="obj_123",
            final_answer="The system is stable.",
            executive_summary="All diagnostic checks passed.",
            supporting_evidence=["Trace A"],
            generated_artifacts=["report.md"],
            session=session
        )
        assert resp.id.startswith("exec_")
        assert resp.final_answer == "The system is stable."

        latest = await executive_response_engine.get_latest_executive_responses(session=session)
        assert len(latest) == 1
        assert latest[0].objective_id == "obj_123"

@pytest.mark.asyncio
async def test_civilization_reconstruction():
    async with TestingSessionLocal() as session:
        # Create multiple agents
        await registry.create_agent("Agent-A", "HOUSE_OF_COMMAND", "Planning", session)
        await registry.create_agent("Agent-B", "HOUSE_OF_ENGINEERS", "Coding", session)
        
        alive = await registry.get_all_alive_agents(session)
        assert len(alive) == 2
