# PromptCraft - API Client for Brython
# Uses window.fetch for REST API calls

from browser import window, document
import json

# API Configuration
API_BASE_URL = "/api/v1"


class TokenManager:
    """Manage JWT tokens in localStorage."""

    ACCESS_TOKEN_KEY = "promptcraft_access_token"
    REFRESH_TOKEN_KEY = "promptcraft_refresh_token"

    @classmethod
    def get_access_token(cls):
        """Get access token from localStorage."""
        return window.localStorage.getItem(cls.ACCESS_TOKEN_KEY)

    @classmethod
    def get_refresh_token(cls):
        """Get refresh token from localStorage."""
        return window.localStorage.getItem(cls.REFRESH_TOKEN_KEY)

    @classmethod
    def set_tokens(cls, access_token, refresh_token):
        """Store both tokens."""
        window.localStorage.setItem(cls.ACCESS_TOKEN_KEY, access_token)
        window.localStorage.setItem(cls.REFRESH_TOKEN_KEY, refresh_token)

    @classmethod
    def clear_tokens(cls):
        """Remove all tokens (logout)."""
        window.localStorage.removeItem(cls.ACCESS_TOKEN_KEY)
        window.localStorage.removeItem(cls.REFRESH_TOKEN_KEY)

    @classmethod
    def is_authenticated(cls):
        """Check if user has access token."""
        return cls.get_access_token() is not None


class APIClient:
    """
    REST API client using window.fetch.

    Usage:
        api = APIClient()

        # With callbacks
        api.get("/lessons", on_success=handle_lessons, on_error=handle_error)

        # POST with data
        api.post("/auth/login", {"email": "...", "password": "..."}, on_success=...)
    """

    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url

    def _get_headers(self, include_auth=True):
        """Build request headers."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if include_auth:
            token = TokenManager.get_access_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"

        return headers

    def _handle_response(self, response, on_success, on_error):
        """Process fetch response."""
        def process_json(data):
            if response.ok:
                if on_success:
                    on_success(data)
            else:
                error_msg = data.get("detail", "Unknown error")
                if on_error:
                    on_error(response.status, error_msg)

        def handle_error(err):
            if on_error:
                on_error(0, str(err))

        # Check for 401 and try token refresh
        if response.status == 401:
            self._try_refresh_token(
                on_success=lambda: self._retry_request(response, on_success, on_error),
                on_error=lambda: on_error(401, "Session expired") if on_error else None
            )
            return

        response.json().then(process_json).catch(handle_error)

    def _try_refresh_token(self, on_success, on_error):
        """Try to refresh the access token."""
        refresh_token = TokenManager.get_refresh_token()
        if not refresh_token:
            on_error()
            return

        def handle_refresh(data):
            TokenManager.set_tokens(data["access_token"], data["refresh_token"])
            on_success()

        def handle_error(status, msg):
            TokenManager.clear_tokens()
            on_error()

        self.post(
            "/auth/refresh",
            {"refresh_token": refresh_token},
            on_success=handle_refresh,
            on_error=handle_error,
            include_auth=False
        )

    def get(self, endpoint, on_success=None, on_error=None, params=None):
        """Make GET request."""
        url = f"{self.base_url}{endpoint}"

        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query_string}"

        options = {
            "method": "GET",
            "headers": self._get_headers()
        }

        def handle_response(response):
            self._handle_response(response, on_success, on_error)

        def handle_error(err):
            if on_error:
                on_error(0, str(err))

        window.fetch(url, options).then(handle_response).catch(handle_error)

    def post(self, endpoint, data=None, on_success=None, on_error=None, include_auth=True):
        """Make POST request."""
        url = f"{self.base_url}{endpoint}"

        options = {
            "method": "POST",
            "headers": self._get_headers(include_auth),
            "body": json.dumps(data) if data else "{}"
        }

        def handle_response(response):
            self._handle_response(response, on_success, on_error)

        def handle_error(err):
            if on_error:
                on_error(0, str(err))

        window.fetch(url, options).then(handle_response).catch(handle_error)

    def patch(self, endpoint, data=None, on_success=None, on_error=None):
        """Make PATCH request."""
        url = f"{self.base_url}{endpoint}"

        options = {
            "method": "PATCH",
            "headers": self._get_headers(),
            "body": json.dumps(data) if data else "{}"
        }

        def handle_response(response):
            self._handle_response(response, on_success, on_error)

        def handle_error(err):
            if on_error:
                on_error(0, str(err))

        window.fetch(url, options).then(handle_response).catch(handle_error)

    def delete(self, endpoint, on_success=None, on_error=None):
        """Make DELETE request."""
        url = f"{self.base_url}{endpoint}"

        options = {
            "method": "DELETE",
            "headers": self._get_headers()
        }

        def handle_response(response):
            self._handle_response(response, on_success, on_error)

        def handle_error(err):
            if on_error:
                on_error(0, str(err))

        window.fetch(url, options).then(handle_response).catch(handle_error)


# Singleton instance
api = APIClient()


# ============= Auth API =============

def login(email, password, on_success=None, on_error=None):
    """Login user and store tokens."""
    def handle_success(data):
        TokenManager.set_tokens(data["access_token"], data["refresh_token"])
        if on_success:
            on_success(data)

    api.post(
        "/auth/login",
        {"email": email, "password": password},
        on_success=handle_success,
        on_error=on_error,
        include_auth=False
    )


def register(email, username, password, display_name=None, on_success=None, on_error=None):
    """Register new user."""
    data = {
        "email": email,
        "username": username,
        "password": password
    }
    if display_name:
        data["display_name"] = display_name

    def handle_success(data):
        TokenManager.set_tokens(data["access_token"], data["refresh_token"])
        if on_success:
            on_success(data)

    api.post("/auth/register", data, on_success=handle_success, on_error=on_error, include_auth=False)


def logout():
    """Logout user (clear tokens)."""
    TokenManager.clear_tokens()


def get_current_user(on_success=None, on_error=None):
    """Get current authenticated user."""
    api.get("/auth/me", on_success=on_success, on_error=on_error)


# ============= Lessons API =============

def get_lessons(page=1, per_page=20, category=None, on_success=None, on_error=None):
    """Get list of lessons."""
    params = {"page": page, "per_page": per_page}
    if category:
        params["category"] = category
    api.get("/lessons", on_success=on_success, on_error=on_error, params=params)


def get_lesson(slug, on_success=None, on_error=None):
    """Get single lesson by slug."""
    api.get(f"/lessons/{slug}", on_success=on_success, on_error=on_error)


def start_lesson(slug, on_success=None, on_error=None):
    """Start a lesson (create progress)."""
    api.post(f"/lessons/{slug}/start", on_success=on_success, on_error=on_error)


def update_lesson_progress(slug, data, on_success=None, on_error=None):
    """Update lesson progress."""
    api.patch(f"/lessons/{slug}/progress", data, on_success=on_success, on_error=on_error)


def complete_lesson(slug, on_success=None, on_error=None):
    """Mark lesson as completed."""
    api.post(f"/lessons/{slug}/complete", on_success=on_success, on_error=on_error)


def submit_exercise(slug, answer, on_success=None, on_error=None):
    """Submit lesson exercise."""
    api.post(f"/lessons/{slug}/exercise", {"answer": answer}, on_success=on_success, on_error=on_error)


# ============= Puzzles API =============

def get_puzzles(page=1, per_page=20, category=None, on_success=None, on_error=None):
    """Get list of puzzles."""
    params = {"page": page, "per_page": per_page}
    if category:
        params["category"] = category
    api.get("/puzzles", on_success=on_success, on_error=on_error, params=params)


def get_puzzle(slug, on_success=None, on_error=None):
    """Get single puzzle by slug."""
    api.get(f"/puzzles/{slug}", on_success=on_success, on_error=on_error)


def get_daily_puzzle(on_success=None, on_error=None):
    """Get today's daily puzzle."""
    api.get("/puzzles/daily", on_success=on_success, on_error=on_error)


def start_puzzle(slug, on_success=None, on_error=None):
    """Start a puzzle attempt."""
    api.post(f"/puzzles/{slug}/start", on_success=on_success, on_error=on_error)


def submit_puzzle(slug, attempt_id, solution, time_taken, on_success=None, on_error=None):
    """Submit puzzle solution."""
    data = {
        "attempt_id": attempt_id,
        "solution": solution,
        "time_taken_seconds": time_taken
    }
    api.post(f"/puzzles/{slug}/submit", data, on_success=on_success, on_error=on_error)


def get_puzzle_hint(slug, attempt_id, on_success=None, on_error=None):
    """Request a hint for puzzle."""
    api.post(f"/puzzles/{slug}/hint", {"attempt_id": attempt_id}, on_success=on_success, on_error=on_error)


# ============= Gamification API =============

def get_gamification_stats(on_success=None, on_error=None):
    """Get user's gamification stats."""
    api.get("/gamification/stats", on_success=on_success, on_error=on_error)


def get_xp_history(page=1, per_page=20, on_success=None, on_error=None):
    """Get XP transaction history."""
    api.get("/gamification/xp/history", on_success=on_success, on_error=on_error,
            params={"page": page, "per_page": per_page})


def get_badges(on_success=None, on_error=None):
    """Get all badges with progress."""
    api.get("/gamification/badges", on_success=on_success, on_error=on_error)


def get_leaderboard(type="weekly", on_success=None, on_error=None):
    """Get leaderboard."""
    api.get("/gamification/leaderboard", on_success=on_success, on_error=on_error,
            params={"type": type})


def get_streak_status(on_success=None, on_error=None):
    """Get streak status."""
    api.get("/gamification/streak", on_success=on_success, on_error=on_error)


def use_streak_freeze(on_success=None, on_error=None):
    """Use a streak freeze."""
    api.post("/gamification/streak/freeze", on_success=on_success, on_error=on_error)


def get_daily_challenge(on_success=None, on_error=None):
    """Get today's daily challenge."""
    api.get("/gamification/daily-challenge", on_success=on_success, on_error=on_error)


def update_daily_goal(goal, on_success=None, on_error=None):
    """Update daily XP goal."""
    api.patch("/gamification/settings/daily-goal", {"daily_xp_goal": goal},
              on_success=on_success, on_error=on_error)


# ============= Users API =============

def get_user_profile(username, on_success=None, on_error=None):
    """Get public user profile."""
    api.get(f"/users/{username}", on_success=on_success, on_error=on_error)


def update_my_profile(data, on_success=None, on_error=None):
    """Update current user's profile."""
    api.patch("/users/me", data, on_success=on_success, on_error=on_error)
