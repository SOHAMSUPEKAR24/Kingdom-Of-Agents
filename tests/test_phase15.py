import pytest
import pytest_asyncio
from app.models.schemas import async_session
from app.services.causal_reasoning_engine import causal_reasoning_engine
from app.services.uncertainty_reasoning_engine import uncertainty_reasoning_engine
from app.services.scientific_hypothesis_engine import scientific_hypothesis_engine
from app.services.generalization_engine import generalization_engine
from app.services.strategic_reasoning_engine import strategic_reasoning_engine
from app.services.adversarial_reasoning_engine import adversarial_reasoning_engine
from app.services.long_chain_reasoning_engine import long_chain_reasoning_engine
from app.services.theory_formation_engine import theory_formation_engine
from app.services.reasoning_benchmark_engine import reasoning_benchmark_engine
from app.services.cognitive_depth_engine import cognitive_depth_engine

@pytest_asyncio.fixture
async def db_session():
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_causal_reasoning_chains(db_session):
    graph = await causal_reasoning_engine.construct_causal_graph("Test Graph", {}, db_session)
    assert graph is not None
    assert len(graph.nodes) > 0
    assert len(graph.edges) > 0

@pytest.mark.asyncio
async def test_uncertainty_confidence_scoring():
    evidence = [{"supports_hypothesis": True}, {"supports_hypothesis": False}]
    res = await uncertainty_reasoning_engine.calculate_confidence("Hypothesis A", evidence)
    assert res["confidence"] == 0.5
    assert res["uncertainty"] == 0.5

@pytest.mark.asyncio
async def test_competing_hypotheses_generation(db_session):
    hyp = await scientific_hypothesis_engine.generate_hypothesis("Rate limits spiked", db_session)
    assert hyp is not None
    assert hyp.falsified == False

@pytest.mark.asyncio
async def test_abstraction_extraction(db_session):
    # Mocking experience vectors
    class MockVector:
        id = "VEC-1"
    
    abstraction = await generalization_engine.generalize_experiences([MockVector(), MockVector()], db_session)
    assert abstraction is not None
    assert "API Resiliency" in abstraction.concept_name

@pytest.mark.asyncio
async def test_strategic_simulation_branches(db_session):
    res = await strategic_reasoning_engine.evaluate_strategy_tradeoffs(["Strategy A", "Strategy B"], db_session)
    assert res["best_strategy"] is not None
    assert "simulation_id" in res

@pytest.mark.asyncio
async def test_adversarial_flaw_exposing():
    res = await adversarial_reasoning_engine.expose_flaws("If API works, retry indefinitely.")
    assert len(res["vulnerabilities"]) > 0

@pytest.mark.asyncio
async def test_long_chain_reasoning_continuity():
    chain = await long_chain_reasoning_engine.initialize_chain("Initial premise")
    assert chain["steps_taken"] == 0
    chain = await long_chain_reasoning_engine.advance_chain(chain, "Next deduction")
    assert chain["steps_taken"] == 1

@pytest.mark.asyncio
async def test_theory_formation_persistence():
    res = await theory_formation_engine.form_theory(["Hyp1", "Hyp2"])
    assert res["status"] == "theory_formed"
    assert "confidence" in res

@pytest.mark.asyncio
async def test_reasoning_benchmarks():
    score = await reasoning_benchmark_engine.benchmark_reasoning_quality("trace-1", True)
    assert score["causal_awareness_score"] > 0.8

@pytest.mark.asyncio
async def test_knight_deeper_conceptual_abstractions(db_session):
    depth = await cognitive_depth_engine.evaluate_depth("Knight-0", db_session)
    assert depth is not None
    assert depth.abstraction_depth > 0.5
