from typing import List, Optional
import uuid
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import SQLPersistentAgent, PersistentAgentSchema, get_db_session

class PersistentAgentRegistry:
    """
    Manages the lifecycle, persistence, and state of agents across the civilization.
    Agents survive reboots by being written directly to PostgreSQL.
    """
    
    @staticmethod
    async def create_agent(name: str, house: str, specialization: str = None, session: AsyncSession = None) -> PersistentAgentSchema:
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            new_id = f"agent_{uuid.uuid4().hex[:12]}"
            agent = SQLPersistentAgent(
                id=new_id,
                name=name,
                house=house,
                specialization=specialization,
                status="ALIVE",
                current_level=1,
                experience_points=0.0,
                reliability_score=1.0,
                hallucination_rate=0.0,
                last_active=datetime.utcnow(),
                created_at=datetime.utcnow()
            )
            db.add(agent)
            await db.flush()
            if not session:
                await db.commit()
            return PersistentAgentSchema.model_validate(agent)
        finally:
            if not session:
                await async_gen.aclose()

    @staticmethod
    async def get_agent(agent_id: str, session: AsyncSession = None) -> Optional[PersistentAgentSchema]:
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            result = await db.execute(select(SQLPersistentAgent).filter_by(id=agent_id))
            agent = result.scalar_one_or_none()
            if agent:
                return PersistentAgentSchema.model_validate(agent)
            return None
        finally:
            if not session:
                await async_gen.aclose()

    @staticmethod
    async def update_agent_status(agent_id: str, status: str, session: AsyncSession = None) -> bool:
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            stmt = update(SQLPersistentAgent).where(SQLPersistentAgent.id == agent_id).values(
                status=status,
                last_active=datetime.utcnow()
            )
            result = await db.execute(stmt)
            if not session:
                await db.commit()
            return result.rowcount > 0
        finally:
            if not session:
                await async_gen.aclose()

    @staticmethod
    async def get_all_alive_agents(session: AsyncSession = None) -> List[PersistentAgentSchema]:
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            result = await db.execute(select(SQLPersistentAgent).filter_by(status="ALIVE"))
            agents = result.scalars().all()
            return [PersistentAgentSchema.model_validate(a) for a in agents]
        finally:
            if not session:
                await async_gen.aclose()

registry = PersistentAgentRegistry()
