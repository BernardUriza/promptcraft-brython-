# PromptCraft - Pages
# Páginas de la aplicación

from .home import home_page
from .lessons import lessons_page
from .lesson_detail import lesson_detail_page
from .puzzles import puzzles_page
from .puzzle import puzzle_page
from .playground import playground_page
from .profile import profile_page
from .badges import badges_page

# Nuevas páginas de práctica y evaluación
from .assessment import assessment_page
from .practice import practice_page, practice_exercise_page
from .claude_exercises import claude_exercises_page, claude_exercise_detail_page
from .final_project import final_project_page
from .guides import guides_page

__all__ = [
    'home_page',
    'lessons_page',
    'lesson_detail_page',
    'puzzles_page',
    'puzzle_page',
    'playground_page',
    'profile_page',
    'badges_page',
    # Nuevas páginas
    'assessment_page',
    'practice_page',
    'practice_exercise_page',
    'claude_exercises_page',
    'claude_exercise_detail_page',
    'final_project_page',
    'guides_page',
]
