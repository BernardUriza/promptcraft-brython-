# PromptCraft - Plan de Arquitectura Completa
## Plataforma de Aprendizaje Gamificada Estilo Duolingo

---

## Resumen Ejecutivo

Este plan detalla la transformacion de PromptCraft de un prototipo frontend estatico a una **plataforma multiusuario completa** con backend, base de datos, autenticacion, y sistema de gamificacion en tiempo real, similar al modelo de Duolingo.

**Comando para arrancar:** `make dev-all`

---

## Investigacion Realizada (10 Busquedas)

### Fuentes Consultadas:

1. **Arquitectura Duolingo** - [Duolingo Tech Stack](https://stackshare.io/duolingo/duolingo), [Scala Rewrite](https://blog.duolingo.com/rewriting-duolingos-engine-in-scala/)
2. **Gamificacion Best Practices** - [Smartico Architecture](https://www.smartico.ai/blog-post/gamification-architecture-best-practices)
3. **FastAPI JWT Auth** - [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [TestDriven.io JWT](https://testdriven.io/blog/fastapi-jwt-auth/)
4. **PostgreSQL Gamification Schema** - [Gamification Framework](https://github.com/rwth-acis/Gamification-Framework), [Badge System Design](https://www.namitjain.com/blog/backend-driven-badge-system-part-1)
5. **Docker Compose Production** - [KhueApps Guide](https://www.khueapps.com/blog/article/setup-docker-compose-for-fastapi-postgres-redis-and-nginx-caddy)
6. **React TypeScript Frontend** - [Conf42 React Gamification](https://www.conf42.com/JavaScript_2024_Courtney_Yatteau_15_react_gamification_frontend)
7. **SQLAlchemy 2.0 Async** - [Leapcell Guide](https://leapcell.io/blog/building-high-performance-async-apis-with-fastapi-sqlalchemy-2-0-and-asyncpg)
8. **Alembic Migrations** - [FastAPI Boilerplate](https://benavlabs.github.io/FastAPI-boilerplate/user-guide/database/migrations/)
9. **Redis Leaderboards** - [Redis Solutions](https://redis.io/solutions/leaderboards/), [HackerNoon Redis Gamification](https://hackernoon.com/redis-gamification-60e49b5494ae)
10. **WebSocket Real-time** - [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/), [Postgres LISTEN/NOTIFY](https://hexshift.medium.com/real-time-notifications-with-fastapi-websockets-and-postgres-listen-notify-f26dbb9fe3e2)

---

## Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────┐
│                         LOAD BALANCER (Nginx)                        │
│                              Port 80/443                             │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│   Frontend (React)  │  │  API Gateway        │  │  WebSocket Server   │
│   Port 3000         │  │  FastAPI :8000      │  │  FastAPI :8001      │
│   - TypeScript      │  │  - REST API         │  │  - Real-time        │
│   - Tailwind CSS    │  │  - JWT Auth         │  │  - Notifications    │
│   - Zustand         │  │  - Rate Limiting    │  │  - Live Leaderboard │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
                                    │                       │
                    ┌───────────────┴───────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SERVICE LAYER                                │
├─────────────────────┬─────────────────────┬─────────────────────────┤
│   Auth Service      │   Gamification      │   Content Service       │
│   - Register/Login  │   - XP Calculator   │   - Lessons CRUD        │
│   - OAuth2 (future) │   - Level System    │   - Puzzles Engine      │
│   - Password Reset  │   - Badge Awards    │   - Progress Tracking   │
│   - Session Mgmt    │   - Streak Manager  │   - Exercise Validator  │
└─────────────────────┴─────────────────────┴─────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│   PostgreSQL        │  │   Redis             │  │   Celery Worker     │
│   Port 5432         │  │   Port 6379         │  │   Background Tasks  │
│   - Users           │  │   - Session Cache   │  │   - Email sending   │
│   - Progress        │  │   - Leaderboards    │  │   - XP calculations │
│   - Achievements    │  │   - Rate Limiting   │  │   - Badge checks    │
│   - Content         │  │   - Real-time data  │  │   - Daily rewards   │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

---

## Stack Tecnologico

### Backend
| Componente | Tecnologia | Justificacion |
|------------|------------|---------------|
| Framework | FastAPI 0.115+ | Async nativo, OpenAPI, type hints |
| ORM | SQLAlchemy 2.0 + asyncpg | Async PostgreSQL, mejor performance |
| Auth | python-jose + passlib | JWT tokens, Argon2 hashing |
| Migrations | Alembic | Version control de schema |
| Task Queue | Celery + Redis | Background jobs |
| Cache | Redis | Leaderboards O(log N), sessions |
| Server | Uvicorn + Gunicorn | Production ASGI |

### Frontend
| Componente | Tecnologia | Justificacion |
|------------|------------|---------------|
| Framework | React 18 + TypeScript | Componentes, type safety |
| Styling | Tailwind CSS 3.4 | Utility-first, como Duolingo |
| State | Zustand | Ligero, simple, performante |
| Routing | React Router 6 | SPA navigation |
| HTTP | Axios + React Query | Caching, mutations |
| WebSocket | socket.io-client | Real-time updates |
| Build | Vite | Fast HMR, ESBuild |

### Infrastructure
| Componente | Tecnologia | Justificacion |
|------------|------------|---------------|
| Containers | Docker + Docker Compose | Reproducible environments |
| Reverse Proxy | Nginx | SSL, load balancing |
| Database | PostgreSQL 15 | ACID, JSON support |
| Cache/Queue | Redis 7 | In-memory, sorted sets |
| CI/CD | GitHub Actions | Automated testing/deploy |

---

## Estructura del Proyecto

```
promptcraft/
├── docker-compose.yml           # Orquestacion de servicios
├── docker-compose.dev.yml       # Override para desarrollo
├── docker-compose.prod.yml      # Override para produccion
├── Makefile                     # Comandos de desarrollo
├── .env.example                 # Variables de entorno template
├── README.md
│
├── backend/                     # FastAPI Backend
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── pyproject.toml           # Poetry dependencies
│   ├── poetry.lock
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry
│   │   ├── config.py            # Settings with Pydantic
│   │   ├── dependencies.py      # Dependency injection
│   │   │
│   │   ├── api/                 # API Routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py    # API v1 router
│   │   │   │   ├── auth.py      # Auth endpoints
│   │   │   │   ├── users.py     # User endpoints
│   │   │   │   ├── lessons.py   # Lessons endpoints
│   │   │   │   ├── puzzles.py   # Puzzles endpoints
│   │   │   │   ├── gamification.py  # XP, badges, etc
│   │   │   │   ├── leaderboard.py   # Rankings
│   │   │   │   └── progress.py      # User progress
│   │   │   └── websocket.py     # WebSocket handlers
│   │   │
│   │   ├── core/                # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── security.py      # JWT, password hashing
│   │   │   ├── exceptions.py    # Custom exceptions
│   │   │   └── middleware.py    # Rate limiting, CORS
│   │   │
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base model class
│   │   │   ├── user.py          # User model
│   │   │   ├── lesson.py        # Lesson model
│   │   │   ├── puzzle.py        # Puzzle model
│   │   │   ├── progress.py      # Progress tracking
│   │   │   ├── achievement.py   # Badges, achievements
│   │   │   └── gamification.py  # XP, levels, streaks
│   │   │
│   │   ├── schemas/             # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── lesson.py
│   │   │   ├── puzzle.py
│   │   │   ├── gamification.py
│   │   │   └── responses.py     # Standard responses
│   │   │
│   │   ├── services/            # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Auth service
│   │   │   ├── user.py          # User service
│   │   │   ├── lesson.py        # Lesson service
│   │   │   ├── puzzle.py        # Puzzle engine
│   │   │   ├── xp.py            # XP calculator
│   │   │   ├── level.py         # Level system
│   │   │   ├── badge.py         # Badge awards
│   │   │   ├── streak.py        # Streak manager
│   │   │   ├── leaderboard.py   # Redis leaderboard
│   │   │   └── notification.py  # Real-time notifications
│   │   │
│   │   ├── repositories/        # Data access layer
│   │   │   ├── __init__.py
│   │   │   ├── base.py          # Base repository
│   │   │   ├── user.py
│   │   │   ├── lesson.py
│   │   │   ├── puzzle.py
│   │   │   └── progress.py
│   │   │
│   │   ├── db/                  # Database config
│   │   │   ├── __init__.py
│   │   │   ├── session.py       # Async session
│   │   │   └── redis.py         # Redis connection
│   │   │
│   │   └── tasks/               # Celery tasks
│   │       ├── __init__.py
│   │       ├── celery_app.py
│   │       ├── email.py
│   │       ├── daily_rewards.py
│   │       └── badge_check.py
│   │
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_lessons.py
│       ├── test_puzzles.py
│       └── test_gamification.py
│
├── frontend/                    # React Frontend
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── index.html
│   │
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── vite-env.d.ts
│   │   │
│   │   ├── api/                 # API client
│   │   │   ├── client.ts        # Axios instance
│   │   │   ├── auth.ts
│   │   │   ├── lessons.ts
│   │   │   ├── puzzles.ts
│   │   │   └── gamification.ts
│   │   │
│   │   ├── components/          # React components
│   │   │   ├── common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Toast.tsx
│   │   │   │   └── Loading.tsx
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── lessons/
│   │   │   │   ├── LessonCard.tsx
│   │   │   │   ├── LessonContent.tsx
│   │   │   │   └── LessonExercise.tsx
│   │   │   ├── puzzles/
│   │   │   │   ├── LogicGrid.tsx
│   │   │   │   ├── PuzzleTimer.tsx
│   │   │   │   └── ClueList.tsx
│   │   │   └── gamification/
│   │   │       ├── XPBar.tsx
│   │   │       ├── LevelBadge.tsx
│   │   │       ├── StreakFlame.tsx
│   │   │       ├── BadgeDisplay.tsx
│   │   │       └── Leaderboard.tsx
│   │   │
│   │   ├── pages/               # Page components
│   │   │   ├── Home.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Lessons.tsx
│   │   │   ├── LessonDetail.tsx
│   │   │   ├── Puzzles.tsx
│   │   │   ├── PuzzlePlay.tsx
│   │   │   ├── Profile.tsx
│   │   │   ├── Badges.tsx
│   │   │   ├── Leaderboard.tsx
│   │   │   └── Settings.tsx
│   │   │
│   │   ├── hooks/               # Custom hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useXP.ts
│   │   │   └── useLeaderboard.ts
│   │   │
│   │   ├── store/               # Zustand stores
│   │   │   ├── authStore.ts
│   │   │   ├── userStore.ts
│   │   │   ├── lessonStore.ts
│   │   │   └── gamificationStore.ts
│   │   │
│   │   ├── types/               # TypeScript types
│   │   │   ├── user.ts
│   │   │   ├── lesson.ts
│   │   │   ├── puzzle.ts
│   │   │   └── gamification.ts
│   │   │
│   │   └── utils/               # Utilities
│   │       ├── constants.ts
│   │       ├── helpers.ts
│   │       └── validators.ts
│   │
│   └── tests/
│       └── components/
│
├── nginx/                       # Nginx config
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
│
├── scripts/                     # Utility scripts
│   ├── init-db.sh
│   ├── seed-data.py
│   └── backup-db.sh
│
└── docs/                        # Documentation
    ├── API.md
    ├── DEPLOYMENT.md
    └── CONTRIBUTING.md
```

---

## Schema de Base de Datos (PostgreSQL)

### Diagrama ER

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     users       │       │  user_progress  │       │    lessons      │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │───┐   │ id (PK)         │   ┌───│ id (PK)         │
│ email           │   │   │ user_id (FK)    │───┤   │ title           │
│ username        │   └──▶│ lesson_id (FK)  │───┘   │ category        │
│ password_hash   │       │ status          │       │ difficulty      │
│ avatar_url      │       │ completed_at    │       │ xp_reward       │
│ created_at      │       │ score           │       │ content (JSON)  │
│ last_active     │       └─────────────────┘       │ order           │
│ is_active       │                                 └─────────────────┘
│ is_verified     │       ┌─────────────────┐
└─────────────────┘       │  puzzle_attempts │       ┌─────────────────┐
         │                ├─────────────────┤       │    puzzles      │
         │                │ id (PK)         │       ├─────────────────┤
         │                │ user_id (FK)    │───┐   │ id (PK)         │
         │                │ puzzle_id (FK)  │───┼───│ title           │
         │                │ started_at      │   │   │ difficulty      │
         │                │ completed_at    │   │   │ category        │
         │                │ time_taken      │   │   │ xp_reward       │
         │                │ stars           │   │   │ grid_data (JSON)│
         │                │ hints_used      │   │   │ clues (JSON)    │
         │                └─────────────────┘   │   │ solution (JSON) │
         │                                      │   └─────────────────┘
         │                                      │
         ▼                                      │
┌─────────────────┐       ┌─────────────────┐   │
│  user_gamification│     │   user_badges   │   │
├─────────────────┤       ├─────────────────┤   │
│ user_id (PK,FK) │───────│ id (PK)         │   │
│ total_xp        │       │ user_id (FK)    │◀──┘
│ level           │       │ badge_id (FK)   │───────┐
│ current_streak  │       │ earned_at       │       │
│ longest_streak  │       │ notified        │       │
│ last_activity   │       └─────────────────┘       │
│ streak_freezes  │                                 │
└─────────────────┘       ┌─────────────────┐       │
                          │     badges      │       │
┌─────────────────┐       ├─────────────────┤       │
│   xp_transactions│      │ id (PK)         │◀──────┘
├─────────────────┤       │ name            │
│ id (PK)         │       │ description     │
│ user_id (FK)    │       │ icon            │
│ amount          │       │ rarity          │
│ source          │       │ category        │
│ source_id       │       │ condition (JSON)│
│ multiplier      │       └─────────────────┘
│ created_at      │
└─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│  daily_challenges│      │   user_settings │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ user_id (PK,FK) │
│ date            │       │ theme           │
│ challenge_type  │       │ notifications   │
│ target          │       │ daily_goal      │
│ xp_reward       │       │ language        │
└─────────────────┘       │ timezone        │
                          └─────────────────┘
```

### Migraciones Alembic (Orden)

1. `001_initial_users.py` - Tabla users
2. `002_lessons_puzzles.py` - Content tables
3. `003_gamification.py` - XP, levels, streaks
4. `004_badges_achievements.py` - Badges system
5. `005_progress_tracking.py` - User progress
6. `006_daily_challenges.py` - Daily/weekly challenges
7. `007_indexes_performance.py` - Indexes for performance

---

## API Endpoints (REST)

### Authentication
```
POST   /api/v1/auth/register     - Registrar usuario
POST   /api/v1/auth/login        - Login (retorna JWT)
POST   /api/v1/auth/refresh      - Refresh token
POST   /api/v1/auth/logout       - Logout (invalidar token)
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password
GET    /api/v1/auth/verify-email/{token}
```

### Users
```
GET    /api/v1/users/me          - Perfil actual
PUT    /api/v1/users/me          - Actualizar perfil
GET    /api/v1/users/{id}        - Perfil publico
GET    /api/v1/users/{id}/stats  - Estadisticas publicas
PUT    /api/v1/users/me/settings - Configuracion
DELETE /api/v1/users/me          - Eliminar cuenta
```

### Lessons
```
GET    /api/v1/lessons           - Listar lecciones
GET    /api/v1/lessons/{id}      - Detalle de leccion
POST   /api/v1/lessons/{id}/start    - Iniciar leccion
POST   /api/v1/lessons/{id}/complete - Completar leccion
POST   /api/v1/lessons/{id}/exercise - Enviar ejercicio
GET    /api/v1/lessons/categories    - Categorias
GET    /api/v1/lessons/recommended   - Recomendadas
```

### Puzzles
```
GET    /api/v1/puzzles           - Listar puzzles
GET    /api/v1/puzzles/{id}      - Detalle de puzzle
POST   /api/v1/puzzles/{id}/start    - Iniciar puzzle
POST   /api/v1/puzzles/{id}/submit   - Enviar solucion
POST   /api/v1/puzzles/{id}/hint     - Pedir pista
GET    /api/v1/puzzles/daily         - Puzzle del dia
```

### Gamification
```
GET    /api/v1/gamification/stats    - Stats del usuario
GET    /api/v1/gamification/xp-history
GET    /api/v1/gamification/level-info
GET    /api/v1/gamification/streak
POST   /api/v1/gamification/streak/freeze - Usar freeze
```

### Badges
```
GET    /api/v1/badges            - Todos los badges
GET    /api/v1/badges/my         - Mis badges
GET    /api/v1/badges/{id}       - Detalle de badge
GET    /api/v1/badges/progress   - Progreso hacia badges
```

### Leaderboard
```
GET    /api/v1/leaderboard/daily     - Top diario
GET    /api/v1/leaderboard/weekly    - Top semanal
GET    /api/v1/leaderboard/alltime   - Top historico
GET    /api/v1/leaderboard/friends   - Entre amigos
GET    /api/v1/leaderboard/my-rank   - Mi posicion
```

### WebSocket Events
```
WS     /ws/notifications    - Notificaciones en tiempo real
       - xp_earned          - XP ganado
       - level_up           - Subida de nivel
       - badge_unlocked     - Badge desbloqueado
       - streak_update      - Actualizacion de racha
       - daily_reminder     - Recordatorio diario
       - leaderboard_update - Cambio en ranking
```

---

## Flujos de Gamificacion

### Sistema de XP

```python
XP_REWARDS = {
    'lesson_complete': 50,
    'lesson_first_time': 25,  # Bonus primera vez
    'exercise_correct': 10,
    'puzzle_complete': {
        'easy': 30,
        'medium': 50,
        'hard': 75
    },
    'puzzle_3_stars': 25,  # Bonus
    'puzzle_speed_bonus': 15,  # < 2 min
    'daily_goal': 20,
    'streak_bonus': lambda days: min(days * 2, 50),
    'weekly_challenge': 100,
}

MULTIPLIERS = {
    'streak_3': 1.1,   # 10% bonus
    'streak_7': 1.25,  # 25% bonus
    'streak_30': 1.5,  # 50% bonus
    'weekend': 1.2,    # 20% bonus fin de semana
    'perfect_day': 1.3 # 30% si todo perfecto
}
```

### Sistema de Niveles

```python
LEVEL_THRESHOLDS = [
    (1, 0, "Novato", "🌱"),
    (2, 100, "Aprendiz", "📖"),
    (3, 350, "Estudiante", "✏️"),
    (4, 850, "Practicante", "🎯"),
    (5, 1600, "Competente", "⭐"),
    (6, 2600, "Habil", "💪"),
    (7, 4100, "Experto", "🏅"),
    (8, 6100, "Maestro", "🎓"),
    (9, 9100, "Gran Maestro", "👑"),
    (10, 14100, "Leyenda", "🏆"),
]
```

### Sistema de Badges (30+)

```python
BADGE_CATEGORIES = {
    'progress': [
        'first_lesson', 'lessons_5', 'lessons_10', 'all_fundamentals',
        'all_techniques', 'all_advanced', 'course_complete'
    ],
    'puzzles': [
        'first_puzzle', 'puzzles_5', 'puzzles_10', 'puzzles_25',
        'first_3_stars', 'all_3_stars', 'speed_demon', 'no_hints'
    ],
    'streak': [
        'streak_3', 'streak_7', 'streak_14', 'streak_30', 'streak_100',
        'weekend_warrior', 'early_bird', 'night_owl'
    ],
    'xp': [
        'xp_100', 'xp_500', 'xp_1000', 'xp_5000', 'xp_10000'
    ],
    'levels': [
        'level_5', 'level_10', 'max_level'
    ],
    'special': [
        'beta_tester', 'first_week', 'comeback_kid', 'perfectionist',
        'social_butterfly', 'helpful_reviewer'
    ]
}
```

### Sistema de Streaks

```python
STREAK_CONFIG = {
    'activity_required': ['lesson_complete', 'puzzle_complete'],
    'reset_hour': 4,  # 4 AM local time
    'freeze_cost': 200,  # XP para comprar freeze
    'max_freezes': 3,
    'streak_milestones': [3, 7, 14, 30, 60, 100, 365],
}
```

---

## Redis Data Structures

### Leaderboards (Sorted Sets)
```redis
# Daily leaderboard
ZADD leaderboard:daily:2024-01-15 {score} {user_id}
ZREVRANK leaderboard:daily:2024-01-15 {user_id}
ZREVRANGE leaderboard:daily:2024-01-15 0 9 WITHSCORES

# Weekly leaderboard
ZADD leaderboard:weekly:2024-W03 {score} {user_id}

# All-time leaderboard
ZADD leaderboard:alltime {score} {user_id}
```

### Session Cache
```redis
# User session
SET session:{user_id} {session_data} EX 86400

# Rate limiting
INCR ratelimit:{user_id}:{endpoint} EX 60
```

### Real-time Data
```redis
# Online users
SADD online_users {user_id}
SREM online_users {user_id}

# Recent activities (for feed)
LPUSH activities:recent {activity_json}
LTRIM activities:recent 0 99
```

---

## Docker Compose Configuration

### docker-compose.yml (Base)
```yaml
version: '3.9'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      REDIS_URL: redis://redis:6379
      SECRET_KEY: ${SECRET_KEY}
      ENVIRONMENT: ${ENVIRONMENT}

  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.tasks.celery_app worker -l info
    depends_on:
      - backend
      - redis

  celery-beat:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.tasks.celery_app beat -l info
    depends_on:
      - celery

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - backend
      - frontend

volumes:
  postgres_data:
  redis_data:
```

### docker-compose.dev.yml (Override)
```yaml
version: '3.9'

services:
  backend:
    build:
      dockerfile: Dockerfile.dev
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"

  frontend:
    build:
      dockerfile: Dockerfile.dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev
    ports:
      - "3000:3000"

  db:
    ports:
      - "5432:5432"

  redis:
    ports:
      - "6379:6379"
```

---

## Makefile

```makefile
.PHONY: help dev-all dev-backend dev-frontend build test lint migrate seed clean

# Colors
GREEN  := \033[0;32m
YELLOW := \033[0;33m
NC     := \033[0m

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================
# DEVELOPMENT
# ============================================

dev-all: ## Start all services for development
	@echo "$(GREEN)Starting PromptCraft development environment...$(NC)"
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

dev-backend: ## Start only backend services
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build db redis backend celery

dev-frontend: ## Start only frontend
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build frontend

dev-db: ## Start only database
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build db redis

logs: ## Show logs
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

# ============================================
# BUILD & PRODUCTION
# ============================================

build: ## Build all containers
	docker-compose build

build-prod: ## Build for production
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

up-prod: ## Start production environment
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

down: ## Stop all containers
	docker-compose down

down-volumes: ## Stop and remove volumes
	docker-compose down -v

# ============================================
# DATABASE
# ============================================

migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

migrate-create: ## Create new migration (usage: make migrate-create MSG="description")
	docker-compose exec backend alembic revision --autogenerate -m "$(MSG)"

migrate-rollback: ## Rollback last migration
	docker-compose exec backend alembic downgrade -1

migrate-history: ## Show migration history
	docker-compose exec backend alembic history

seed: ## Seed database with sample data
	docker-compose exec backend python scripts/seed_data.py

db-shell: ## Open PostgreSQL shell
	docker-compose exec db psql -U $${DB_USER} -d $${DB_NAME}

db-backup: ## Backup database
	docker-compose exec db pg_dump -U $${DB_USER} $${DB_NAME} > backups/backup_$$(date +%Y%m%d_%H%M%S).sql

# ============================================
# TESTING
# ============================================

test: ## Run all tests
	docker-compose exec backend pytest -v

test-cov: ## Run tests with coverage
	docker-compose exec backend pytest --cov=app --cov-report=html

test-backend: ## Run backend tests
	docker-compose exec backend pytest tests/ -v

test-frontend: ## Run frontend tests
	docker-compose exec frontend npm test

# ============================================
# LINTING & FORMATTING
# ============================================

lint: ## Run linters
	docker-compose exec backend ruff check app/
	docker-compose exec frontend npm run lint

format: ## Format code
	docker-compose exec backend ruff format app/
	docker-compose exec frontend npm run format

type-check: ## Run type checking
	docker-compose exec backend mypy app/
	docker-compose exec frontend npm run type-check

# ============================================
# UTILITIES
# ============================================

shell-backend: ## Open shell in backend container
	docker-compose exec backend bash

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend sh

redis-cli: ## Open Redis CLI
	docker-compose exec redis redis-cli

clean: ## Clean up containers, images, and volumes
	docker-compose down -v --rmi local
	docker system prune -f

install-deps: ## Install all dependencies
	cd backend && poetry install
	cd frontend && npm install

# ============================================
# INITIAL SETUP
# ============================================

init: ## Initial project setup
	@echo "$(GREEN)Setting up PromptCraft...$(NC)"
	cp .env.example .env
	@echo "$(YELLOW)Please edit .env with your configuration$(NC)"
	make build
	make migrate
	make seed
	@echo "$(GREEN)Setup complete! Run 'make dev-all' to start$(NC)"
```

---

## Plan de Implementacion (Fases)

### Fase 1: Infraestructura Base (Semana 1-2)
```
[ ] Crear estructura de directorios
[ ] Configurar Docker Compose
[ ] Configurar Makefile
[ ] Setup PostgreSQL + Redis
[ ] Configurar Alembic
[ ] Backend FastAPI base
    [ ] Config con Pydantic Settings
    [ ] Async database session
    [ ] Health check endpoint
[ ] Frontend React base
    [ ] Vite + TypeScript
    [ ] Tailwind CSS
    [ ] Router basico
```

### Fase 2: Autenticacion (Semana 2-3)
```
[ ] Modelo User
[ ] Migracion inicial
[ ] Endpoints auth
    [ ] Register
    [ ] Login
    [ ] Refresh token
    [ ] Logout
[ ] JWT middleware
[ ] Password hashing (Argon2)
[ ] Frontend auth
    [ ] Login page
    [ ] Register page
    [ ] Protected routes
    [ ] Auth store (Zustand)
```

### Fase 3: Contenido - Lecciones (Semana 3-4)
```
[ ] Modelos Lesson, LessonProgress
[ ] Migraciones
[ ] CRUD endpoints
[ ] Lesson service
[ ] Seed data - 10 lecciones
[ ] Frontend
    [ ] Lista de lecciones
    [ ] Detalle de leccion
    [ ] Progreso visual
    [ ] Ejercicios interactivos
```

### Fase 4: Puzzles (Semana 4-5)
```
[ ] Modelos Puzzle, PuzzleAttempt
[ ] Migraciones
[ ] Puzzle engine (logica)
[ ] Validador de soluciones
[ ] Endpoints
[ ] Seed data - 8 puzzles
[ ] Frontend
    [ ] Lista de puzzles
    [ ] LogicGrid component
    [ ] Timer component
    [ ] Sistema de pistas
```

### Fase 5: Gamificacion Core (Semana 5-6)
```
[ ] Modelos XP, Level, Streak
[ ] Migraciones
[ ] XP service con multiplicadores
[ ] Level service
[ ] Streak service
[ ] Celery tasks para daily checks
[ ] Frontend
    [ ] XP Bar
    [ ] Level Badge
    [ ] Streak Flame
    [ ] Animaciones de XP
```

### Fase 6: Badges & Achievements (Semana 6-7)
```
[ ] Modelos Badge, UserBadge
[ ] 30+ badges definidos
[ ] Badge checker service
[ ] Celery tasks para checks
[ ] Frontend
    [ ] Badge grid
    [ ] Badge detail modal
    [ ] Unlock animations
    [ ] Progress indicators
```

### Fase 7: Leaderboards (Semana 7-8)
```
[ ] Redis sorted sets
[ ] Leaderboard service
[ ] Daily/Weekly/AllTime
[ ] API endpoints
[ ] Frontend
    [ ] Leaderboard page
    [ ] User rank display
    [ ] Real-time updates
```

### Fase 8: Real-time & Polish (Semana 8-9)
```
[ ] WebSocket setup
[ ] Notification service
[ ] Live updates
    [ ] XP earned
    [ ] Level up
    [ ] Badge unlock
    [ ] Leaderboard changes
[ ] Daily challenges
[ ] Celery scheduled tasks
[ ] Email notifications (opcional)
```

### Fase 9: Testing & QA (Semana 9-10)
```
[ ] Unit tests backend (pytest)
[ ] Integration tests
[ ] Frontend tests (Vitest)
[ ] E2E tests (Playwright)
[ ] Performance testing
[ ] Security audit
[ ] Bug fixes
```

### Fase 10: Deployment (Semana 10)
```
[ ] Production Docker config
[ ] CI/CD pipeline
[ ] SSL certificates
[ ] Monitoring setup
[ ] Backup strategy
[ ] Documentation final
[ ] Launch!
```

---

## Metricas de Exito

| Metrica | Target |
|---------|--------|
| Tiempo de carga inicial | < 2s |
| API response time (P95) | < 200ms |
| WebSocket latency | < 50ms |
| Uptime | 99.9% |
| Test coverage | > 80% |
| Lighthouse score | > 90 |

---

## Notas de Seguridad

1. **Passwords**: Argon2 hashing, nunca plaintext
2. **JWT**: Tokens de corta duracion (30 min), refresh tokens
3. **Rate Limiting**: Por IP y por usuario
4. **CORS**: Configuracion restrictiva
5. **Input Validation**: Pydantic en todo
6. **SQL Injection**: Prevenido por SQLAlchemy ORM
7. **XSS**: React escapa por defecto
8. **HTTPS**: Obligatorio en produccion
9. **Secrets**: Variables de entorno, nunca en codigo
10. **Database**: Usuario con minimos privilegios

---

## Estimacion de Recursos

### Desarrollo
- 1 Backend Developer (Python/FastAPI)
- 1 Frontend Developer (React/TypeScript)
- 10 semanas de desarrollo

### Infraestructura (Produccion Inicial)
- VPS: 4 vCPU, 8GB RAM (~$40/mes)
- PostgreSQL managed: (~$15/mes)
- Redis managed: (~$10/mes)
- Domain + SSL: (~$15/ano)
- **Total**: ~$65/mes

---

*Plan creado basado en investigacion de mejores practicas 2024-2025*
*Inspirado en la arquitectura de Duolingo y plataformas de gamificacion modernas*
