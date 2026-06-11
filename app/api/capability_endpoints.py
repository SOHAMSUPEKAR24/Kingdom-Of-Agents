from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.api.deps import get_db
from app.core.capability_engine import (
    run_gap_discovery,
    generate_learning_campaign,
    evaluate_mastery_promotion,
    run_self_competition,
    update_civilization_scorecard
)
from app.models.schemas import (
    CapabilityNodeSchema,
    CapabilityGapSchema,
    PracticeCampaignSchema,
    CivilizationScorecardSchema,
    SQLCapabilityNode,
    SQLCapabilityGap,
    SQLCivilizationScorecard
)

router = APIRouter()

@router.post("/gaps/discover", response_model=List[CapabilityGapSchema])
def trigger_gap_discovery(db: Session = Depends(get_db)):
    """Triggers the Knight-0 Discovery Engine to find capability gaps."""
    gaps = run_gap_discovery(db)
    return gaps

@router.get("/gaps", response_model=List[CapabilityGapSchema])
def get_capability_gaps(db: Session = Depends(get_db)):
    """Retrieve all active capability gaps."""
    gaps = db.query(SQLCapabilityGap).all()
    return gaps

@router.get("/graph", response_model=List[CapabilityNodeSchema])
def get_capability_graph(db: Session = Depends(get_db)):
    """Retrieve the entire Capability Graph (Component 1)."""
    nodes = db.query(SQLCapabilityNode).all()
    return nodes

@router.post("/campaigns/generate/{gap_id}", response_model=PracticeCampaignSchema)
def generate_campaign(gap_id: str, db: Session = Depends(get_db)):
    """Generates an Autonomous Learning Campaign for a specific gap."""
    try:
        campaign = generate_learning_campaign(db, gap_id)
        return campaign
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/competition/run")
def trigger_self_competition(competitor_a_id: str, competitor_b_id: str, db: Session = Depends(get_db)):
    """Component 6: Runs a self-competition benchmark and archives the loser."""
    try:
        result = run_self_competition(db, competitor_a_id, competitor_b_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/scorecard/update", response_model=CivilizationScorecardSchema)
def update_scorecard(db: Session = Depends(get_db)):
    """Updates and returns the global Civilization Scorecard."""
    scorecard = update_civilization_scorecard(db)
    return scorecard

@router.get("/scorecard", response_model=CivilizationScorecardSchema)
def get_scorecard(db: Session = Depends(get_db)):
    """Retrieve the current Civilization Scorecard."""
    scorecard = db.query(SQLCivilizationScorecard).first()
    if not scorecard:
        scorecard = update_civilization_scorecard(db)
    return scorecard
