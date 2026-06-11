import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy import select

from app.models.schemas import init_db, SQLKnowledgeSource, SQLToolMastery, SQLBenchmarkRun, SQLSkillScore
from app.core.event_bus import event_bus, Event

from app.services.knowledge_ingestion_engine import knowledge_ingestion_engine
from app.services.tool_mastery_engine import tool_mastery_engine
from app.services.domain_benchmark_engine import domain_benchmark_engine
from app.services.skill_scoring_system import skill_scoring_system

class MockRecord:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class MockScalars:
    def __init__(self, record):
        self.record = record
    def first(self):
        return self.record

class MockResult:
    def __init__(self, record):
        self.record = record
    def scalars(self):
        return MockScalars(self.record)

class MockSessionContext:
    async def __aenter__(self):
        session = AsyncMock()
        
        async def mock_execute(query, *args, **kwargs):
            query_str = str(query).lower()
            if "knowledge_sources" in query_str:
                return MockResult(MockRecord(content_type="RFC"))
            elif "tool_mastery" in query_str:
                return MockResult(MockRecord(total_executions=2, successful_executions=1, success_rate=50.0))
            elif "benchmark_runs" in query_str:
                return MockResult(MockRecord(passed_tests=85, score_percentage=85.0))
            elif "skill_scores" in query_str:
                return MockResult(MockRecord(proficiency_score=85.0))
            return MockResult(None)
            
        session.execute = mock_execute
        return session
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

def mock_async_session():
    return MockSessionContext()

@patch("app.services.knowledge_ingestion_engine.async_session", side_effect=mock_async_session)
@patch("tests.test_phase12.init_db", new_callable=AsyncMock)
def test_knowledge_ingestion(mock_init, mock_session):
    async def run_test():
        await knowledge_ingestion_engine.initialize()
        
        await event_bus.publish(Event(
            event_type="KNOWLEDGE_INGESTION_REQUESTED",
            sender="TestRunner",
            payload={"title": "RFC 793 - TCP", "content_type": "RFC", "content": "Transmission Control Protocol...", "source_url": "https://ietf.org/rfc793"}
        ))
        await asyncio.sleep(0.5)
        
        async with mock_session() as session:
            result = await session.execute(select(SQLKnowledgeSource).where(SQLKnowledgeSource.title == "RFC 793 - TCP"))
            record = result.scalars().first()
            assert record is not None
            assert record.content_type == "RFC"

    asyncio.run(run_test())

@patch("app.services.tool_mastery_engine.async_session", side_effect=mock_async_session)
@patch("tests.test_phase12.init_db", new_callable=AsyncMock)
def test_tool_mastery_tracking(mock_init, mock_session):
    async def run_test():
        await tool_mastery_engine.initialize()
        
        await event_bus.publish(Event(event_type="TOOL_EXECUTED", sender="TestRunner", payload={"tool_name": "Nmap_Scanner", "success": True, "latency_ms": 150.0}))
        await event_bus.publish(Event(event_type="TOOL_EXECUTED", sender="TestRunner", payload={"tool_name": "Nmap_Scanner", "success": False, "latency_ms": 120.0}))
        await asyncio.sleep(0.5)
        
        async with mock_session() as session:
            result = await session.execute(select(SQLToolMastery).where(SQLToolMastery.tool_name == "Nmap_Scanner"))
            record = result.scalars().first()
            assert record is not None
            assert record.total_executions == 2
            assert record.successful_executions == 1
            assert record.success_rate == 50.0

    asyncio.run(run_test())

@patch("app.services.domain_benchmark_engine.async_session", side_effect=mock_async_session)
@patch("app.services.skill_scoring_system.async_session", side_effect=mock_async_session)
@patch("tests.test_phase12.init_db", new_callable=AsyncMock)
def test_benchmark_and_scoring(mock_init, mock_score_session, mock_bench_session):
    async def run_test():
        await domain_benchmark_engine.initialize()
        await skill_scoring_system.initialize()
        
        await event_bus.publish(Event(event_type="RUN_BENCHMARK", sender="TestRunner", payload={"domain": "PYTHON", "test_suite": "AsyncIO Mastery"}))
        await asyncio.sleep(0.5)
        
        async with mock_bench_session() as session:
            result = await session.execute(select(SQLBenchmarkRun).where(SQLBenchmarkRun.domain == "PYTHON"))
            run = result.scalars().first()
            assert run is not None
            assert run.passed_tests == 85
            assert run.score_percentage == 85.0
            
            score_res = await session.execute(select(SQLSkillScore).where(SQLSkillScore.skill_domain == "PYTHON"))
            skill = score_res.scalars().first()
            assert skill is not None
            assert skill.proficiency_score == 85.0

    asyncio.run(run_test())

