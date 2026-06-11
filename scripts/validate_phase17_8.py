import asyncio
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.agents.factory import CodeSoldier
from app.models.schemas import get_db_session, SQLGeneratedArtifact, SQLExecutionTrace, Base, engine
from sqlalchemy import select

from sqlalchemy import create_engine
sync_engine = create_engine("sqlite:///kingdom.db")

# Ensure tables are created
Base.metadata.create_all(bind=sync_engine)

async def run_validation():
    print("--- STARTING PHASE 17.8 REALITY VALIDATION ---")
    
    # 1. Initialize the CodeSoldier
    soldier = CodeSoldier(
        agent_id="knight_test_01",
        role="Software Engineer",
        house="Software Engineering",
        permissions=["EXECUTE", "WRITE"]
    )
    
    task_input = {
        "id": "task_url_shortener_001",
        "objective": "Build a FastAPI URL Shortener Service. It must include main.py, requirements.txt, README.md, and tests/test_main.py that actually run via pytest.",
        "tech_stack": "python"
    }
    
    print(f"Assigning objective: '{task_input['objective']}'")
    
    # 2. Execute the objective (This will invoke the LLM via autonomous_execution_engine)
    try:
        # Provide a fallback if LLM key isn't present
        # In a real environment, this blocks until the LLM returns and tests pass
        result = await soldier.execute(task_input)
        print(f"Task Completed with Status: {result.get('status')}")
        print(f"Generated Files: {result.get('generated_files')}")
        print(f"Trace ID: {result.get('trace_id')}")
        
    except Exception as e:
        print(f"Task FAILED due to Reality Enforcement: {e}")
        sys.exit(1)
        
    # 3. Verify Database Persistence
    print("Verifying artifacts in the database...")
    async for session in get_db_session():
        stmt_arts = select(SQLGeneratedArtifact).where(SQLGeneratedArtifact.task_id == task_input["id"])
        result_arts = await session.execute(stmt_arts)
        artifacts = result_arts.scalars().all()
        
        stmt_trace = select(SQLExecutionTrace).where(SQLExecutionTrace.task_id == task_input["id"])
        result_trace = await session.execute(stmt_trace)
        trace = result_trace.scalars().first()
        
        print(f"Found {len(artifacts)} physical artifacts registered.")
        if len(artifacts) == 0:
            print("ERROR: No artifacts found in database.")
            sys.exit(1)
            
        print(f"Found Trace record: {trace is not None}")
        if trace:
            print(f"Trace Status: {trace.status}, Exit Code: {trace.exit_code}")
            
        break
        
    print("--- REALITY VALIDATION SUCCESSFUL ---")

if __name__ == "__main__":
    asyncio.run(run_validation())
