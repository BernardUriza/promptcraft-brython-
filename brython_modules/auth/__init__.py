# PromptCraft - Auth Module for Brython
from brython_modules.auth.login_page import render_login_page
from brython_modules.auth.register_page import render_register_page
from brython_modules.auth.auth_guard import require_auth, is_authenticated, get_current_user

__all__ = [
    "render_login_page",
    "render_register_page",
    "require_auth",
    "is_authenticated",
    "get_current_user"
]
