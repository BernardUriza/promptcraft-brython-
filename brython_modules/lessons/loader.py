# PromptCraft - Lesson Loader
# Cargador de lecciones

from .content import EMBEDDED_LESSONS, LESSON_CATEGORIES, get_lessons_by_category_data


class LessonLoader:
    """Gestiona la carga y acceso a lecciones."""

    def __init__(self):
        self.lessons = EMBEDDED_LESSONS
        self.categories = LESSON_CATEGORIES

    def get_lesson(self, lesson_id):
        """
        Obtiene una lección por su ID.

        Args:
            lesson_id: ID de la lección

        Returns:
            dict con datos de la lección o None
        """
        return self.lessons.get(lesson_id)

    def get_all_lessons(self):
        """
        Obtiene todas las lecciones.

        Returns:
            Lista de todas las lecciones
        """
        return list(self.lessons.values())

    def get_lessons_by_category(self, category_id):
        """
        Obtiene lecciones de una categoría.

        Args:
            category_id: ID de la categoría

        Returns:
            Lista de lecciones de esa categoría
        """
        return get_lessons_by_category_data(category_id)

    def get_categories(self):
        """
        Obtiene todas las categorías.

        Returns:
            Lista de categorías ordenadas
        """
        return sorted(self.categories, key=lambda c: c.get('order', 0))

    def get_category(self, category_id):
        """
        Obtiene una categoría por ID.

        Args:
            category_id: ID de la categoría

        Returns:
            dict con datos de la categoría o None
        """
        for cat in self.categories:
            if cat['id'] == category_id:
                return cat
        return None

    def get_next_lesson(self, current_lesson_id):
        """
        Obtiene la siguiente lección en la secuencia.

        Args:
            current_lesson_id: ID de la lección actual

        Returns:
            dict de la siguiente lección o None
        """
        current = self.get_lesson(current_lesson_id)
        if current and current.get('next_lesson'):
            return self.get_lesson(current['next_lesson'])
        return None

    def get_previous_lesson(self, current_lesson_id):
        """
        Obtiene la lección anterior en la secuencia.

        Args:
            current_lesson_id: ID de la lección actual

        Returns:
            dict de la lección anterior o None
        """
        for lesson in self.lessons.values():
            if lesson.get('next_lesson') == current_lesson_id:
                return lesson
        return None

    def search_lessons(self, query):
        """
        Busca lecciones por texto.

        Args:
            query: Texto a buscar

        Returns:
            Lista de lecciones que coinciden
        """
        query = query.lower()
        results = []

        for lesson in self.lessons.values():
            # Buscar en título, descripción y objetivos
            searchable = ' '.join([
                lesson.get('title', ''),
                lesson.get('description', ''),
                ' '.join(lesson.get('objectives', []))
            ]).lower()

            if query in searchable:
                results.append(lesson)

        return results

    def get_lessons_by_difficulty(self, difficulty):
        """
        Obtiene lecciones por dificultad.

        Args:
            difficulty: 'beginner', 'intermediate', 'advanced'

        Returns:
            Lista de lecciones con esa dificultad
        """
        return [
            lesson for lesson in self.lessons.values()
            if lesson.get('difficulty') == difficulty
        ]

    def get_total_xp_available(self):
        """
        Calcula el XP total disponible en todas las lecciones.

        Returns:
            int con XP total
        """
        return sum(
            lesson.get('xp_reward', 0)
            for lesson in self.lessons.values()
        )

    def get_total_duration(self):
        """
        Calcula la duración total de todas las lecciones.

        Returns:
            int con minutos totales
        """
        return sum(
            lesson.get('duration', 0)
            for lesson in self.lessons.values()
        )

    def get_lesson_count(self):
        """
        Obtiene el número total de lecciones.

        Returns:
            int con cantidad de lecciones
        """
        return len(self.lessons)

    def get_category_stats(self, category_id):
        """
        Obtiene estadísticas de una categoría.

        Args:
            category_id: ID de la categoría

        Returns:
            dict con estadísticas
        """
        lessons = self.get_lessons_by_category(category_id)

        return {
            'count': len(lessons),
            'total_xp': sum(l.get('xp_reward', 0) for l in lessons),
            'total_duration': sum(l.get('duration', 0) for l in lessons),
            'difficulties': {
                'beginner': len([l for l in lessons if l.get('difficulty') == 'beginner']),
                'intermediate': len([l for l in lessons if l.get('difficulty') == 'intermediate']),
                'advanced': len([l for l in lessons if l.get('difficulty') == 'advanced'])
            }
        }


# Instancia global del loader
_loader = None


def get_loader():
    """Obtiene la instancia global del loader."""
    global _loader
    if _loader is None:
        _loader = LessonLoader()
    return _loader


def get_lesson(lesson_id):
    """Atajo para obtener una lección."""
    return get_loader().get_lesson(lesson_id)


def get_lessons_by_category(category_id):
    """Atajo para obtener lecciones por categoría."""
    return get_loader().get_lessons_by_category(category_id)


def get_all_lessons():
    """Atajo para obtener todas las lecciones."""
    return get_loader().get_all_lessons()


def get_categories():
    """Atajo para obtener categorías."""
    return get_loader().get_categories()


# Alias para compatibilidad
LESSONS_DATA = EMBEDDED_LESSONS
