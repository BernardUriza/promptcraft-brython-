#!/usr/bin/env python
"""
PromptCraft - Seed Data Script

Populates the database with initial lessons, puzzles, and badges.
Usage: python -m scripts.seed_data
"""

import asyncio
import json
import sys
import os
from datetime import datetime, date

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.db.session import async_session_factory
from app.models.lesson import Lesson, DifficultyLevel, LessonCategory
from app.models.puzzle import Puzzle, PuzzleCategory
from app.models.gamification import Badge, BadgeRarity, BadgeCategory, DailyChallenge


# Seed data for lessons
LESSONS_DATA = [
    {
        "slug": "what-is-prompt-engineering",
        "title": "¿Qué es Prompt Engineering?",
        "description": "Aprende los fundamentos de la ingeniería de prompts y por qué es crucial para trabajar con IA.",
        "icon": "🎯",
        "category": LessonCategory.FUNDAMENTALS,
        "difficulty": DifficultyLevel.BEGINNER,
        "duration_minutes": 10,
        "xp_reward": 50,
        "order": 1,
        "content": json.dumps([
            {"type": "text", "title": "Introducción", "content": "La ingeniería de prompts es el arte de comunicarse efectivamente con modelos de IA."},
            {"type": "text", "title": "Por qué importa", "content": "Un buen prompt puede ser la diferencia entre una respuesta útil y una inútil."},
            {"type": "tip", "content": "Piensa en el prompt como instrucciones para un asistente muy capaz pero literal."}
        ]),
        "objectives": json.dumps([
            "Entender qué es prompt engineering",
            "Conocer su importancia en el uso de IA",
            "Identificar buenos y malos prompts"
        ]),
        "exercise": json.dumps({
            "type": "multiple_choice",
            "instruction": "¿Cuál es el objetivo principal del prompt engineering?",
            "options": [
                "Escribir código más rápido",
                "Comunicarse efectivamente con modelos de IA",
                "Crear imágenes con IA",
                "Entrenar nuevos modelos"
            ],
            "correct_answer": 1
        })
    },
    {
        "slug": "anatomy-of-a-prompt",
        "title": "Anatomía de un Prompt",
        "description": "Descubre los componentes esenciales que forman un prompt efectivo.",
        "icon": "🔬",
        "category": LessonCategory.FUNDAMENTALS,
        "difficulty": DifficultyLevel.BEGINNER,
        "duration_minutes": 15,
        "xp_reward": 60,
        "order": 2,
        "content": json.dumps([
            {"type": "text", "title": "Componentes", "content": "Un prompt efectivo tiene: contexto, instrucción, formato de salida y ejemplos."},
            {"type": "code", "language": "text", "content": "Contexto: Eres un experto en...\nInstrucción: Explica...\nFormato: En 3 puntos:\nEjemplo: Como por ejemplo..."}
        ]),
        "objectives": json.dumps([
            "Identificar los 4 componentes de un prompt",
            "Entender cuándo usar cada componente",
            "Practicar la estructura básica"
        ])
    },
    {
        "slug": "zero-shot-prompting",
        "title": "Zero-Shot Prompting",
        "description": "Aprende a obtener resultados sin proporcionar ejemplos previos.",
        "icon": "0️⃣",
        "category": LessonCategory.TECHNIQUES,
        "difficulty": DifficultyLevel.BEGINNER,
        "duration_minutes": 12,
        "xp_reward": 55,
        "order": 3,
        "content": json.dumps([
            {"type": "text", "title": "¿Qué es Zero-Shot?", "content": "Zero-shot significa pedir una tarea sin dar ejemplos de cómo hacerla."},
            {"type": "text", "title": "Cuándo usarlo", "content": "Ideal para tareas simples y directas donde el modelo ya tiene conocimiento."}
        ]),
        "objectives": json.dumps([
            "Entender zero-shot prompting",
            "Saber cuándo aplicarlo",
            "Comparar con otras técnicas"
        ])
    },
    {
        "slug": "few-shot-prompting",
        "title": "Few-Shot Prompting",
        "description": "Mejora tus resultados proporcionando ejemplos al modelo.",
        "icon": "📝",
        "category": LessonCategory.TECHNIQUES,
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "duration_minutes": 20,
        "xp_reward": 75,
        "order": 4,
        "content": json.dumps([
            {"type": "text", "title": "El poder de los ejemplos", "content": "Few-shot significa dar 2-5 ejemplos antes de tu pregunta real."},
            {"type": "code", "language": "text", "content": "Ejemplo 1: perro -> animal\nEjemplo 2: manzana -> fruta\nEjemplo 3: silla -> ?"}
        ]),
        "objectives": json.dumps([
            "Dominar few-shot prompting",
            "Crear ejemplos efectivos",
            "Optimizar cantidad de ejemplos"
        ])
    },
    {
        "slug": "chain-of-thought",
        "title": "Chain of Thought (CoT)",
        "description": "Guía al modelo a través de razonamiento paso a paso.",
        "icon": "🔗",
        "category": LessonCategory.TECHNIQUES,
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "duration_minutes": 25,
        "xp_reward": 85,
        "order": 5,
        "content": json.dumps([
            {"type": "text", "title": "Pensamiento encadenado", "content": "CoT pide al modelo que muestre su razonamiento paso a paso."},
            {"type": "tip", "content": "Usa frases como 'Piensa paso a paso' o 'Explica tu razonamiento'."}
        ]),
        "objectives": json.dumps([
            "Implementar Chain of Thought",
            "Mejorar respuestas complejas",
            "Detectar errores de razonamiento"
        ])
    },
    {
        "slug": "role-prompting",
        "title": "Role Prompting",
        "description": "Asigna roles específicos al modelo para obtener respuestas especializadas.",
        "icon": "🎭",
        "category": LessonCategory.TECHNIQUES,
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "duration_minutes": 18,
        "xp_reward": 70,
        "order": 6,
        "content": json.dumps([
            {"type": "text", "title": "El poder de los roles", "content": "Asignar un rol cambia el estilo y profundidad de las respuestas."},
            {"type": "code", "language": "text", "content": "Eres un experto senior en Python con 15 años de experiencia..."}
        ]),
        "objectives": json.dumps([
            "Crear roles efectivos",
            "Combinar roles con otras técnicas",
            "Evitar roles contradictorios"
        ])
    },
    {
        "slug": "output-formatting",
        "title": "Formateo de Salida",
        "description": "Controla exactamente cómo el modelo estructura sus respuestas.",
        "icon": "📋",
        "category": LessonCategory.ADVANCED,
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "duration_minutes": 22,
        "xp_reward": 80,
        "order": 7,
        "content": json.dumps([
            {"type": "text", "title": "JSON, Markdown y más", "content": "Puedes pedir respuestas en JSON, tablas, listas, código, etc."},
            {"type": "code", "language": "text", "content": "Responde SOLO en formato JSON con esta estructura:\n{\"nombre\": \"\", \"edad\": 0}"}
        ]),
        "objectives": json.dumps([
            "Dominar formatos de salida",
            "Crear templates reutilizables",
            "Validar respuestas estructuradas"
        ])
    },
    {
        "slug": "prompt-chaining",
        "title": "Encadenamiento de Prompts",
        "description": "Combina múltiples prompts para tareas complejas.",
        "icon": "⛓️",
        "category": LessonCategory.ADVANCED,
        "difficulty": DifficultyLevel.ADVANCED,
        "duration_minutes": 30,
        "xp_reward": 100,
        "order": 8,
        "content": json.dumps([
            {"type": "text", "title": "Divide y vencerás", "content": "Tareas complejas se resuelven mejor en pasos secuenciales."},
            {"type": "text", "title": "Ejemplo", "content": "1. Analiza el problema -> 2. Genera opciones -> 3. Evalúa opciones -> 4. Implementa"}
        ]),
        "objectives": json.dumps([
            "Diseñar cadenas de prompts",
            "Manejar dependencias entre pasos",
            "Optimizar flujos complejos"
        ])
    }
]

# Seed data for puzzles
PUZZLES_DATA = [
    {
        "slug": "prompt-components-basics",
        "title": "Componentes del Prompt",
        "description": "Relaciona cada componente con su función.",
        "icon": "🧩",
        "category": PuzzleCategory.FUNDAMENTALS,
        "difficulty": DifficultyLevel.BEGINNER,
        "xp_reward": 50,
        "time_limit_seconds": 180,
        "order": 1,
        "grid_size": json.dumps({"rows": 4, "cols": 4}),
        "categories": json.dumps([
            {"name": "Componente", "items": ["Contexto", "Instrucción", "Formato", "Ejemplo"]},
            {"name": "Función", "items": ["Define el rol", "Indica la tarea", "Estructura salida", "Muestra patrón"]}
        ]),
        "clues": json.dumps([
            {"id": 1, "text": "El contexto define quién es el asistente", "type": "positive"},
            {"id": 2, "text": "La instrucción NO define la estructura de la respuesta", "type": "negative"},
            {"id": 3, "text": "Los ejemplos muestran el patrón esperado", "type": "positive"}
        ]),
        "solution": json.dumps({
            "Contexto": "Define el rol",
            "Instrucción": "Indica la tarea",
            "Formato": "Estructura salida",
            "Ejemplo": "Muestra patrón"
        })
    },
    {
        "slug": "technique-difficulty-match",
        "title": "Técnicas y Dificultad",
        "description": "Empareja cada técnica con su nivel de dificultad típico.",
        "icon": "📊",
        "category": PuzzleCategory.TECHNIQUES,
        "difficulty": DifficultyLevel.INTERMEDIATE,
        "xp_reward": 75,
        "time_limit_seconds": 240,
        "order": 2,
        "grid_size": json.dumps({"rows": 4, "cols": 4}),
        "categories": json.dumps([
            {"name": "Técnica", "items": ["Zero-shot", "Few-shot", "CoT", "Chaining"]},
            {"name": "Nivel", "items": ["Básico", "Intermedio", "Avanzado", "Experto"]}
        ]),
        "clues": json.dumps([
            {"id": 1, "text": "Zero-shot es la técnica más básica", "type": "positive"},
            {"id": 2, "text": "Chain of Thought no es básico ni experto", "type": "negative"},
            {"id": 3, "text": "Chaining requiere experiencia avanzada", "type": "positive"}
        ]),
        "solution": json.dumps({
            "Zero-shot": "Básico",
            "Few-shot": "Intermedio",
            "CoT": "Avanzado",
            "Chaining": "Experto"
        })
    }
]

# Seed data for badges
BADGES_DATA = [
    # Progress badges
    {
        "slug": "first-lesson",
        "name": "Primera Lección",
        "description": "Completaste tu primera lección",
        "icon": "🌱",
        "category": BadgeCategory.PROGRESS,
        "rarity": BadgeRarity.COMMON,
        "condition": json.dumps({"type": "lessons_completed", "value": 1, "operator": "gte"}),
        "xp_reward": 25,
        "order": 1
    },
    {
        "slug": "lesson-master-5",
        "name": "Estudiante Dedicado",
        "description": "Completaste 5 lecciones",
        "icon": "📚",
        "category": BadgeCategory.PROGRESS,
        "rarity": BadgeRarity.COMMON,
        "condition": json.dumps({"type": "lessons_completed", "value": 5, "operator": "gte"}),
        "xp_reward": 50,
        "order": 2
    },
    {
        "slug": "lesson-master-10",
        "name": "Maestro del Conocimiento",
        "description": "Completaste 10 lecciones",
        "icon": "🎓",
        "category": BadgeCategory.PROGRESS,
        "rarity": BadgeRarity.RARE,
        "condition": json.dumps({"type": "lessons_completed", "value": 10, "operator": "gte"}),
        "xp_reward": 100,
        "order": 3
    },
    # Puzzle badges
    {
        "slug": "first-puzzle",
        "name": "Primer Puzzle",
        "description": "Resolviste tu primer puzzle",
        "icon": "🧩",
        "category": BadgeCategory.PUZZLES,
        "rarity": BadgeRarity.COMMON,
        "condition": json.dumps({"type": "puzzles_completed", "value": 1, "operator": "gte"}),
        "xp_reward": 25,
        "order": 10
    },
    {
        "slug": "puzzle-pro",
        "name": "Puzzle Pro",
        "description": "Resolviste 10 puzzles",
        "icon": "🏆",
        "category": BadgeCategory.PUZZLES,
        "rarity": BadgeRarity.RARE,
        "condition": json.dumps({"type": "puzzles_completed", "value": 10, "operator": "gte"}),
        "xp_reward": 100,
        "order": 11
    },
    {
        "slug": "perfectionist",
        "name": "Perfeccionista",
        "description": "Obtén 3 estrellas en 5 puzzles",
        "icon": "⭐",
        "category": BadgeCategory.PUZZLES,
        "rarity": BadgeRarity.EPIC,
        "condition": json.dumps({"type": "puzzles_3_stars", "value": 5, "operator": "gte"}),
        "xp_reward": 150,
        "order": 12
    },
    # Streak badges
    {
        "slug": "streak-3",
        "name": "Racha de 3 días",
        "description": "Mantén una racha de 3 días",
        "icon": "🔥",
        "category": BadgeCategory.STREAK,
        "rarity": BadgeRarity.COMMON,
        "condition": json.dumps({"type": "current_streak", "value": 3, "operator": "gte"}),
        "xp_reward": 30,
        "order": 20
    },
    {
        "slug": "streak-7",
        "name": "Semana Perfecta",
        "description": "Mantén una racha de 7 días",
        "icon": "🔥",
        "category": BadgeCategory.STREAK,
        "rarity": BadgeRarity.RARE,
        "condition": json.dumps({"type": "current_streak", "value": 7, "operator": "gte"}),
        "xp_reward": 75,
        "order": 21
    },
    {
        "slug": "streak-30",
        "name": "Mes Imparable",
        "description": "Mantén una racha de 30 días",
        "icon": "💪",
        "category": BadgeCategory.STREAK,
        "rarity": BadgeRarity.EPIC,
        "condition": json.dumps({"type": "current_streak", "value": 30, "operator": "gte"}),
        "xp_reward": 200,
        "order": 22
    },
    {
        "slug": "streak-100",
        "name": "Leyenda",
        "description": "Mantén una racha de 100 días",
        "icon": "👑",
        "category": BadgeCategory.STREAK,
        "rarity": BadgeRarity.LEGENDARY,
        "condition": json.dumps({"type": "current_streak", "value": 100, "operator": "gte"}),
        "xp_reward": 500,
        "is_hidden": True,
        "order": 23
    },
    # XP badges
    {
        "slug": "xp-500",
        "name": "Aprendiz",
        "description": "Acumula 500 XP",
        "icon": "✨",
        "category": BadgeCategory.XP,
        "rarity": BadgeRarity.COMMON,
        "condition": json.dumps({"type": "total_xp", "value": 500, "operator": "gte"}),
        "xp_reward": 25,
        "order": 30
    },
    {
        "slug": "xp-2000",
        "name": "Practicante",
        "description": "Acumula 2000 XP",
        "icon": "💫",
        "category": BadgeCategory.XP,
        "rarity": BadgeRarity.RARE,
        "condition": json.dumps({"type": "total_xp", "value": 2000, "operator": "gte"}),
        "xp_reward": 75,
        "order": 31
    },
    {
        "slug": "xp-10000",
        "name": "Experto",
        "description": "Acumula 10000 XP",
        "icon": "🌟",
        "category": BadgeCategory.XP,
        "rarity": BadgeRarity.EPIC,
        "condition": json.dumps({"type": "total_xp", "value": 10000, "operator": "gte"}),
        "xp_reward": 200,
        "order": 32
    },
    # Level badges
    {
        "slug": "level-5",
        "name": "Nivel 5",
        "description": "Alcanza el nivel 5",
        "icon": "5️⃣",
        "category": BadgeCategory.LEVELS,
        "rarity": BadgeRarity.COMMON,
        "condition": json.dumps({"type": "level", "value": 5, "operator": "gte"}),
        "xp_reward": 50,
        "order": 40
    },
    {
        "slug": "level-10",
        "name": "Nivel 10",
        "description": "Alcanza el nivel 10",
        "icon": "🔟",
        "category": BadgeCategory.LEVELS,
        "rarity": BadgeRarity.RARE,
        "condition": json.dumps({"type": "level", "value": 10, "operator": "gte"}),
        "xp_reward": 100,
        "order": 41
    }
]


async def seed_lessons():
    """Seed lessons data."""
    async with async_session_factory() as session:
        for lesson_data in LESSONS_DATA:
            # Check if lesson already exists
            result = await session.execute(
                select(Lesson).where(Lesson.slug == lesson_data["slug"])
            )
            existing = result.scalar_one_or_none()

            if not existing:
                lesson = Lesson(
                    **lesson_data,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(lesson)
                print(f"  ✅ Created lesson: {lesson_data['title']}")
            else:
                print(f"  ⏭️  Lesson already exists: {lesson_data['title']}")

        await session.commit()


async def seed_puzzles():
    """Seed puzzles data."""
    async with async_session_factory() as session:
        for puzzle_data in PUZZLES_DATA:
            result = await session.execute(
                select(Puzzle).where(Puzzle.slug == puzzle_data["slug"])
            )
            existing = result.scalar_one_or_none()

            if not existing:
                puzzle = Puzzle(
                    **puzzle_data,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(puzzle)
                print(f"  ✅ Created puzzle: {puzzle_data['title']}")
            else:
                print(f"  ⏭️  Puzzle already exists: {puzzle_data['title']}")

        await session.commit()


async def seed_badges():
    """Seed badges data."""
    async with async_session_factory() as session:
        for badge_data in BADGES_DATA:
            result = await session.execute(
                select(Badge).where(Badge.slug == badge_data["slug"])
            )
            existing = result.scalar_one_or_none()

            if not existing:
                badge = Badge(**badge_data)
                session.add(badge)
                print(f"  ✅ Created badge: {badge_data['name']}")
            else:
                print(f"  ⏭️  Badge already exists: {badge_data['name']}")

        await session.commit()


async def seed_daily_challenge():
    """Seed today's daily challenge."""
    async with async_session_factory() as session:
        today = date.today()

        result = await session.execute(
            select(DailyChallenge).where(DailyChallenge.challenge_date == today)
        )
        existing = result.scalar_one_or_none()

        if not existing:
            challenge = DailyChallenge(
                challenge_date=today,
                challenge_type="xp",
                target_count=100,
                xp_reward=50,
                title="Objetivo Diario",
                description="Gana 100 XP hoy completando lecciones o puzzles"
            )
            session.add(challenge)
            print(f"  ✅ Created daily challenge for {today}")
        else:
            print(f"  ⏭️  Daily challenge already exists for {today}")

        await session.commit()


async def run_seed():
    """Run all seed functions."""
    print("🌱 Seeding PromptCraft database...\n")

    print("📚 Seeding lessons...")
    await seed_lessons()

    print("\n🧩 Seeding puzzles...")
    await seed_puzzles()

    print("\n🏅 Seeding badges...")
    await seed_badges()

    print("\n📅 Seeding daily challenge...")
    await seed_daily_challenge()

    print("\n🎉 Seed complete!")


if __name__ == "__main__":
    asyncio.run(run_seed())
