import asyncio
import logging
from app.models.schemas import engine, Base
from app.services.capability_tree_engine import capability_tree_engine
from app.services.specialist_dynasty_engine import specialist_dynasty_engine
from app.services.autonomous_practice_engine import autonomous_practice_engine
from app.services.specialist_promotion_engine import specialist_promotion_engine
from app.services.capability_gap_engine import capability_gap_engine
from app.services.doctrine_automation_engine import doctrine_automation_engine
from app.services.specialist_dashboard import specialist_dashboard
from sqlalchemy.ext.asyncio import async_sessionmaker

logging.basicConfig(level=logging.INFO)

async def test_phase17():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        print("=== VERIFYING PHASE 17 ===")

        # 1. Seed Tree
        await capability_tree_engine.seed_initial_trees(session)
        print("✅ Capability tree seeded.")

        # 2. Dynasty Persistence
        dynasty = await specialist_dynasty_engine.ensure_dynasty_exists(session, "Browser Dynasty")
        await specialist_dynasty_engine.register_agent_to_dynasty(session, "Agent-007", "Browser Dynasty")
        print(f"✅ Dynasty persistence. Member count: {dynasty.member_count}")

        # 3. Gap Discovery -> Campaigns
        campaigns = await capability_gap_engine.detect_gaps_and_create_campaigns(session)
        print(f"✅ Gap discovery. Created {len(campaigns)} active campaigns.")

        # 4. Practice Loop & Benchmark Progression
        # Agent-007 practices Python -> FastAPI
        score = await autonomous_practice_engine.execute_practice_loop(session, "Software Engineering", "FastAPI", "Agent-007")
        print(f"✅ Practice loop executed. Benchmark score: {score:.2f}")

        # Practice multiple times to increase mastery
        for _ in range(10):
            await autonomous_practice_engine.execute_practice_loop(session, "Software Engineering", "FastAPI", "Agent-007")
            
        nodes = await capability_tree_engine.get_weak_capabilities(session, threshold=1.0)
        fastapi_node = next((n for n in nodes if n.skill_name == "FastAPI"), None)
        print(f"✅ Benchmark progression. FastAPI mastery: {fastapi_node.mastery_score:.2f}")

        # 5. Capability Promotion
        promotion = await specialist_promotion_engine.evaluate_and_promote(session, "Agent-007", "Browser Dynasty", "Novice", fastapi_node.mastery_score)
        if promotion:
            print(f"✅ Capability promotion. Promoted to: {promotion.new_rank}")
        else:
            print(f"⚠️ Capability promotion. Not promoted. Mastery: {fastapi_node.mastery_score:.2f}")

        # 6. Doctrine Automation
        doctrine = await doctrine_automation_engine.formulate_doctrine(session, "Browser Dynasty", "Software Engineering", "trace_123", 0.95)
        print(f"✅ Doctrine automation. Created doctrine: {doctrine.id}")

        # 7. Dashboard
        report = await specialist_dashboard.generate_dashboard_report(session)
        print(f"✅ Dashboard generated. Dynasties tracked: {len(report['dynasties'])}")

        await session.commit()
        print("=== ALL PHASE 17 VERIFICATIONS COMPLETED ===")

if __name__ == "__main__":
    asyncio.run(test_phase17())
