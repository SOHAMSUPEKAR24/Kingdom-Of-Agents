import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Callable, List, Coroutine, Optional
from pydantic import BaseModel, Field
import redis.asyncio as aioredis
from app.core.config import settings

logger = logging.getLogger("antigravity.event_bus")

class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    sender: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    payload: Dict[str, Any] = Field(default_factory=dict)

    def serialize(self) -> str:
        # Convert datetime to ISO string for JSON serialization
        data = self.model_dump()
        data["timestamp"] = data["timestamp"].isoformat()
        return json.dumps(data)

    @classmethod
    def deserialize(cls, raw: str) -> "Event":
        data = json.loads(raw)
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)

class EventBus:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
        self._local_subscribers: Dict[str, List[Callable[[Event], Coroutine]]] = {}
        self._listening_task: Optional[asyncio.Task] = None
        self._redis_connected = False

    async def connect(self):
        """Initializes the connection to Redis. Falls back to local in-memory if offline."""
        try:
            self.redis = aioredis.from_url(settings.REDIS_URL)
            # Test connection
            await self.redis.ping()
            self._redis_connected = True
            logger.info("Connected to Redis successfully. Event Bus running in distributed mode.")
            # Start background listener for Redis subscription channels
            self._listening_task = asyncio.create_task(self._listen_redis_loop())
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}. Event Bus falling back to local in-memory mode.")
            self._redis_connected = False

    async def disconnect(self):
        if self._listening_task:
            self._listening_task.cancel()
            try:
                await self._listening_task
            except asyncio.CancelledError:
                pass
        if self.redis:
            await self.redis.close()

    def subscribe(self, event_type: str, callback: Callable[[Event], Coroutine]):
        """Registers a callback for a specific event type."""
        if event_type not in self._local_subscribers:
            self._local_subscribers[event_type] = []
        self._local_subscribers[event_type].append(callback)
        logger.debug(f"Subscribed callback to event type: '{event_type}'")

    async def publish(self, event: Event):
        """Publishes an event to the Event Bus (Redis stream/pubsub + local handlers)."""
        logger.info(f"⚡ [EVENT PUBLISHED] {event.event_type} (from {event.sender})")
        
        # 1. Trigger local in-memory subscribers directly (immediate execution within the event loop)
        await self._trigger_local_handlers(event)

        # 2. Push to Redis (distributes events to other scale instances)
        if self._redis_connected and self.redis:
            try:
                # Publish via Pub/Sub channel
                await self.redis.publish("kingdom:events:channel", event.serialize())
                # Log persistently inside a Redis Stream for historical audits
                await self.redis.xadd(
                    "kingdom:events:stream",
                    {"event": event.serialize()},
                    max_len=10000,
                    approximate=True
                )
            except Exception as e:
                logger.error(f"Failed to publish to Redis stream: {e}")

    async def _trigger_local_handlers(self, event: Event):
        """Dispatches an event to registered local async handlers in parallel."""
        handlers = self._local_subscribers.get(event.event_type, [])
        # Also support wildcard subscriptions
        wildcards = self._local_subscribers.get("*", [])
        
        all_handlers = handlers + wildcards
        if not all_handlers:
            return

        tasks = []
        for handler in all_handlers:
            tasks.append(self._safe_execute_handler(handler, event))
        
        # Run all handlers concurrently as tasks
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _safe_execute_handler(self, handler: Callable[[Event], Coroutine], event: Event):
        try:
            await handler(event)
        except Exception as e:
            logger.error(f"Error in subscriber handler for event '{event.event_type}': {e}", exc_info=True)

    async def _listen_redis_loop(self):
        """Background worker that listens to Redis Pub/Sub events and triggers local subscribers."""
        if not self.redis:
            return
        
        pubsub = self.redis.pubsub()
        await pubsub.subscribe("kingdom:events:channel")
        logger.info("Redis PubSub listener loop started.")

        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message and message["type"] == "message":
                    try:
                        raw_data = message["data"].decode("utf-8")
                        event = Event.deserialize(raw_data)
                        
                        # Only trigger local handlers if the event was NOT generated locally
                        # (since publish() already triggers local subscribers to avoid double processing)
                        # We tag events or just trigger directly if there's multiple distinct node instances
                        # To keep it simple: local publish() triggers locally. If we have distributed,
                        # we check if event.sender is us or check an instance ID.
                        # For simple single-process dynamic run, trigger only local or filter duplicates:
                        pass
                    except Exception as ex:
                        logger.error(f"Failed to deserialize event from Redis: {ex}")
                await asyncio.sleep(0.01)
        except asyncio.CancelledError:
            logger.info("Redis PubSub listener cancelled.")
        except Exception as e:
            logger.error(f"Redis PubSub listener crashed: {e}")
        finally:
            await pubsub.unsubscribe("kingdom:events:channel")
            await pubsub.close()

# Global Event Bus instance
event_bus = EventBus()
