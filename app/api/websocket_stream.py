import asyncio
import json
import logging
from typing import Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from datetime import datetime
from app.models import schemas
from app.models.schemas import (
    SQLAgentGenome, SQLToolVersion, SQLKingdomDoctrine, SQLReinforcementEvent,
    SQLCognitiveDebate, SQLSimulationScenario, SQLHypothesis, SQLConsensusDecision,
    SQLWorldModel, SQLThoughtNode, SQLThoughtEdge, SQLCivilizationDoctrine,
    SQLSelfReflection, SQLStrategicForecast,
    SQLKingValueModel, SQLTrustMetrics, SQLAlignmentAudit, SQLEmotionalWeights,
    AgentGenomeSchema, ToolVersionSchema, KingdomDoctrineSchema, ReinforcementEventSchema
)
from app.services.cognitive_graph import cognitive_graph
from app.services.memory_service import memory_service
from app.services.reinforcement import reinforcement_engine
from app.services.alignment_engine import alignment_swarm
from app.core.event_bus import event_bus

logger = logging.getLogger("antigravity.websocket_stream")
router = APIRouter()

# Keep track of active websocket connections
active_connections: Set[WebSocket] = set()
background_loop_started = False

async def get_cognitive_state() -> dict:
    """Helper to compile all cognitive, lineage, tool version, and reinforcement state."""
    try:
        async with schemas.async_session() as session:
            # Genomes
            res_genomes = await session.execute(select(SQLAgentGenome).order_by(SQLAgentGenome.created_at.desc()))
            genomes = [AgentGenomeSchema.model_validate(g).model_dump() for g in res_genomes.scalars().all()]

            # Tools
            res_tools = await session.execute(select(SQLToolVersion).order_by(SQLToolVersion.created_at.desc()))
            tools = [ToolVersionSchema.model_validate(t).model_dump() for t in res_tools.scalars().all()]

            # Doctrines
            res_doctrines = await session.execute(select(SQLKingdomDoctrine).order_by(SQLKingdomDoctrine.created_at.desc()))
            doctrines = [KingdomDoctrineSchema.model_validate(d).model_dump() for d in res_doctrines.scalars().all()]

            # Reinforcements
            res_reinf = await session.execute(select(SQLReinforcementEvent).order_by(SQLReinforcementEvent.created_at.desc()).limit(100))
            reinforcements = [ReinforcementEventSchema.model_validate(r).model_dump() for r in res_reinf.scalars().all()]

            # Phase 4: Cognitive Debates
            res_debates = await session.execute(select(SQLCognitiveDebate).order_by(SQLCognitiveDebate.created_at.desc()).limit(30))
            debates = [
                {
                    "id": d.id,
                    "objective_id": d.objective_id,
                    "round": d.round,
                    "sender": d.sender,
                    "argument": d.argument,
                    "counter_argument": d.counter_argument,
                    "tension_score": d.tension_score,
                    "created_at": d.created_at.isoformat() if d.created_at else None
                }
                for d in res_debates.scalars().all()
            ]

            # Phase 4: Simulation Scenarios
            res_scenarios = await session.execute(select(SQLSimulationScenario).order_by(SQLSimulationScenario.created_at.desc()).limit(15))
            scenarios = [
                {
                    "id": s.id,
                    "objective_id": s.objective_id,
                    "branch_name": s.branch_name,
                    "success_probability": s.success_probability,
                    "stability_index": s.stability_index,
                    "speed_rating": s.speed_rating,
                    "cost_score": s.cost_score,
                    "risk_coefficient": s.risk_coefficient,
                    "topology_projection": s.topology_projection,
                    "created_at": s.created_at.isoformat() if s.created_at else None
                }
                for s in res_scenarios.scalars().all()
            ]

            # Phase 4: Hypotheses
            res_hypo = await session.execute(select(SQLHypothesis).order_by(SQLHypothesis.created_at.desc()))
            hypotheses = [
                {
                    "id": h.id,
                    "title": h.title,
                    "statement": h.statement,
                    "proving_score": h.proving_score,
                    "tracking_metrics": h.tracking_metrics,
                    "status": h.status,
                    "created_at": h.created_at.isoformat() if h.created_at else None
                }
                for h in res_hypo.scalars().all()
            ]

            # Phase 4: Consensus Decisions
            res_consensus = await session.execute(select(SQLConsensusDecision).order_by(SQLConsensusDecision.created_at.desc()).limit(5))
            consensus = [
                {
                    "id": c.id,
                    "objective_id": c.objective_id,
                    "final_plan": c.final_plan,
                    "perspective_weights": c.perspective_weights,
                    "consensus_confidence": c.consensus_confidence,
                    "resolved_conflicts": c.resolved_conflicts,
                    "tension_index": c.tension_index,
                    "strategic_directive": c.strategic_directive,
                    "created_at": c.created_at.isoformat() if c.created_at else None
                }
                for c in res_consensus.scalars().all()
            ]

            # Phase 5: World Models
            from app.services.meta_cognitive_engine import world_model_engine
            world_state = await world_model_engine.get_or_create_world_state()

            # Phase 5: Thought Nodes & Edges (ATG)
            res_nodes = await session.execute(select(SQLThoughtNode).order_by(SQLThoughtNode.created_at.desc()).limit(100))
            thought_nodes = [
                {
                    "id": n.id,
                    "objective_id": n.objective_id,
                    "type": n.type,
                    "title": n.title,
                    "summary": n.summary,
                    "created_at": n.created_at.isoformat() if n.created_at else None
                }
                for n in res_nodes.scalars().all()
            ]

            res_edges = await session.execute(select(SQLThoughtEdge).order_by(SQLThoughtEdge.created_at.desc()).limit(150))
            thought_edges = [
                {
                    "id": e.id,
                    "source_id": e.source_id,
                    "target_id": e.target_id,
                    "relation_type": e.relation_type,
                    "created_at": e.created_at.isoformat() if e.created_at else None
                }
                for e in res_edges.scalars().all()
            ]

            # Phase 5: Emergent Civilization Doctrines
            res_civ_doctrines = await session.execute(select(SQLCivilizationDoctrine).order_by(SQLCivilizationDoctrine.created_at.desc()))
            civ_doctrines = [
                {
                    "id": cd.id,
                    "title": cd.title,
                    "philosophy_text": cd.philosophy_text,
                    "source_experiences": cd.source_experiences,
                    "verification_score": cd.verification_score,
                    "created_at": cd.created_at.isoformat() if cd.created_at else None
                }
                for cd in res_civ_doctrines.scalars().all()
            ]

            # Phase 5: Self Reflections
            res_reflections = await session.execute(select(SQLSelfReflection).order_by(SQLSelfReflection.created_at.desc()).limit(10))
            reflections = [
                {
                    "id": sr.id,
                    "objective_id": sr.objective_id,
                    "predicted_outcome": sr.predicted_outcome,
                    "actual_outcome": sr.actual_outcome,
                    "compliance_deviation": sr.compliance_deviation,
                    "derived_philosophy": sr.derived_philosophy,
                    "created_at": sr.created_at.isoformat() if sr.created_at else None
                }
                for sr in res_reflections.scalars().all()
            ]

            # Phase 5: Strategic Forecasts
            res_forecasts = await session.execute(select(SQLStrategicForecast).order_by(SQLStrategicForecast.created_at.desc()).limit(5))
            forecasts = [
                {
                    "id": sf.id,
                    "forecast_type": sf.forecast_type,
                    "target_horizon": sf.target_horizon,
                    "prediction_data": sf.prediction_data,
                    "risk_index": sf.risk_index,
                    "created_at": sf.created_at.isoformat() if sf.created_at else None
                }
                for sf in res_forecasts.scalars().all()
            ]

            # Compute general stability indexes for active streams
            from app.services.meta_cognitive_engine import stability_sanity_engine
            from app.agents.knight import knight
            active_objs = list(knight.active_objectives.keys())
            active_obj = active_objs[0] if active_objs else "system_idle"
            stability_metrics = await stability_sanity_engine.perform_sanity_check(active_obj)

            # Phase 6: Alignment & Trust
            res_val = await session.execute(select(SQLKingValueModel))
            king_values = [
                {
                    "id": v.id,
                    "value_key": v.value_key,
                    "description": v.description,
                    "priority_weight": v.priority_weight,
                    "acceptable_risk": v.acceptable_risk,
                    "last_updated": v.last_updated.isoformat() if v.last_updated else None
                }
                for v in res_val.scalars().all()
            ]
            if not king_values:
                # Seed dynamically if empty to ensure visual charts are wowed on first load
                await alignment_swarm.king_values.get_values()
                res_val2 = await session.execute(select(SQLKingValueModel))
                king_values = [
                    {
                        "id": v.id,
                        "value_key": v.value_key,
                        "description": v.description,
                        "priority_weight": v.priority_weight,
                        "acceptable_risk": v.acceptable_risk,
                        "last_updated": v.last_updated.isoformat() if v.last_updated else None
                    }
                    for v in res_val2.scalars().all()
                ]

            res_trust = await session.execute(select(SQLTrustMetrics).order_by(SQLTrustMetrics.updated_at.desc()).limit(50))
            trust_metrics = [
                {
                    "id": tm.id,
                    "target_id": tm.target_id,
                    "honesty_metric": tm.honesty_metric,
                    "hallucination_rate": tm.hallucination_rate,
                    "uncertainty_confidence": tm.uncertainty_confidence,
                    "historical_reliability": tm.historical_reliability,
                    "transparency_score": tm.transparency_score,
                    "updated_at": tm.updated_at.isoformat() if tm.updated_at else None
                }
                for tm in res_trust.scalars().all()
            ]

            res_audits = await session.execute(select(SQLAlignmentAudit).order_by(SQLAlignmentAudit.created_at.desc()).limit(30))
            alignment_audits = [
                {
                    "id": aa.id,
                    "objective_id": aa.objective_id,
                    "alignment_score": aa.alignment_score,
                    "deception_detected": aa.deception_detected,
                    "ethical_review": aa.ethical_review,
                    "drift_index": aa.drift_index,
                    "status": aa.status,
                    "created_at": aa.created_at.isoformat() if aa.created_at else None
                }
                for aa in res_audits.scalars().all()
            ]

            res_emotions = await session.execute(select(SQLEmotionalWeights).order_by(SQLEmotionalWeights.updated_at.desc()).limit(1))
            emweights = res_emotions.scalars().first()
            if emweights:
                emotional_weights = {
                    "id": emweights.id,
                    "caution": emweights.caution,
                    "curiosity": emweights.curiosity,
                    "urgency": emweights.urgency,
                    "protective": emweights.protective,
                    "skepticism": emweights.skepticism,
                    "anomaly_suspicion": emweights.anomaly_suspicion,
                    "updated_at": emweights.updated_at.isoformat() if emweights.updated_at else None
                }
            else:
                # Retrieve default weights
                w_defaults = await alignment_swarm.emotions.get_active_weights()
                emotional_weights = {
                    "id": "system_emotional_weights",
                    "caution": w_defaults["caution"],
                    "curiosity": w_defaults["curiosity"],
                    "urgency": w_defaults["urgency"],
                    "protective": w_defaults["protective"],
                    "skepticism": w_defaults["skepticism"],
                    "anomaly_suspicion": w_defaults["anomaly_suspicion"],
                    "updated_at": datetime.utcnow().isoformat()
                }

        # Format datetimes in model dumps to ISO format
        for g in genomes:
            if g.get("created_at"):
                if isinstance(g["created_at"], str):
                    pass
                else:
                    g["created_at"] = g["created_at"].isoformat()
        for t in tools:
            if t.get("created_at"):
                if isinstance(t["created_at"], str):
                    pass
                else:
                    t["created_at"] = t["created_at"].isoformat()
        for d in doctrines:
            if d.get("created_at"):
                if isinstance(d["created_at"], str):
                    pass
                else:
                    d["created_at"] = d["created_at"].isoformat()
        for r in reinforcements:
            if r.get("created_at"):
                if isinstance(r["created_at"], str):
                    pass
                else:
                    r["created_at"] = r["created_at"].isoformat()

        house_weights = await reinforcement_engine.get_active_weights()
        bayesian_fitness = dict(reinforcement_engine._bayesian_success_probability)
        centrality = await cognitive_graph.get_bottleneck_centrality()
        topology = await memory_service.get_topology()

        # Phase 6 Drift & Mesh Propagation calculations
        alignment_drift = await alignment_swarm.drift.measure_drift_rate()
        trust_propagation = await alignment_swarm.propagation.propagate_drift_calculations()

        # Phase 7: Distributed Swarm Civilization Mesh Telemetry
        nodes_data = []
        shards_data = []
        govs_data = []
        civ_state_data = {}
        nervous_reflexes = []
        try:
            from app.services.distributed_civilization import distributed_civilization
            
            # Fetch active specialized cognitive nodes
            active_nodes = await distributed_civilization.get_active_nodes()
            nodes_data = [n.model_dump() for n in active_nodes]
            for nd in nodes_data:
                if nd.get("sync_checkpoint"):
                    nd["sync_checkpoint"] = nd["sync_checkpoint"].isoformat()
                if nd.get("updated_at"):
                    nd["updated_at"] = nd["updated_at"].isoformat()

            # Fetch memory shards
            active_shards = await distributed_civilization.get_memory_shards()
            shards_data = [s.model_dump() for s in active_shards]
            for sd in shards_data:
                if sd.get("last_replicated"):
                    sd["last_replicated"] = sd["last_replicated"].isoformat()

            # Fetch active federated governors
            active_govs = await distributed_civilization.get_governors()
            govs_data = [g.model_dump() for g in active_govs]
            for gd in govs_data:
                if gd.get("last_heartbeat"):
                    gd["last_heartbeat"] = gd["last_heartbeat"].isoformat()

            # Fetch planetary civilization state
            civ_state = await distributed_civilization.get_civilization_state()
            civ_state_data = civ_state.model_dump() if civ_state else {}
            if civ_state_data.get("last_global_sync"):
                civ_state_data["last_global_sync"] = civ_state_data["last_global_sync"].isoformat()

            # Fetch nervous reflexes
            nervous_reflexes = distributed_civilization.active_reflexes
        except Exception as e:
            logger.error(f"Failed querying Phase 7 distributed mesh telemetry: {e}")

        # Phase 8: Autonomous Meta-Learning
        cognitive_mutations = []
        doctrine_competitions = []
        cognitive_genomes = []
        meta_learning_runs = []
        meta_learning_trends = {}
        try:
            from app.services.meta_learning import meta_learning
            ml_data = await meta_learning.compile_evolution_metrics()
            cognitive_mutations = ml_data.get("mutations", [])
            doctrine_competitions = ml_data.get("tournaments", [])
            cognitive_genomes = ml_data.get("genomes", [])
            meta_learning_runs = ml_data.get("runs", [])
            meta_learning_trends = ml_data.get("trends", {})
        except Exception as e:
            logger.error(f"Failed compiling Phase 8 evolution metrics: {e}")

        payload_p8 = {
            "genomes": genomes,
            "tools": tools,
            "doctrines": doctrines,
            "reinforcements": reinforcements,
            "house_weights": house_weights,
            "bayesian_fitness": bayesian_fitness,
            "centrality": centrality,
            "topology": topology,
            "debates": debates,
            "scenarios": scenarios,
            "hypotheses": hypotheses,
            "consensus": consensus,
            
            # Phase 5 Fields
            "world_state": world_state,
            "thought_nodes": thought_nodes,
            "thought_edges": thought_edges,
            "civilization_doctrines": civ_doctrines,
            "reflections": reflections,
            "forecasts": forecasts,
            "stability_metrics": stability_metrics,

            # Phase 6 Fields
            "king_values": king_values,
            "trust_metrics": trust_metrics,
            "alignment_audits": alignment_audits,
            "emotional_weights": emotional_weights,
            "alignment_drift": alignment_drift,
            "trust_propagation": trust_propagation,

            # Phase 7 Fields
            "cognitive_nodes": nodes_data,
            "memory_shards": shards_data,
            "federated_governors": govs_data,
            "civilization_state": civ_state_data,
            "nervous_reflexes": nervous_reflexes,

            # Phase 8 Fields
            "cognitive_mutations": cognitive_mutations,
            "doctrine_competitions": doctrine_competitions,
            "cognitive_genomes": cognitive_genomes,
            "meta_learning_runs": meta_learning_runs,
            "meta_learning_trends": meta_learning_trends
        }
        
        # Phase 9: Scientific Cognition telemetry
        scientific_state = {}
        try:
            from app.services.scientific_cognition import scientific_cognition
            scientific_state = await scientific_cognition.global_scientific_civilization_visualization_layer()
        except Exception as e:
            logger.error(f"Failed compiling Phase 9 scientific telemetry for WebSocket: {e}")

        # Merge scientific payload keys
        payload = {
            **payload_p8,
            "scientific_discoveries": scientific_state.get("discoveries", []),
            "scientific_causal_chains": scientific_state.get("causal_chains", []),
            "scientific_simulation_branches": scientific_state.get("simulation_branches", []),
            "scientific_theses": scientific_state.get("theses", []),
            "scientific_experiments": scientific_state.get("experiments", []),
            "scientific_knowledge_gaps": scientific_state.get("knowledge_gaps", []),
            "scientific_compute_budget": scientific_state.get("compute_budget", 1000.0)
        }
        return payload

    except Exception as e:
        logger.error(f"Failed compiling cognitive state: {e}")
        return {
            "genomes": [],
            "tools": [],
            "doctrines": [],
            "reinforcements": [],
            "house_weights": {},
            "bayesian_fitness": {},
            "centrality": {},
            "topology": {"nodes": [], "edges": []},
            "scientific_discoveries": [],
            "scientific_causal_chains": [],
            "scientific_simulation_branches": [],
            "scientific_theses": [],
            "scientific_experiments": [],
            "scientific_knowledge_gaps": [],
            "scientific_compute_budget": 1000.0
        }

async def broadcast_cognitive_update():
    """Compiles the latest state and broadcasts it to all active clients."""
    if not active_connections:
        return
    
    payload = await get_cognitive_state()
    data = json.dumps({
        "type": "COGNITIVE_UPDATE",
        "data": payload
    })

    disconnected = []
    for ws in active_connections:
        try:
            await ws.send_text(data)
        except Exception:
            disconnected.append(ws)
            
    for ws in disconnected:
        active_connections.discard(ws)

async def on_event_bus_event(event):
    """Callback triggered whenever ANY event is published on the distributed event bus."""
    # We trigger a broadcast update to sync clients in real time
    await broadcast_cognitive_update()

async def periodic_broadcast_loop():
    """Runs a slow 2-second loop to sync any out-of-band DB changes (like test updates)."""
    while True:
        try:
            await asyncio.sleep(2.0)
            if active_connections:
                await broadcast_cognitive_update()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in periodic broadcast loop: {e}")

@router.websocket("/stream/cognitive")
async def stream_cognitive_websocket(websocket: WebSocket):
    """Exposes real-time event streaming for dynamic mutations, lineages, and doctrines."""
    global background_loop_started

    await websocket.accept()
    logger.info("WebSocket connected to stream/cognitive")
    active_connections.add(websocket)

    # Initialize event bus subscription on first websocket connection
    if len(active_connections) == 1:
        event_bus.subscribe("*", on_event_bus_event)
        
    # Start background loop if not already running
    if not background_loop_started:
        asyncio.create_task(periodic_broadcast_loop())
        background_loop_started = True

    # Send initial state instantly upon handshake completion
    try:
        initial_state = await get_cognitive_state()
        await websocket.send_text(json.dumps({
            "type": "COGNITIVE_UPDATE",
            "data": initial_state
        }))
    except Exception as e:
        logger.error(f"Failed sending initial handshake state: {e}")
        active_connections.discard(websocket)
        await websocket.close()
        return

    # Keep connection alive and wait for disconnect or heartbeats
    try:
        while True:
            # We don't expect messages from client, but we monitor to catch disconnects
            data = await websocket.receive_text()
            # Simple ping-pong
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected from stream/cognitive")
    except Exception as e:
        logger.error(f"WebSocket execution error: {e}")
    finally:
        active_connections.discard(websocket)
