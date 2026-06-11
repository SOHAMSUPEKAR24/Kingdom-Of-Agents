import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def fix_db():
    print("Fixing DB schema...")
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
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

    print("Done fixing db!")

if __name__ == "__main__":
    from sqlalchemy import text
    asyncio.run(fix_db())
