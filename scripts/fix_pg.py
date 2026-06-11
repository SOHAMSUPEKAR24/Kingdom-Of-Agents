import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def fix_db():
    print("Fixing PostgreSQL DB schema...")
    engine = create_async_engine("postgresql+asyncpg://king:kingdom_auth_key@localhost:5432/antigravity_db", echo=True)
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE generated_artifacts ADD COLUMN task_id VARCHAR(100);"))
        except Exception as e:
            print(f"Failed to add task_id: {e}")
            
        try:
            await conn.execute(text("ALTER TABLE generated_artifacts ADD COLUMN trace_id VARCHAR(100);"))
        except Exception:
            pass
            
        try:
            await conn.execute(text("ALTER TABLE generated_artifacts ADD COLUMN creator_agent VARCHAR(100);"))
        except Exception:
            pass
            
        try:
            await conn.execute(text("ALTER TABLE generated_artifacts ADD COLUMN benchmark_result FLOAT;"))
        except Exception:
            pass
            
        try:
            await conn.execute(text("ALTER TABLE generated_artifacts ADD COLUMN validation_status VARCHAR(50) DEFAULT 'PENDING';"))
        except Exception:
            pass
            
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS execution_traces (
                    id VARCHAR(100) PRIMARY KEY,
                    task_id VARCHAR(100) NOT NULL,
                    stdout_log TEXT,
                    stderr_log TEXT,
                    execution_time_ms FLOAT,
                    exit_code INTEGER,
                    status VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
        except Exception as e:
            print(f"Failed to create execution_traces: {e}")

        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS scientific_experiments (
                    id VARCHAR(100) PRIMARY KEY,
                    thesis_id VARCHAR(100) NOT NULL,
                    methodology TEXT,
                    trace_id VARCHAR(100),
                    p_value FLOAT,
                    confidence_score FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
        except Exception as e:
            print(f"Failed to create scientific_experiments: {e}")

    print("Done fixing postgres db!")

if __name__ == "__main__":
    asyncio.run(fix_db())
