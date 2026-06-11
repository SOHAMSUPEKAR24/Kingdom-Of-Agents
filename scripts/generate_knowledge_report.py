import os
import asyncio
from datetime import datetime
from sqlalchemy import select, func
from app.models.schemas import async_session, SQLScientificDiscovery, SQLGeneratedArtifact, SQLExecutionTrace
from app.services.memory_service import memory_service

async def generate_report():
    print("Gathering civilization metrics...")
    
    async with async_session() as session:
        # 1. Total Discoveries
        res_disc = await session.execute(select(func.count(SQLScientificDiscovery.id)))
        total_discoveries = res_disc.scalar()
        
        # 2. Total Artifacts Generated
        res_art = await session.execute(select(func.count(SQLGeneratedArtifact.id)))
        total_artifacts = res_art.scalar()
        
        # 3. Success Rate
        res_success = await session.execute(select(func.count(SQLExecutionTrace.id)).where(SQLExecutionTrace.status == "PASSED"))
        res_total = await session.execute(select(func.count(SQLExecutionTrace.id)))
        passed = res_success.scalar() or 0
        total = res_total.scalar() or 1
        success_rate = (passed / total) * 100
        
    # Get Qdrant vectors count
    vector_count = 0
    if memory_service.qdrant_client:
        try:
            info = memory_service.qdrant_client.get_collection("kingdom_memories")
            vector_count = info.vectors_count
        except Exception:
            pass

    report = f"""# PHASE 17.9 KNOWLEDGE CIVILIZATION REPORT

## 🧠 Civilization Metrics
- **Total Knowledge Assets (Vectors):** {vector_count}
- **Proven Doctrines Synthesized:** {total_discoveries}
- **Artifacts Generated:** {total_artifacts}
- **Execution Success Rate:** {success_rate:.1f}%

## 🔬 Active Research
The Autonomous Scientific Lab is continuously drawing hypotheses from the World Model and dispatching them to the Execution Engine.
When an Execution Engine completes a task successfully, it permanently distills the facts and doctrines into Qdrant to be reused on the next task, thus compounding knowledge infinitely.
"""
    
    out_path = os.path.join(os.path.abspath('.'), "artifacts", "KNOWLEDGE_CIVILIZATION_REPORT.md")
    with open(out_path, "w") as f:
        f.write(report)
        
    print(f"Report successfully generated at: {out_path}")

if __name__ == "__main__":
    asyncio.run(generate_report())
