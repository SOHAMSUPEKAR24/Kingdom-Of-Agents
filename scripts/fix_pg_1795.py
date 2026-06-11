import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def fix_db():
    print("Fixing PostgreSQL DB schema for 17.95...")
    engine = create_async_engine("postgresql+asyncpg://king:kingdom_auth_key@localhost:5432/antigravity_db", echo=True)
    async with engine.begin() as conn:
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS research_campaigns (
                    id VARCHAR(100) PRIMARY KEY,
                    capability VARCHAR(100) NOT NULL,
                    token_budget FLOAT DEFAULT 100000.0,
                    tokens_spent FLOAT DEFAULT 0.0,
                    experiment_budget INTEGER DEFAULT 50,
                    experiments_run INTEGER DEFAULT 0,
                    success_criteria TEXT NOT NULL,
                    status VARCHAR(50) DEFAULT 'ACTIVE',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """))
        except Exception as e:
            print(f"Failed to create research_campaigns: {e}")

        try:
            await conn.execute(text("ALTER TABLE execution_traces ADD COLUMN llm_bypassed BOOLEAN DEFAULT FALSE;"))
        except Exception:
            pass
            
        try:
            await conn.execute(text("ALTER TABLE execution_traces ADD COLUMN model_calls INTEGER DEFAULT 1;"))
        except Exception:
            pass
            
        try:
            await conn.execute(text("ALTER TABLE generated_artifacts ADD COLUMN capability VARCHAR(100);"))
        except Exception:
            pass
            
        try:
            await conn.execute(text("ALTER TABLE scientific_experiments ADD COLUMN capability VARCHAR(100) DEFAULT 'UNKNOWN';"))
        except Exception:
            pass
            
        try:
            await conn.execute(text("ALTER TABLE scientific_experiments ADD COLUMN campaign_id VARCHAR(100) DEFAULT 'UNKNOWN';"))
        except Exception:
            pass
            
        # Also fix scientific_experiments dropping old fields if they exist
        try:
            await conn.execute(text("ALTER TABLE scientific_experiments DROP COLUMN title;"))
        except Exception:
            pass

    print("Done fixing postgres db!")

if __name__ == "__main__":
    asyncio.run(fix_db())
