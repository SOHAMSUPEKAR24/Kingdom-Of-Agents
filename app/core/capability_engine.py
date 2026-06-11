import uuid
import json
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.schemas import (
    SQLCapabilityNode,
    SQLCapabilityGap,
    SQLPracticeCampaign,
    SQLSpecialistPromotion,
    SQLAgentState,
    SQLAgentGenome,
    SQLCivilizationScorecard,
    SQLArtifactPortfolio
)

logger = logging.getLogger(__name__)

def run_gap_discovery(db: Session) -> list[SQLCapabilityGap]:
    """
    Component 2: Capability Gap Discovery Engine
    Knight-0 continuously asks: 'What can I not do?'
    Detects missing tools, benchmark failures, and creates gaps.
    """
    # Identify domains where mastery is very low or non-existent
    # In a full simulation, this would parse recent failed tasks.
    # For now, we mock the detection of a missing capability based on a baseline.
    baseline_skills = [
        {"domain": "Cybersecurity", "sub_domain": "Web Security", "skill": "SQL Injection Analysis"},
        {"domain": "Software Engineering", "sub_domain": "Kubernetes", "skill": "Cluster Operations"}
    ]
    
    new_gaps = []
    for skill_req in baseline_skills:
        existing = db.query(SQLCapabilityNode).filter(
            SQLCapabilityNode.domain == skill_req["domain"],
            SQLCapabilityNode.skill_name == skill_req["skill"]
        ).first()
        
        if not existing or existing.mastery_score < 0.3:
            gap_id = f"gap_{uuid.uuid4().hex[:8]}"
            gap = SQLCapabilityGap(
                id=gap_id,
                domain=skill_req["domain"],
                identified_weakness=f"Lacking proficiency in {skill_req['skill']}",
                severity_score=0.8,
                created_at=datetime.utcnow()
            )
            db.add(gap)
            new_gaps.append(gap)
            
            # Create a placeholder CapabilityNode if it doesn't exist
            if not existing:
                cap = SQLCapabilityNode(
                    id=f"cap_{uuid.uuid4().hex[:8]}",
                    domain=skill_req["domain"],
                    sub_domain=skill_req["sub_domain"],
                    skill_name=skill_req["skill"],
                    dependencies=[],
                    required_tools=["docker", "kubectl"] if "Kubernetes" in skill_req["domain"] else ["nmap"],
                    benchmark_metrics={"target_accuracy": 0.9},
                    mastery_score=0.0
                )
                db.add(cap)

    db.commit()
    logger.info(f"[Capability Engine] Discovered {len(new_gaps)} capability gaps.")
    return new_gaps

def generate_learning_campaign(db: Session, gap_id: str) -> SQLPracticeCampaign:
    """
    Component 3: Autonomous Learning Campaigns
    For a given gap, generate reading plans, experiments, and practice tasks.
    """
    gap = db.query(SQLCapabilityGap).filter(SQLCapabilityGap.id == gap_id).first()
    if not gap:
        raise ValueError(f"Capability gap {gap_id} not found.")

    target_cap = db.query(SQLCapabilityNode).filter(
        SQLCapabilityNode.domain == gap.domain
    ).first()
    
    cap_id = target_cap.id if target_cap else f"cap_{uuid.uuid4().hex[:8]}"

    campaign = SQLPracticeCampaign(
        id=f"camp_{uuid.uuid4().hex[:8]}",
        target_capability_id=cap_id,
        objective=f"Master domain: {gap.domain} to mitigate weakness: {gap.identified_weakness}",
        reading_plans=[{"topic": gap.domain, "source": "official_docs", "status": "PENDING"}],
        experiments=[{"hypothesis": f"Using new tools improves {gap.domain} execution", "status": "PENDING"}],
        practice_tasks=[f"solve_benchmark_{gap.domain.lower().replace(' ', '_')}"],
        status="ACTIVE",
        iterations_completed=0,
        improvement_score=0.0
    )
    
    # Mark gap as mitigated
    gap.mitigation_plan_id = campaign.id
    
    db.add(campaign)
    db.commit()
    logger.info(f"[Capability Engine] Generated learning campaign {campaign.id} for gap {gap_id}.")
    return campaign

def evaluate_mastery_promotion(db: Session, agent_id: str) -> SQLSpecialistPromotion:
    """
    Component 5: Mastery System
    Levels: Novice, Apprentice, Practitioner, Advanced, Expert, Master, Legendary
    Promotes an agent based on benchmark evidence.
    """
    agent = db.query(SQLAgentState).filter(SQLAgentState.agent_id == agent_id).first()
    if not agent:
        raise ValueError(f"Agent {agent_id} not found.")

    levels = ["Novice", "Apprentice", "Practitioner", "Advanced", "Expert", "Master", "Legendary"]
    
    current_idx = min(agent.current_level - 1, len(levels) - 1)
    current_rank = levels[current_idx]
    
    # Calculate evidence (mock logic - in reality, evaluate benchmark scores)
    if agent.success_count >= (current_idx + 1) * 10:
        new_idx = min(current_idx + 1, len(levels) - 1)
        new_rank = levels[new_idx]
        
        promotion = SQLSpecialistPromotion(
            id=f"promo_{uuid.uuid4().hex[:8]}",
            agent_id=agent_id,
            dynasty=agent.house,
            previous_rank=current_rank,
            new_rank=new_rank,
            justification=f"Achieved {agent.success_count} benchmark successes.",
            created_at=datetime.utcnow()
        )
        
        agent.current_level = new_idx + 1
        db.add(promotion)
        db.commit()
        logger.info(f"[Capability Engine] Promoted agent {agent_id} to {new_rank}.")
        return promotion
    
    return None

def run_self_competition(db: Session, competitor_a_id: str, competitor_b_id: str) -> dict:
    """
    Component 6: Self-Competition Engine
    Competitors face off. Winner survives. Loser is archived.
    """
    agent_a = db.query(SQLAgentState).filter(SQLAgentState.agent_id == competitor_a_id).first()
    agent_b = db.query(SQLAgentState).filter(SQLAgentState.agent_id == competitor_b_id).first()
    
    if not agent_a or not agent_b:
        raise ValueError("Competitors not found.")

    # Calculate benchmark metrics to determine winner
    score_a = (agent_a.success_count + 1) / max(1, agent_a.failure_count)
    score_b = (agent_b.success_count + 1) / max(1, agent_b.failure_count)
    
    if score_a >= score_b:
        winner = agent_a
        loser = agent_b
    else:
        winner = agent_b
        loser = agent_a
        
    loser.status = "ARCHIVED" # Archive loser as requested
    
    db.commit()
    logger.info(f"[Capability Engine] Competition concluded. Winner: {winner.agent_id}, Loser archived: {loser.agent_id}")
    
    return {
        "winner": winner.agent_id,
        "loser": loser.agent_id,
        "winner_score": max(score_a, score_b),
        "loser_score": min(score_a, score_b)
    }

def update_civilization_scorecard(db: Session) -> SQLCivilizationScorecard:
    """
    Component 10: Civilization Scorecard
    Aggregates growth across the entire civilization.
    """
    cap_count = db.query(SQLCapabilityNode).count()
    promo_count = db.query(SQLSpecialistPromotion).count()
    artifact_count = db.query(SQLArtifactPortfolio).count()
    
    # Calculate benchmark wins from all successful tasks or agents
    agents = db.query(SQLAgentState).all()
    total_wins = sum([a.success_count for a in agents])
    
    scorecard = db.query(SQLCivilizationScorecard).first()
    if not scorecard:
        scorecard = SQLCivilizationScorecard(id="global_scorecard")
        db.add(scorecard)
        
    scorecard.capabilities_count = cap_count
    scorecard.benchmark_wins = total_wins
    scorecard.promotions_count = promo_count
    scorecard.artifacts_produced = artifact_count
    scorecard.created_at = datetime.utcnow()
    
    db.commit()
    logger.info("[Capability Engine] Updated global civilization scorecard.")
    return scorecard
