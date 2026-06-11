import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test():
    try:
        engine = create_async_engine('postgresql+asyncpg://king:kingdom_auth_key@localhost:5432/antigravity_db')
        async with engine.connect() as conn:
            print('Connection successful!')
    except Exception as e:
        print(f'Error: {e}')

asyncio.run(test())
