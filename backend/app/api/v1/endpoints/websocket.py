# PromptCraft - WebSocket Endpoints

import json
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy import select

from app.db.session import async_session_factory
from app.db.redis import get_redis_sync, RedisKeys
from app.core.security import decode_token, verify_token_type
from app.models.user import User

router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections."""

    def __init__(self):
        # user_id -> list of WebSocket connections
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and store connection."""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        """Remove connection."""
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal(self, user_id: int, message: dict):
        """Send message to specific user."""
        if user_id in self.active_connections:
            message_json = json.dumps(message)
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message_json)
                except Exception:
                    pass

    async def broadcast(self, message: dict, exclude_user: Optional[int] = None):
        """Broadcast message to all connected users."""
        message_json = json.dumps(message)
        for user_id, connections in self.active_connections.items():
            if exclude_user and user_id == exclude_user:
                continue
            for connection in connections:
                try:
                    await connection.send_text(message_json)
                except Exception:
                    pass

    def get_online_count(self) -> int:
        """Get number of online users."""
        return len(self.active_connections)

    def is_online(self, user_id: int) -> bool:
        """Check if user is online."""
        return user_id in self.active_connections


# Global connection manager
manager = ConnectionManager()


async def get_user_from_token(token: str) -> Optional[User]:
    """Verify token and get user."""
    payload = verify_token_type(token, "access")
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    async with async_session_factory() as db:
        result = await db.execute(
            select(User).where(User.id == int(user_id))
        )
        return result.scalar_one_or_none()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for real-time updates.

    Protocol:
    1. Client connects with token in query params: /ws?token=xxx
    2. Server validates token and accepts connection
    3. Server sends events:
       - xp_earned: When user earns XP
       - badge_earned: When user earns a badge
       - level_up: When user levels up
       - streak_update: When streak changes
       - leaderboard_update: When leaderboard position changes
       - daily_goal_complete: When daily goal is achieved
    """
    # Get token from query params
    token = websocket.query_params.get("token")

    if not token:
        await websocket.close(code=4001, reason="Token required")
        return

    # Verify token and get user
    user = await get_user_from_token(token)
    if not user:
        await websocket.close(code=4002, reason="Invalid token")
        return

    if not user.is_active:
        await websocket.close(code=4003, reason="User inactive")
        return

    # Accept connection
    await manager.connect(websocket, user.id)

    # Send connection confirmation
    await manager.send_personal(user.id, {
        "type": "connected",
        "data": {
            "user_id": user.id,
            "username": user.username,
            "online_count": manager.get_online_count(),
            "timestamp": datetime.utcnow().isoformat()
        }
    })

    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                message_type = message.get("type")

                if message_type == "ping":
                    # Respond to ping
                    await manager.send_personal(user.id, {
                        "type": "pong",
                        "data": {"timestamp": datetime.utcnow().isoformat()}
                    })

                elif message_type == "subscribe":
                    # Subscribe to specific channels
                    channels = message.get("channels", [])
                    await manager.send_personal(user.id, {
                        "type": "subscribed",
                        "data": {"channels": channels}
                    })

            except json.JSONDecodeError:
                await manager.send_personal(user.id, {
                    "type": "error",
                    "data": {"message": "Invalid JSON"}
                })

    except WebSocketDisconnect:
        manager.disconnect(websocket, user.id)


# Helper functions for sending notifications from other parts of the app

async def notify_xp_earned(user_id: int, amount: int, source: str, total_xp: int):
    """Notify user of XP earned."""
    await manager.send_personal(user_id, {
        "type": "xp_earned",
        "data": {
            "amount": amount,
            "source": source,
            "total_xp": total_xp,
            "timestamp": datetime.utcnow().isoformat()
        }
    })


async def notify_badge_earned(user_id: int, badge_name: str, badge_icon: str, xp_reward: int):
    """Notify user of badge earned."""
    await manager.send_personal(user_id, {
        "type": "badge_earned",
        "data": {
            "badge_name": badge_name,
            "badge_icon": badge_icon,
            "xp_reward": xp_reward,
            "timestamp": datetime.utcnow().isoformat()
        }
    })


async def notify_level_up(user_id: int, new_level: int, xp_to_next: int):
    """Notify user of level up."""
    await manager.send_personal(user_id, {
        "type": "level_up",
        "data": {
            "new_level": new_level,
            "xp_to_next": xp_to_next,
            "timestamp": datetime.utcnow().isoformat()
        }
    })


async def notify_streak_update(user_id: int, current_streak: int, is_at_risk: bool):
    """Notify user of streak update."""
    await manager.send_personal(user_id, {
        "type": "streak_update",
        "data": {
            "current_streak": current_streak,
            "is_at_risk": is_at_risk,
            "timestamp": datetime.utcnow().isoformat()
        }
    })


async def notify_daily_goal_complete(user_id: int, xp_earned: int, goal: int):
    """Notify user of daily goal completion."""
    await manager.send_personal(user_id, {
        "type": "daily_goal_complete",
        "data": {
            "xp_earned": xp_earned,
            "goal": goal,
            "timestamp": datetime.utcnow().isoformat()
        }
    })


async def broadcast_leaderboard_update(leaderboard_type: str):
    """Broadcast leaderboard update to all users."""
    await manager.broadcast({
        "type": "leaderboard_update",
        "data": {
            "leaderboard_type": leaderboard_type,
            "timestamp": datetime.utcnow().isoformat()
        }
    })
