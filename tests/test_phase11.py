import pytest
import asyncio
from app.services.memory_service import memory_service
from app.services.infrastructure_guardian import infrastructure_guardian
from app.services.system_health_verifier import system_health_verifier
from app.services.cognitive_scheduler import cognitive_scheduler
from app.services.reality_audit_engine import reality_audit_engine
from app.services.execution_reality_engine import execution_reality_engine
from app.services.persistent_memory_engine import persistent_memory_engine

@pytest.mark.asyncio
async def test_infrastructure_is_real():
    """Phase 11: Mocks are banned. Infrastructure must be real."""
    
    # 1. Memory service should not have a mock dict or sqlite path
    assert getattr(memory_service, '_mock_graph_db', None) is None, "Mock NetworkX graph should be deleted"
    assert getattr(memory_service, '_mock_vector_db', None) is None, "Mock vector DB should be deleted"
    
    # 2. Guardian must identify postgres connection status
    report = await infrastructure_guardian.get_health_report()
    assert report["postgres"] in ["HEALTHY", "OFFLINE"], "Guardian must return real connection state"
    
@pytest.mark.asyncio
async def test_system_health_aggregation():
    """Phase 11: System health verifier must aggregate all infrastructure state"""
    health = await system_health_verifier.generate_full_report()
    assert "version" in health
    assert "uptime_seconds" in health
    assert "civilization_status" in health
    assert "infrastructure" in health
    assert "postgres" in health["infrastructure"]
    assert "redis" in health["infrastructure"]

@pytest.mark.asyncio
async def test_cognitive_scheduler_loop():
    """Phase 11: Background loops must be scheduled securely."""
    iterations = 0
    
    async def dummy_worker():
        nonlocal iterations
        iterations += 1
        
    task = cognitive_scheduler.schedule_background_loop(
        "Test Loop",
        dummy_worker,
        0.1
    )
    
    await asyncio.sleep(0.3)
    await cognitive_scheduler.shutdown_all()
    
    assert iterations >= 2, "Scheduler failed to run background loop continuously"

@pytest.mark.asyncio
async def test_reality_audit_engine(monkeypatch):
    """Phase 11: Reality audit engine must detect fake executions"""
    from app.core.event_bus import Event
    
    # Mock punish_sender so we don't try to query DB to store log
    async def mock_punish_sender(*args, **kwargs):
        pass
    monkeypatch.setattr(reality_audit_engine, "punish_sender", mock_punish_sender)
    
    initial_count = reality_audit_engine.hallucinations_detected
    
    event = Event(
        event_type="TASK_COMPLETED",
        sender="TestAgent",
        payload={
            "task": {"id": "fake_task_id"},
            "output_data": {"status": "SUCCESS"} # Missing trace_id
        }
    )
    await reality_audit_engine.audit_event(event)
    
    # Count should increment because there's no trace_id
    assert reality_audit_engine.hallucinations_detected == initial_count + 1

@pytest.mark.asyncio
async def test_persistent_memory_recovery(monkeypatch):
    """Phase 11: System should attempt to recover interrupted tasks"""
    # Mock DB query to prevent cross-loop issues
    class MockSession:
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc_val, exc_tb): pass
        async def execute(self, *args, **kwargs):
            class MockResult:
                def scalars(self):
                    class MockScalars:
                        def all(self): return []
                    return MockScalars()
            return MockResult()

    monkeypatch.setattr("app.services.persistent_memory_engine.async_session", MockSession)
    await persistent_memory_engine.recover_civilization_state()
