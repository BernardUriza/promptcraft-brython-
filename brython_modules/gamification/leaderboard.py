# PromptCraft - Leaderboard
# Sistema de tabla de clasificación (local/demo)

from browser import local_storage, window
import json


class Leaderboard:
    """
    Sistema de leaderboard local.
    En una aplicación real, esto se conectaría a un backend.
    """

    STORAGE_KEY = 'promptcraft_leaderboard'
    MAX_ENTRIES = 100

    def __init__(self, state=None):
        self.state = state
        self._cache = None

    def _load(self):
        """Carga el leaderboard del storage."""
        if self._cache is not None:
            return self._cache

        try:
            data = local_storage.getItem(self.STORAGE_KEY)
            if data:
                self._cache = json.loads(data)
            else:
                self._cache = {'entries': [], 'last_updated': None}
        except:
            self._cache = {'entries': [], 'last_updated': None}

        return self._cache

    def _save(self):
        """Guarda el leaderboard en storage."""
        if self._cache:
            self._cache['last_updated'] = str(window.Date.new())
            local_storage.setItem(self.STORAGE_KEY, json.dumps(self._cache))

    def add_entry(self, username, xp, level, badges_count):
        """
        Añade o actualiza una entrada en el leaderboard.

        Args:
            username: Nombre de usuario
            xp: XP total
            level: Nivel actual
            badges_count: Número de badges
        """
        data = self._load()

        # Buscar entrada existente
        existing_idx = None
        for i, entry in enumerate(data['entries']):
            if entry['username'] == username:
                existing_idx = i
                break

        new_entry = {
            'username': username,
            'xp': xp,
            'level': level,
            'badges': badges_count,
            'updated': str(window.Date.new()),
        }

        if existing_idx is not None:
            data['entries'][existing_idx] = new_entry
        else:
            data['entries'].append(new_entry)

        # Ordenar por XP descendente
        data['entries'].sort(key=lambda x: x['xp'], reverse=True)

        # Limitar entradas
        if len(data['entries']) > self.MAX_ENTRIES:
            data['entries'] = data['entries'][:self.MAX_ENTRIES]

        self._cache = data
        self._save()

    def get_top(self, limit=10):
        """
        Obtiene los top jugadores.

        Args:
            limit: Número de entradas a retornar

        Returns:
            Lista de entradas con rank
        """
        data = self._load()
        entries = data['entries'][:limit]

        # Añadir rank
        for i, entry in enumerate(entries):
            entry['rank'] = i + 1

        return entries

    def get_rank(self, username):
        """
        Obtiene el rank de un usuario.

        Args:
            username: Nombre de usuario

        Returns:
            Rank (1-based) o None si no está
        """
        data = self._load()

        for i, entry in enumerate(data['entries']):
            if entry['username'] == username:
                return i + 1

        return None

    def get_nearby(self, username, count=5):
        """
        Obtiene entradas cercanas a un usuario.

        Args:
            username: Nombre de usuario
            count: Número de entradas arriba y abajo

        Returns:
            Lista de entradas con rank
        """
        data = self._load()
        entries = data['entries']

        # Encontrar posición del usuario
        user_idx = None
        for i, entry in enumerate(entries):
            if entry['username'] == username:
                user_idx = i
                break

        if user_idx is None:
            return []

        # Obtener entradas cercanas
        start = max(0, user_idx - count)
        end = min(len(entries), user_idx + count + 1)

        nearby = []
        for i in range(start, end):
            entry = dict(entries[i])
            entry['rank'] = i + 1
            entry['is_user'] = (i == user_idx)
            nearby.append(entry)

        return nearby

    def get_stats(self):
        """
        Obtiene estadísticas del leaderboard.

        Returns:
            Dict con estadísticas
        """
        data = self._load()
        entries = data['entries']

        if not entries:
            return {
                'total_players': 0,
                'avg_xp': 0,
                'max_xp': 0,
                'avg_level': 0,
            }

        total_xp = sum(e['xp'] for e in entries)
        total_level = sum(e['level'] for e in entries)

        return {
            'total_players': len(entries),
            'avg_xp': total_xp // len(entries),
            'max_xp': entries[0]['xp'] if entries else 0,
            'avg_level': total_level // len(entries),
        }

    def clear(self):
        """Limpia el leaderboard."""
        self._cache = {'entries': [], 'last_updated': None}
        self._save()

    def sync_current_user(self):
        """
        Sincroniza el usuario actual con el leaderboard.
        """
        if not self.state:
            return

        username = self.state.data.get('username', 'Anónimo')
        xp = self.state.data.get('xp', 0)
        level = self.state.get_level_info()['level']
        badges = len(self.state.data.get('badges', []))

        self.add_entry(username, xp, level, badges)

    @staticmethod
    def generate_demo_data():
        """
        Genera datos de demostración para el leaderboard.

        Returns:
            Lista de entradas demo
        """
        import random

        names = [
            'PromptMaster', 'AIExplorer', 'CodeWizard', 'TechNinja',
            'DataDragon', 'LogicLord', 'SmartCookie', 'BrainStorm',
            'QuickMind', 'DeepThinker', 'PromptPro', 'AIAce',
            'CleverBot', 'WiseSage', 'TechTitan'
        ]

        entries = []
        for i, name in enumerate(names):
            xp = random.randint(100, 15000)
            level = min(10, xp // 1000 + 1)
            badges = random.randint(1, 25)

            entries.append({
                'username': name,
                'xp': xp,
                'level': level,
                'badges': badges,
                'is_demo': True,
            })

        # Ordenar por XP
        entries.sort(key=lambda x: x['xp'], reverse=True)

        return entries
