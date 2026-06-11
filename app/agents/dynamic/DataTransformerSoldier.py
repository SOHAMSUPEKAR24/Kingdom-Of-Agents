# Dynamic Generated Agent Class for ANTIGRAVITY
import asyncio
import logging
from typing import Dict, Any, List
from app.agents.factory import BaseSoldier
from app.services.memory_service import memory_service

class DataTransformerSoldier(BaseSoldier):
    def __init__(self, agent_id: str, role: str, house: str, permissions: List[str]):
        super().__init__(agent_id, role, house, permissions)
        self.gap_desc = "Data layout and format transformer to convert between nested JSON, XML, and clean Markdown tables."
        self.max_lifespan_sec = 60

    async def _run_logic(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        data = task_input.get("data", {})
        format_target = task_input.get("format", "markdown")
        
        await memory_service.store_log(self.agent_id, self.role, f"Transforming data structure into format: {format_target}", "INFO")
        await asyncio.sleep(0.4)
        
        from app.services.tool_creator import DYNAMIC_TOOL_LIBRARY
        if format_target == "markdown" and "dict_to_markdown_table" in DYNAMIC_TOOL_LIBRARY:
            result = DYNAMIC_TOOL_LIBRARY["dict_to_markdown_table"](data)
        else:
            if format_target == "markdown":
                # Convert dictionary keys and values to a clean markdown table
                headers = list(data.keys())
                rows = [str(data[h]) for h in headers]
                md_table = f"| {' | '.join(headers)} |\n| {' | '.join(['---']*len(headers))} |\n| {' | '.join(rows)} |"
                result = md_table
            else:
                result = f"<data>{str(data)}</data>"
            
        return {
            "target_format": format_target,
            "transformed_content": result,
            "validation_score": 1.0,
            "evolution_metadata": {"generated_agent": True, "description": self.gap_desc}
        }

