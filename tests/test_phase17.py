from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime

from app.models.schemas import Base, SQLAgentState, SQLCapabilityNode, SQLCapabilityGap, SQLPracticeCampaign, SQLSpecialistPromotion, SQLArtifactPortfolio
from app.core.capability_engine import (
    run_gap_discovery,
    generate_learning_campaign,
    evaluate_mastery_promotion,
    run_self_competition,
    update_civilization_scorecard
)

# Setup in-memory SQLite for testing
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_capability_gap_detection(db):
    gaps = run_gap_discovery(db)
    assert len(gaps) > 0
    assert gaps[0].domain in ["Cybersecurity", "Software Engineering"]

def test_learning_campaign_generation(db):
    gaps = run_gap_discovery(db)
    gap_id = gaps[0].id
    
    campaign = generate_learning_campaign(db, gap_id)
    assert campaign.status == "ACTIVE"
    assert "solve_benchmark" in campaign.practice_tasks[0]
    
    # Verify the gap was mitigated
    updated_gap = db.query(SQLCapabilityGap).filter(SQLCapabilityGap.id == gap_id).first()
    assert updated_gap.mitigation_plan_id == campaign.id

def test_specialist_promotion(db):
    agent_id = f"agent_{uuid.uuid4().hex[:8]}"
    agent = SQLAgentState(
        agent_id=agent_id,
        role="Cyber Expert",
        house="CyberHouse",
        status="ACTIVE",
        success_count=10, # Enough for first promotion
        failure_count=0,
        current_level=1
    )
    db.add(agent)
    db.commit()

    promo = evaluate_mastery_promotion(db, agent_id)
    assert promo is not None
    assert promo.previous_rank == "Novice"
    assert promo.new_rank == "Apprentice"
    
    updated_agent = db.query(SQLAgentState).filter(SQLAgentState.agent_id == agent_id).first()
    assert updated_agent.current_level == 2

def test_self_competition_survival(db):
    agent_a_id = f"agent_a_{uuid.uuid4().hex[:8]}"
    agent_b_id = f"agent_b_{uuid.uuid4().hex[:8]}"
    
    agent_a = SQLAgentState(
        agent_id=agent_a_id,
        role="Worker",
        house="LogicHouse",
        success_count=50,
        failure_count=5,
        current_level=3
    )
    agent_b = SQLAgentState(
        agent_id=agent_b_id,
        role="Worker",
        house="LogicHouse",
        success_count=10,
        failure_count=10,
        current_level=3
    )
    db.add(agent_a)
    db.add(agent_b)
    db.commit()

    result = run_self_competition(db, agent_a_id, agent_b_id)
    
    assert result["winner"] == agent_a_id
    assert result["loser"] == agent_b_id
    
    archived_loser = db.query(SQLAgentState).filter(SQLAgentState.agent_id == agent_b_id).first()
    assert archived_loser.status == "ARCHIVED"

def test_artifact_portfolio_production(db):
    # Simulate an artifact being produced at the end of a campaign
    art = SQLArtifactPortfolio(
        id=f"art_{uuid.uuid4().hex[:8]}",
        capability_id="cap_123",
        artifact_type="CODE",
        file_path="/artifacts/cap_123_benchmark.py",
        content_summary="Solved Kubernetes scheduling benchmark."
    )
    db.add(art)
    db.commit()
    
    scorecard = update_civilization_scorecard(db)
    assert scorecard.artifacts_produced >= 1

if __name__ == "__main__":
    db_session = TestingSessionLocal()
    Base.metadata.create_all(bind=engine)
    print("Running test_capability_gap_detection...")
    test_capability_gap_detection(db_session)
    print("Running test_learning_campaign_generation...")
    test_learning_campaign_generation(db_session)
    print("Running test_specialist_promotion...")
    test_specialist_promotion(db_session)
    print("Running test_self_competition_survival...")
    test_self_competition_survival(db_session)
    print("Running test_artifact_portfolio_production...")
    test_artifact_portfolio_production(db_session)
    print("ALL TESTS PASSED!")
