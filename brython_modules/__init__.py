# PromptCraft - Brython Modules
# Curso Interactivo de Prompt Engineering

__version__ = "2.0.0"
__author__ = "PromptCraft Team"

# Solo importaciones esenciales para evitar errores
from .state import AppState, get_state
from .router import Router, navigate
from .app import init_app

__all__ = [
    'AppState',
    'get_state',
    'Router',
    'navigate',
    'init_app',
]
