import logging
import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.world_interaction_engine import world_interaction_engine

logger = logging.getLogger(__name__)

class BrowserOperationsEngine:
    """
    Provides isolated, safe, and rate-limited browser automation for the civilization.
    Focuses on docs retrieval, testing, and research.
    """
    def __init__(self):
        self._semaphore = asyncio.Semaphore(2) # Strict rate limiting (max 2 concurrent browser sessions)

    async def fetch_page_content(self, agent_id: str, url: str, session: AsyncSession) -> Dict[str, Any]:
        """
        Navigates to a URL, extracts text content safely.
        """
        async with self._semaphore:
            success = False
            outcome = ""
            try:
                async with async_playwright() as p:
                    # Run strictly with isolated context
                    browser = await p.chromium.launch(
                        headless=True,
                        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
                    )
                    context = await browser.new_context(
                        viewport={'width': 1280, 'height': 800},
                        user_agent='ANTIGRAVITY-Civilization-Knight0/1.0'
                    )
                    page = await context.new_page()
                    
                    # Set a timeout for navigation (30s)
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                    
                    # Extract raw text or markdown-like representation
                    content = await page.evaluate('document.body.innerText')
                    title = await page.title()
                    
                    success = True
                    outcome = f"Title: {title}\nExtracted {len(content)} characters."
                    
                    await context.close()
                    await browser.close()
                    
                    await world_interaction_engine.log_interaction(
                        agent_id, "BROWSER_FETCH", url, "Navigated and extracted text", outcome, success, session
                    )
                    return {"success": True, "title": title, "content": content}
            except Exception as e:
                outcome = str(e)
                logger.error(f"❌ [BROWSER OPS] Failed to fetch {url}: {outcome}")
                await world_interaction_engine.log_interaction(
                    agent_id, "BROWSER_FETCH", url, "Navigation attempt failed", outcome, False, session
                )
                return {"success": False, "error": outcome}

browser_operations_engine = BrowserOperationsEngine()
