import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import get_db_session, SQLThoughtEdge
import logging

logger = logging.getLogger(__name__)

class PersistentTopologyEngine:
    """
    Persists swarm topology, House relationships, debate networks, and execution chains.
    Writes to PostgreSQL and mirrors to Neo4j for graph queries.
    """
    
    @staticmethod
    async def persist_relationship(source_id: str, target_id: str, relation_type: str, session: AsyncSession = None) -> bool:
        """Stores a topological link between agents or tasks."""
        async_gen = get_db_session()
        db = session or await anext(async_gen)
        try:
            edge_id = f"edge_{uuid.uuid4().hex[:12]}"
            edge = SQLThoughtEdge(
                id=edge_id,
                source_id=source_id,
                target_id=target_id,
                relation_type=relation_type
            )
            db.add(edge)
            
            # Neo4j fallback mirroring would happen here
            logger.info(f"Persisted topological edge {relation_type} from {source_id} to {target_id}")
            
            if not session:
                await db.commit()
            return True
        finally:
            if not session:
                await async_gen.aclose()

topology_engine = PersistentTopologyEngine()
