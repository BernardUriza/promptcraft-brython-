# PromptCraft - WebSocket Client for Brython
# Real-time notifications using browser.websocket

from browser import window, document
import json

from brython_modules.api_client import TokenManager

# WebSocket URL
WS_BASE_URL = "ws://localhost/api/v1/ws"


class WebSocketClient:
    """
    WebSocket client for real-time notifications.

    Events received:
    - connected: Connection established
    - xp_earned: User earned XP
    - badge_earned: User earned a badge
    - level_up: User leveled up
    - streak_update: Streak changed
    - daily_goal_complete: Daily goal achieved
    - leaderboard_update: Leaderboard changed

    Usage:
        ws = WebSocketClient()
        ws.on("xp_earned", lambda data: print(f"Earned {data['amount']} XP!"))
        ws.connect()
    """

    def __init__(self, url=None):
        self.url = url or WS_BASE_URL
        self.socket = None
        self.handlers = {}
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.reconnect_delay = 1000  # ms
        self.ping_interval = None
        self.is_connected = False

    def connect(self):
        """Connect to WebSocket server."""
        token = TokenManager.get_access_token()
        if not token:
            print("WebSocket: No auth token, skipping connection")
            return

        url = f"{self.url}?token={token}"

        try:
            self.socket = window.WebSocket.new(url)
            self._setup_handlers()
        except Exception as e:
            print(f"WebSocket: Connection failed - {e}")
            self._schedule_reconnect()

    def _setup_handlers(self):
        """Setup WebSocket event handlers."""

        def on_open(event):
            self.is_connected = True
            self.reconnect_attempts = 0
            print("WebSocket: Connected")
            self._emit("connected", {})
            self._start_ping()

        def on_message(event):
            try:
                data = json.loads(event.data)
                event_type = data.get("type", "unknown")
                event_data = data.get("data", {})
                self._emit(event_type, event_data)
            except json.JSONDecodeError:
                print(f"WebSocket: Invalid JSON received")

        def on_close(event):
            self.is_connected = False
            self._stop_ping()
            print(f"WebSocket: Closed (code={event.code})")
            self._emit("disconnected", {"code": event.code})

            # Don't reconnect on auth errors
            if event.code not in [4001, 4002, 4003]:
                self._schedule_reconnect()

        def on_error(event):
            print(f"WebSocket: Error")
            self._emit("error", {})

        self.socket.onopen = on_open
        self.socket.onmessage = on_message
        self.socket.onclose = on_close
        self.socket.onerror = on_error

    def _start_ping(self):
        """Start ping interval to keep connection alive."""
        def send_ping():
            if self.is_connected:
                self.send("ping", {})

        self.ping_interval = window.setInterval(send_ping, 30000)  # 30s

    def _stop_ping(self):
        """Stop ping interval."""
        if self.ping_interval:
            window.clearInterval(self.ping_interval)
            self.ping_interval = None

    def _schedule_reconnect(self):
        """Schedule reconnection attempt."""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            print("WebSocket: Max reconnect attempts reached")
            return

        self.reconnect_attempts += 1
        delay = self.reconnect_delay * (2 ** (self.reconnect_attempts - 1))

        print(f"WebSocket: Reconnecting in {delay}ms (attempt {self.reconnect_attempts})")
        window.setTimeout(self.connect, delay)

    def disconnect(self):
        """Disconnect from WebSocket server."""
        self._stop_ping()
        if self.socket:
            self.socket.close()
            self.socket = None
        self.is_connected = False

    def send(self, event_type, data):
        """Send message to server."""
        if not self.is_connected:
            print("WebSocket: Not connected, cannot send")
            return

        message = json.dumps({
            "type": event_type,
            "data": data
        })
        self.socket.send(message)

    def on(self, event_type, handler):
        """Register event handler."""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def off(self, event_type, handler=None):
        """Remove event handler."""
        if event_type in self.handlers:
            if handler:
                self.handlers[event_type] = [h for h in self.handlers[event_type] if h != handler]
            else:
                del self.handlers[event_type]

    def _emit(self, event_type, data):
        """Emit event to handlers."""
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    handler(data)
                except Exception as e:
                    print(f"WebSocket: Handler error for {event_type} - {e}")


# Singleton instance
ws = WebSocketClient()


# ============= Notification Handlers =============

def show_xp_notification(data):
    """Show XP earned notification."""
    amount = data.get("amount", 0)
    source = data.get("source", "activity")
    _show_toast(f"+{amount} XP", f"From {source}", "success")


def show_badge_notification(data):
    """Show badge earned notification."""
    name = data.get("badge_name", "Badge")
    icon = data.get("badge_icon", "🏆")
    _show_toast(f"{icon} Badge Earned!", name, "achievement")


def show_level_up_notification(data):
    """Show level up notification."""
    level = data.get("new_level", 1)
    _show_toast(f"🎉 Level Up!", f"You reached level {level}", "level-up")


def show_streak_notification(data):
    """Show streak update notification."""
    streak = data.get("current_streak", 0)
    at_risk = data.get("is_at_risk", False)

    if at_risk:
        _show_toast("🔥 Streak at Risk!", "Complete an activity today", "warning")
    else:
        _show_toast(f"🔥 {streak} Day Streak!", "Keep it up!", "success")


def show_daily_goal_notification(data):
    """Show daily goal complete notification."""
    goal = data.get("goal", 50)
    _show_toast("🎯 Daily Goal Complete!", f"You earned {goal} XP today", "success")


def _show_toast(title, message, type="info"):
    """Show toast notification."""
    # Create toast element
    toast = document.createElement("div")
    toast.className = f"toast toast-{type}"
    toast.innerHTML = f"""
        <div class="toast-title">{title}</div>
        <div class="toast-message">{message}</div>
    """

    # Add to container
    container = document.getElementById("toast-container")
    if not container:
        container = document.createElement("div")
        container.id = "toast-container"
        container.className = "fixed top-4 right-4 z-50 flex flex-col gap-2"
        document.body.appendChild(container)

    container.appendChild(toast)

    # Auto remove after 4 seconds
    def remove_toast():
        if toast.parentNode:
            toast.parentNode.removeChild(toast)

    window.setTimeout(remove_toast, 4000)


def setup_notifications():
    """Setup all notification handlers."""
    ws.on("xp_earned", show_xp_notification)
    ws.on("badge_earned", show_badge_notification)
    ws.on("level_up", show_level_up_notification)
    ws.on("streak_update", show_streak_notification)
    ws.on("daily_goal_complete", show_daily_goal_notification)


def connect_websocket():
    """Connect WebSocket and setup handlers."""
    if TokenManager.is_authenticated():
        setup_notifications()
        ws.connect()


def disconnect_websocket():
    """Disconnect WebSocket."""
    ws.disconnect()
