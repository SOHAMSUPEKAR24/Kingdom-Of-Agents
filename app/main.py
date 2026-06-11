import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.event_bus import event_bus
from app.services.memory_service import memory_service
from app.services.tool_executor import tool_executor
from app.models.schemas import init_db
from app.agents.knight import knight
from app.agents.houses import initialize_houses
from app.agents.town_hall import town_hall
from app.api.endpoints import router as api_router
from app.api.websocket_stream import router as ws_router
from app.api.capability_endpoints import router as capability_router

# Setup structured logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("antigravity.main")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="The persistent, evolving backend civilization database and agent orchestrator for ANTIGRAVITY.",
    version=settings.VERSION
)

# Configure CORS so the Next.js frontend can connect seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to dashboard address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register endpoints router
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(ws_router, prefix=settings.API_V1_STR)
app.include_router(capability_router, prefix=f"{settings.API_V1_STR}/capabilities", tags=["Capability Acquisition"])

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing ANTIGRAVITY Kingdom Backend Civilizations...")
    
    # 1. Initialize Relational Database Tables
    await init_db()
    
    # 2. Connect the async Redis Event Bus
    await event_bus.connect()
    
    # 3. Connect Multi-Tier Memory Databases (Postgres, Qdrant, Neo4j, Redis)
    await memory_service.connect()
    
    from app.services.infrastructure_guardian import infrastructure_guardian
    await infrastructure_guardian.verify_infrastructure()
    
    # 4. Initialize Governance Validation Audits in Town Hall
    await town_hall.initialize()
    
    # 5. Connect domain-specialized Houses and event subscribers
    await initialize_houses()
    
    # Phase 11: Hook Reality Audit Engine to event bus
    from app.services.reality_audit_engine import reality_audit_engine
    await reality_audit_engine.initialize()
    
    # Phase 16.8: Connect dormant Intelligence Engines
    from app.services.scientific_experiment_sandbox import scientific_experiment_sandbox
    from app.services.causal_reasoning_engine import causal_reasoning_engine
    from app.services.doctrine_automation_engine import doctrine_automation_engine
    await scientific_experiment_sandbox.initialize()
    await causal_reasoning_engine.initialize()
    await doctrine_automation_engine.initialize()
    
    # Phase 11: Recover any active tasks interrupted by a server restart
    from app.services.persistent_memory_engine import persistent_memory_engine
    await persistent_memory_engine.recover_civilization_state()
    
    # Phase 13: Swarm Reboot Recovery System & Continuity Validation
    from app.services.agent_reconstruction_engine import reconstruction_engine
    from app.services.task_recovery_engine import task_recovery_engine
    from app.services.continuity_validator import continuity_validator
    
    continuity_validator.validate_memory_consistency()
    await reconstruction_engine.reconstruct_civilization()
    await task_recovery_engine.recover_unfinished_tasks()
    
    # 6. Initialize Knight-0 Core objective-DAG scheduler
    await knight.initialize()

    # Phase 21: Seed Scientific Throne on boot
    from app.services.scientific_cognition import scientific_cognition
    await scientific_cognition.seed_initial_state()

    # Pre-seed Executive Responses
    from app.services.executive_response_engine import executive_response_engine
    await executive_response_engine.seed_initial_state()

    # Phase 14: Autonomous Ascension Loop (runs in background)
    import asyncio
    from app.services.knight_ascension_engine import knight_ascension_engine
    from app.services.knight_reasoning_ascension_engine import knight_reasoning_ascension_engine
    from app.services.knight_sovereign_ascension_engine import knight_sovereign_ascension_engine
    from app.models.schemas import async_session
    
    # Run once at startup to seed metrics
    try:
        async with async_session() as session:
            await knight_ascension_engine.run_ascension_cycle(session)
            await knight_reasoning_ascension_engine.run_reasoning_ascension_cycle(session)
            await knight_sovereign_ascension_engine.run_sovereign_ascension_cycle(session)
            await session.commit()
    except Exception as e:
        logger.error(f"Failed to run initial Ascension Cycles: {e}")
    
    async def run_ascension_loop():
        while True:
            await asyncio.sleep(3600)  # Run every hour
            try:
                async with async_session() as session:
                    await knight_ascension_engine.run_ascension_cycle(session)
                    await knight_reasoning_ascension_engine.run_reasoning_ascension_cycle(session)
                    await knight_sovereign_ascension_engine.run_sovereign_ascension_cycle(session)
                    await session.commit()
            except Exception as e:
                logger.error(f"Failed to run Knight-0 Ascension Cycle: {e}")
                
    asyncio.create_task(run_ascension_loop())

    # Phase 16.8: Continuous Civilization Intelligence Heartbeat
    from app.services.research_directorate_engine import research_directorate_engine
    from app.services.toolchain_optimization_engine import toolchain_optimization_engine
    from app.services.specialist_promotion_engine import specialist_promotion_engine
    
    async def run_civilization_heartbeat_loop():
        logger.info("💓 [HEARTBEAT] Booting continuous civilization heartbeat...")
        while True:
            await asyncio.sleep(60)  # Run every 1 minute
            try:
                logger.debug("💓 [HEARTBEAT] Initiating continuous intelligence cycle...")
                # Part 1 & 10: Scientific Loop
                await scientific_cognition.autonomous_scientific_reasoning_engine()
                
                # Part 2: Research Directorate Campaigns
                await research_directorate_engine.propose_research_goal("system_efficiency")
                
                # Part 5: Tool Tournaments
                await toolchain_optimization_engine.run_tool_tournament()
                
                # Part 6: Dynasty Evaluation
                await specialist_promotion_engine.run_dynasty_evaluation()
                
                # Part 11: Reality Enforcement
                await reality_audit_engine.audit_system_idleness()
                
            except Exception as e:
                logger.error(f"🚨 [HEARTBEAT] Civilization background loop encountered critical failure: {e}")
                
    asyncio.create_task(run_civilization_heartbeat_loop())

    logger.info("👑 ANTIGRAVITY Backend Civilization fully online and operational! All systems compliant.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.warning("Terminating ANTIGRAVITY services...")
    
    # Clean up client connections gracefully to prevent leakage
    await event_bus.disconnect()
    await memory_service.disconnect()
    await tool_executor.close()
    
    logger.info("Kingdom offline. Persistent memory persisted safely.")

@app.get("/")
async def health_check():
    """Simple API health check endpoint."""
    return {
        "status": "ONLINE",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.KINGDOM_ENVIRONMENT
    }
