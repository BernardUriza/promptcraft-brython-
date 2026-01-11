# PromptCraft - Mock API Client
# Este es un cliente simulado para funcionamiento sin backend
# Todo el progreso se guarda en localStorage (ver state.py)

from browser import window

# ============================================================
# NOTA: Este proyecto funciona 100% en el navegador.
# No necesita backend - todo se guarda en localStorage.
# Este archivo existe por compatibilidad con el código existente.
# ============================================================


class MockTokenManager:
    """Simulación de gestión de tokens (no hay autenticación real)."""

    @classmethod
    def is_authenticated(cls):
        """Siempre autenticado en modo local."""
        return True

    @classmethod
    def get_access_token(cls):
        return "mock_token"

    @classmethod
    def set_tokens(cls, access_token, refresh_token):
        pass  # No necesario en modo mock

    @classmethod
    def clear_tokens(cls):
        pass  # No necesario en modo mock


# Alias para compatibilidad
TokenManager = MockTokenManager


class MockAPIClient:
    """
    Cliente API simulado.

    En lugar de hacer llamadas HTTP reales, este cliente
    simplemente invoca los callbacks de éxito con datos mock.
    El progreso real del usuario se gestiona en state.py usando localStorage.
    """

    def __init__(self, base_url=None):
        self.base_url = base_url or ""

    def get(self, endpoint, on_success=None, on_error=None, params=None):
        """Simula GET request - retorna datos vacíos."""
        if on_success:
            # Usar setTimeout para simular asincronía
            window.setTimeout(lambda: on_success({}), 10)

    def post(self, endpoint, data=None, on_success=None, on_error=None, include_auth=True):
        """Simula POST request - retorna éxito."""
        if on_success:
            window.setTimeout(lambda: on_success({"success": True}), 10)

    def patch(self, endpoint, data=None, on_success=None, on_error=None):
        """Simula PATCH request - retorna éxito."""
        if on_success:
            window.setTimeout(lambda: on_success({"success": True}), 10)

    def delete(self, endpoint, on_success=None, on_error=None):
        """Simula DELETE request - retorna éxito."""
        if on_success:
            window.setTimeout(lambda: on_success({"success": True}), 10)


# Singleton instance
api = MockAPIClient()


# ============= Auth API (Mock) =============

def login(email, password, on_success=None, on_error=None):
    """Login simulado - siempre exitoso."""
    if on_success:
        on_success({"user": {"email": email, "username": "local_user"}})


def register(email, username, password, display_name=None, on_success=None, on_error=None):
    """Registro simulado - siempre exitoso."""
    if on_success:
        on_success({"user": {"email": email, "username": username}})


def logout():
    """Logout simulado."""
    pass


def get_current_user(on_success=None, on_error=None):
    """Retorna usuario local."""
    if on_success:
        on_success({"username": "local_user", "email": "local@example.com"})


# ============= Lessons API (Mock) =============
# Las lecciones reales se cargan desde content.py, no desde API

def get_lessons(page=1, per_page=20, category=None, on_success=None, on_error=None):
    """Las lecciones se cargan de content.py, no de API."""
    if on_success:
        on_success({"lessons": [], "total": 0})


def get_lesson(slug, on_success=None, on_error=None):
    """La lección se carga de content.py."""
    if on_success:
        on_success({})


def start_lesson(slug, on_success=None, on_error=None):
    """Inicio de lección - éxito simulado."""
    if on_success:
        on_success({"started": True})


def update_lesson_progress(slug, data, on_success=None, on_error=None):
    """Progreso se guarda en localStorage via state.py."""
    if on_success:
        on_success({"updated": True})


def complete_lesson(slug, on_success=None, on_error=None):
    """Completar lección - éxito simulado."""
    if on_success:
        on_success({"completed": True})


def submit_exercise(slug, answer, on_success=None, on_error=None):
    """Ejercicio - éxito simulado."""
    if on_success:
        on_success({"correct": True})


# ============= Puzzles API (Mock) =============
# Los puzzles se cargan desde puzzles.json, no desde API

def get_puzzles(page=1, per_page=20, category=None, on_success=None, on_error=None):
    """Los puzzles se cargan de puzzles.json."""
    if on_success:
        on_success({"puzzles": [], "total": 0})


def get_puzzle(slug, on_success=None, on_error=None):
    """El puzzle se carga de puzzles.json."""
    if on_success:
        on_success({})


def get_daily_puzzle(on_success=None, on_error=None):
    """Daily puzzle mock."""
    if on_success:
        on_success({})


def start_puzzle(slug, on_success=None, on_error=None):
    """Inicio de puzzle - éxito simulado."""
    if on_success:
        on_success({"attempt_id": "local_attempt"})


def submit_puzzle(slug, attempt_id, solution, time_taken, on_success=None, on_error=None):
    """Submit puzzle - éxito simulado (la validación real está en engine.py)."""
    if on_success:
        on_success({"correct": True})


def get_puzzle_hint(slug, attempt_id, on_success=None, on_error=None):
    """Hint - las pistas se gestionan localmente."""
    if on_success:
        on_success({"hint": None})


# ============= Gamification API (Mock) =============
# La gamificación real está en brython_modules/gamification/

def get_gamification_stats(on_success=None, on_error=None):
    """Stats se obtienen de localStorage via state.py."""
    if on_success:
        on_success({})


def get_xp_history(page=1, per_page=20, on_success=None, on_error=None):
    """Historial local."""
    if on_success:
        on_success({"history": []})


def get_badges(on_success=None, on_error=None):
    """Badges se gestionan en badges.py."""
    if on_success:
        on_success({"badges": []})


def get_leaderboard(type="weekly", on_success=None, on_error=None):
    """No hay leaderboard en modo local."""
    if on_success:
        on_success({"leaderboard": []})


def get_streak_status(on_success=None, on_error=None):
    """Streak se gestiona en streaks.py."""
    if on_success:
        on_success({})


def use_streak_freeze(on_success=None, on_error=None):
    """Streak freeze mock."""
    if on_success:
        on_success({"used": True})


def get_daily_challenge(on_success=None, on_error=None):
    """Daily challenge mock."""
    if on_success:
        on_success({})


def update_daily_goal(goal, on_success=None, on_error=None):
    """Goal se guarda en localStorage."""
    if on_success:
        on_success({"goal": goal})


# ============= Users API (Mock) =============

def get_user_profile(username, on_success=None, on_error=None):
    """Perfil local."""
    if on_success:
        on_success({"username": username})


def update_my_profile(data, on_success=None, on_error=None):
    """Perfil se guarda en localStorage."""
    if on_success:
        on_success(data)
