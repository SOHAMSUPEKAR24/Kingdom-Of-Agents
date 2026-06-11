import logging
import uuid
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy import select

from app.core.event_bus import event_bus, Event
from app.models.schemas import async_session, SQLKnowledgeSource
from app.services.memory_service import memory_service
from app.services.cognitive_graph import cognitive_graph

logger = logging.getLogger("antigravity.knowledge_ingestion")

class KnowledgeIngestionEngine:
    def __init__(self):
        self.total_sources_ingested = 0

    async def initialize(self):
        event_bus.subscribe("KNOWLEDGE_INGESTION_REQUESTED", self.handle_ingestion_request)
        logger.info("📚 [KNOWLEDGE INGESTION ENGINE] Online. Ready to ingest real-world evidence.")

    async def handle_ingestion_request(self, event: Event):
        payload = event.payload
        title = payload.get("title", "Unknown Source")
        content_type = payload.get("content_type", "DOC")
        source_url = payload.get("source_url")
        content = payload.get("content", "")
        author = payload.get("author", "Unknown")

        if not content:
            logger.warning(f"⚠️ [KNOWLEDGE INGESTION] Discarding ingestion request for '{title}' due to empty content.")
            return

        source_id = str(uuid.uuid4())
        checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()

        # Check for duplicates
        async with async_session() as session:
            res = await session.execute(select(SQLKnowledgeSource).where(SQLKnowledgeSource.checksum == checksum))
            if res.scalars().first():
                logger.info(f"⏭️ [KNOWLEDGE INGESTION] Source '{title}' already ingested. Skipping.")
                return

        # Simple semantic chunking for now
        chunks = self._chunk_content(content)
        
        # Ingest to Qdrant/Neo4j
        for i, chunk in enumerate(chunks):
            chunk_id = f"{source_id}_chunk_{i}"
            # Store in Vector DB (simulated via memory_service interface)
            await memory_service.store_memory(
                memory_id=chunk_id,
                title=f"{title} [Part {i+1}]",
                raw_content=chunk,
                memory_type="KNOWLEDGE_SOURCE"
            )
            # Store lineage in Graph DB
            await cognitive_graph.store_node(
                node_id=chunk_id,
                node_type="KNOWLEDGE_CHUNK",
                attributes={"source_id": source_id, "index": i}
            )

        # Store Source Metadata in Postgres
        async with async_session() as session:
            source_record = SQLKnowledgeSource(
                id=source_id,
                title=title,
                content_type=content_type,
                source_url=source_url,
                checksum=checksum,
                author=author,
                chunk_count=len(chunks),
                ingested_at=datetime.utcnow()
            )
            session.add(source_record)
            await session.commit()

        self.total_sources_ingested += 1
        logger.info(f"✅ [KNOWLEDGE INGESTION] Successfully ingested '{title}' into {len(chunks)} chunks.")

        # Notify knowledge governor
        await event_bus.publish(Event(
            event_type="KNOWLEDGE_INGESTED",
            sender="KnowledgeIngestionEngine",
            payload={"source_id": source_id, "title": title}
        ))

    def _chunk_content(self, content: str, chunk_size: int = 1000) -> List[str]:
        # Simple character-based chunking
        return [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

knowledge_ingestion_engine = KnowledgeIngestionEngine()
