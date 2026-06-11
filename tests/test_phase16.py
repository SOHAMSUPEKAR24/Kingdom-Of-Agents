import pytest
import asyncio
from app.services.autonomous_objective_engine import autonomous_objective_engine
from app.services.weakness_discovery_engine import weakness_discovery_engine
from app.services.resource_governor_engine import resource_governor_engine
from app.services.self_optimization_engine import self_optimization_engine
from app.services.autonomous_experimentation_engine import autonomous_experimentation_engine
from app.services.generation_evolution_engine import generation_evolution_engine
from app.services.roadmap_engine import roadmap_engine
from app.services.self_repair_engine import self_repair_engine
from app.services.evolution_priority_engine import evolution_priority_engine
from app.services.knight_sovereign_ascension_engine import knight_sovereign_ascension_engine

# Mock session for async db tests
class MockSession:
    def add(self, obj):
        pass

@pytest.mark.asyncio
async def test_autonomous_objective_generation():
    """1. Verify autonomous objective generation"""
    session = MockSession()
    obj = await autonomous_objective_engine.generate_objective("TEST_SRC", 0.9, session)
    assert obj.id.startswith("AUTO-OBJ")
    assert obj.origin_source == "TEST_SRC"

@pytest.mark.asyncio
async def test_weakness_detection_growth_campaigns():
    """2. Verify weakness detection launches growth campaigns"""
    session = MockSession()
    weaknesses = await weakness_discovery_engine.run_discovery_scan(session)
    assert len(weaknesses) > 0

@pytest.mark.asyncio
async def test_resource_allocation_dynamic():
    """3. Verify resource allocation adapts dynamically"""
    priorities = {"learning": 0.5, "execution": 0.5}
    allocations = await resource_governor_engine.allocate_resources(priorities)
    assert allocations["learning"] == 50
    assert allocations["execution"] == 50

@pytest.mark.asyncio
async def test_self_optimization_benchmark():
    """4. Verify self-optimization improves benchmark metrics"""
    opt = await self_optimization_engine.optimize_workflow({"id": "wf-123"})
    assert opt["status"] == "OPTIMIZED"

@pytest.mark.asyncio
async def test_autonomous_experiments():
    """5. Verify autonomous experiments produce measurable results"""
    exp = await autonomous_experimentation_engine.design_experiment("hypo-1")
    assert exp["status"] == "EXPERIMENT_DESIGNED"
    assert "accuracy" in exp["metrics_tracked"]

@pytest.mark.asyncio
async def test_specialist_dynasties():
    """6. Verify specialist dynasties persist across generations"""
    session = MockSession()
    dynasty = await generation_evolution_engine.evolve_generation("Frontend", session)
    assert dynasty.current_generation == 2
    assert "Frontend" in dynasty.dynasty_name

@pytest.mark.asyncio
async def test_roadmap_planning():
    """7. Verify roadmap planning survives reboot"""
    session = MockSession()
    roadmap = await roadmap_engine.generate_roadmap("Phase X", session)
    assert roadmap.phase_name == "Phase X"
    assert roadmap.status == "PLANNING"

@pytest.mark.asyncio
async def test_self_repair():
    """8. Verify self-repair restores damaged workflows"""
    repair = await self_repair_engine.restore_damaged_workflow("wf-crash")
    assert repair["status"] == "REPAIRED"
    assert repair["target"] == "wf-crash"

@pytest.mark.asyncio
async def test_evolution_prioritization():
    """9. Verify evolution prioritization suppresses low-value growth"""
    mutations = ["High Value Mutation", "Low Value Mutation"]
    result = await evolution_priority_engine.prioritize_mutations(mutations)
    assert len(result["approved"]) == 1
    assert result["suppressed_count"] == 1

@pytest.mark.asyncio
async def test_knight_ascension_civilization_metrics():
    """10. Verify Knight-0 autonomously improves civilization metrics over time"""
    session = MockSession()
    ascension = await knight_sovereign_ascension_engine.run_sovereign_ascension_cycle(session)
    assert ascension["status"] == "ASCENDED"
    assert ascension["cycle_complete"] is True
