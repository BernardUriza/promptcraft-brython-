# PromptCraft - Auth Guard for Route Protection

from browser import window
from brython_modules.api_client import TokenManager, get_current_user


# Cached current user
_current_user = None
_user_loaded = False


def is_authenticated():
    """Check if user is authenticated."""
    return TokenManager.is_authenticated()


def get_cached_user():
    """Get cached current user."""
    return _current_user


def require_auth(redirect_to="/login"):
    """
    Decorator/function to require authentication.
    Redirects to login if not authenticated.

    Usage:
        if not require_auth():
            return

        # or as route guard
        @require_auth
        def protected_page():
            ...
    """
    if not is_authenticated():
        window.location.hash = f"#{redirect_to}"
        return False
    return True


def load_current_user(on_success=None, on_error=None):
    """
    Load current user from API.
    Caches the result for future use.
    """
    global _current_user, _user_loaded

    if not is_authenticated():
        _current_user = None
        _user_loaded = False
        if on_error:
            on_error(401, "Not authenticated")
        return

    def handle_success(data):
        global _current_user, _user_loaded
        _current_user = data
        _user_loaded = True
        if on_success:
            on_success(data)

    def handle_error(status, message):
        global _current_user, _user_loaded
        _current_user = None
        _user_loaded = False
        if on_error:
            on_error(status, message)

    get_current_user(on_success=handle_success, on_error=handle_error)


def clear_user_cache():
    """Clear cached user data."""
    global _current_user, _user_loaded
    _current_user = None
    _user_loaded = False


def logout_and_redirect(redirect_to="/login"):
    """Logout user and redirect to login page."""
    from brython_modules.api_client import logout
    from brython_modules.websocket_client import disconnect_websocket

    logout()
    disconnect_websocket()
    clear_user_cache()
    window.location.hash = f"#{redirect_to}"


class AuthGuard:
    """
    Class-based auth guard for more complex scenarios.

    Usage:
        guard = AuthGuard()
        guard.check_auth(
            on_authenticated=show_dashboard,
            on_unauthenticated=show_login
        )
    """

    def __init__(self):
        self.user = None
        self.is_loading = False

    def check_auth(self, on_authenticated=None, on_unauthenticated=None, on_error=None):
        """
        Check authentication status.

        Args:
            on_authenticated: Called with user data if authenticated
            on_unauthenticated: Called if not authenticated
            on_error: Called if error occurs
        """
        if not is_authenticated():
            if on_unauthenticated:
                on_unauthenticated()
            return

        self.is_loading = True

        def handle_success(user):
            self.user = user
            self.is_loading = False
            if on_authenticated:
                on_authenticated(user)

        def handle_error(status, message):
            self.user = None
            self.is_loading = False

            if status == 401:
                # Token expired or invalid
                logout_and_redirect()
                if on_unauthenticated:
                    on_unauthenticated()
            else:
                if on_error:
                    on_error(status, message)

        load_current_user(on_success=handle_success, on_error=handle_error)

    def require_role(self, role, on_forbidden=None):
        """
        Check if user has required role.

        Args:
            role: Required role ('admin', 'verified', etc.)
            on_forbidden: Called if user doesn't have role
        """
        if not self.user:
            return False

        has_role = False

        if role == "admin":
            has_role = self.user.get("is_admin", False)
        elif role == "verified":
            has_role = self.user.get("is_verified", False)
        elif role == "active":
            has_role = self.user.get("is_active", True)

        if not has_role and on_forbidden:
            on_forbidden()

        return has_role
