from typing import List, Dict, Any, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.schemas import get_db_session, SQLExecutiveResponse, ExecutiveResponseSchema

from datetime import datetime

class ExecutiveResponseEngine:
    """
    Synthesizes executive intelligence outputs for the King.
    Replaces raw telemetry dumps with polished, evidence-backed summaries.
    """
    
    @staticmethod
    async def generate_response(
        objective_id: str,
        final_answer: str,
        executive_summary: str,
        supporting_evidence: List[str],
        generated_artifacts: List[str],
        debate_summary: Optional[str] = None,
        confidence_score: float = 1.0,
        primary_specialists: List[str] = None,
        plan: List[str] = None,
        tools_used: List[str] = None,
        benchmark_score: float = 1.0,
        session: AsyncSession = None
    ) -> ExecutiveResponseSchema:
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            resp_id = f"exec_{uuid.uuid4().hex[:12]}"
            response_record = SQLExecutiveResponse(
                id=resp_id,
                objective_id=objective_id,
                final_answer=final_answer,
                executive_summary=executive_summary,
                plan=plan or [],
                supporting_evidence=supporting_evidence,
                generated_artifacts=generated_artifacts,
                tools_used=tools_used or [],
                benchmark_score=benchmark_score,
                debate_summary=debate_summary,
                confidence_score=confidence_score,
                primary_specialists=primary_specialists or [],
                created_at=datetime.utcnow()
            )
            
            db.add(response_record)
            await db.flush()
            if not session:
                await db.commit()
                
            return ExecutiveResponseSchema.model_validate(response_record)
        finally:
            if not session:
                await async_gen.aclose()
                
    @staticmethod
    async def fetch_responses_for_objective(objective_id: str, session: AsyncSession = None) -> List[ExecutiveResponseSchema]:
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            stmt = select(SQLExecutiveResponse).filter_by(objective_id=objective_id).order_by(SQLExecutiveResponse.created_at.desc())
            result = await db.execute(stmt)
            records = result.scalars().all()
            return [ExecutiveResponseSchema.model_validate(r) for r in records]
        finally:
            if not session:
                await async_gen.aclose()

    @staticmethod
    async def get_latest_executive_responses(limit: int = 10, session: AsyncSession = None) -> List[ExecutiveResponseSchema]:
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            stmt = select(SQLExecutiveResponse).order_by(SQLExecutiveResponse.created_at.desc()).limit(limit)
            result = await db.execute(stmt)
            records = result.scalars().all()
            return [ExecutiveResponseSchema.model_validate(r) for r in records]
        finally:
            if not session:
                await async_gen.aclose()
    @staticmethod
    async def seed_initial_state():
        async_gen = get_db_session()
        db = await anext(async_gen)
        try:
            stmt = select(SQLExecutiveResponse).limit(1)
            result = await db.execute(stmt)
            if not result.scalars().first():
                # Seed an initial successful objective run
                resp_id = f"exec_{uuid.uuid4().hex[:12]}"
                response_record = SQLExecutiveResponse(
                    id=resp_id,
                    objective_id="obj_boot_sequence",
                    final_answer="ANTIGRAVITY Backend Civilization successfully initialized. All primary orchestration nodes, sovereign matrices, and reality abstraction engines are online.",
                    executive_summary="Knight-0 successfully executed the multi-stage boot sequence, validating memory consistency, causality trees, and distributed swarm connections.",
                    plan=["1. Verify Relational Memory", "2. Connect Graph Network", "3. Seed Autonomous Agents", "4. Ascend Executive Core"],
                    supporting_evidence=["Memory consistency passed 100%.", "Sovereign matrix loaded 56 active agents.", "Causal inference topology graph built."],
                    generated_artifacts=["civilization_audit_report.md", "boot_sequence.log"],
                    tools_used=["memory_validator", "neo4j_cypher_loader", "ascension_engine"],
                    benchmark_score=0.98,
                    debate_summary="Unanimous consensus by parliament to exit hibernation.",
                    confidence_score=0.99,
                    primary_specialists=["StrategyHouse", "SecurityHouse", "EngineeringHouse"],
                    created_at=datetime.utcnow()
                )
                db.add(response_record)
                await db.commit()
        finally:
            await async_gen.aclose()

executive_response_engine = ExecutiveResponseEngine()
