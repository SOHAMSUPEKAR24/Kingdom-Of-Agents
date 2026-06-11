import asyncio
from app.models.schemas import SQLTopologyNode, SQLTopologyEdge, SQLTask, SQLAgentState, async_session
from sqlalchemy import select

async def main():
    async with async_session() as session:
        # Get all agent states that start with 'soldier_'
        result = await session.execute(select(SQLAgentState).where(SQLAgentState.agent_id.like("soldier_%")))
        agents = result.scalars().all()
        
        for agent in agents:
            old_id = agent.agent_id
            # Just give it a nicer prefix
            new_id = old_id.replace("soldier_", "Legacy_Soldier_")
            
            # Update agent state
            agent.agent_id = new_id
            
            # Update topology nodes
            res_node = await session.execute(select(SQLTopologyNode).where(SQLTopologyNode.id == old_id))
            node = res_node.scalars().first()
            if node:
                node.id = new_id
                node.label = new_id
                
            # Update topology edges (source)
            res_edges_s = await session.execute(select(SQLTopologyEdge).where(SQLTopologyEdge.source_id == old_id))
            for edge in res_edges_s.scalars().all():
                edge.source_id = new_id
                
            # Update topology edges (target)
            res_edges_t = await session.execute(select(SQLTopologyEdge).where(SQLTopologyEdge.target_id == old_id))
            for edge in res_edges_t.scalars().all():
                edge.target_id = new_id
                
            # Update tasks
            res_tasks = await session.execute(select(SQLTask).where(SQLTask.assigned_soldier == old_id))
            for task in res_tasks.scalars().all():
                task.assigned_soldier = new_id
                
        await session.commit()
        print(f"Successfully renamed {len(agents)} old soldiers.")

if __name__ == "__main__":
    asyncio.run(main())
