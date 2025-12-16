# PromptCraft - Curso Interactivo de Prompt Engineering

Aplicacion web interactiva para aprender Prompt Engineering, construida con Brython (Python en el navegador) y Tailwind CSS.

## Caracteristicas

- **Lecciones Interactivas**: 10+ lecciones que cubren desde fundamentos hasta tecnicas avanzadas
- **Logic Grid Puzzles**: Puzzles de logica estilo Zebra para practicar conceptos
- **Gamificacion Completa**: Sistema de XP, niveles, badges y rachas
- **Playground**: Experimenta con prompts en tiempo real
- **Progreso Persistente**: Tu progreso se guarda en localStorage

## Estructura del Proyecto

```
promptcraft-brython/
├── index.html              # Punto de entrada principal
├── brython_modules/         # Modulos Python para Brython
│   ├── __init__.py
│   ├── app.py              # Aplicacion principal
│   ├── router.py           # Sistema de enrutamiento SPA
│   ├── state.py            # Gestion de estado
│   ├── components/         # Componentes UI reutilizables
│   │   ├── base.py         # Clase base Component
│   │   ├── button.py       # Botones
│   │   ├── card.py         # Tarjetas
│   │   ├── modal.py        # Modales
│   │   ├── tabs.py         # Pestanas
│   │   ├── progress.py     # Barras de progreso
│   │   ├── grid.py         # Grids de logica
│   │   ├── hints.py        # Sistema de pistas
│   │   ├── toast.py        # Notificaciones
│   │   ├── code_editor.py  # Editor de codigo
│   │   └── badge_display.py # Display de badges
│   ├── pages/              # Paginas de la aplicacion
│   │   ├── home.py         # Pagina principal
│   │   ├── lessons.py      # Lista de lecciones
│   │   ├── lesson_detail.py # Detalle de leccion
│   │   ├── puzzles.py      # Lista de puzzles
│   │   ├── puzzle.py       # Puzzle individual
│   │   ├── playground.py   # Playground de prompts
│   │   ├── profile.py      # Perfil de usuario
│   │   └── badges.py       # Coleccion de badges
│   ├── puzzles/            # Sistema de puzzles
│   │   ├── engine.py       # Motor del puzzle
│   │   ├── logic_puzzle.py # Componente de puzzle
│   │   ├── timer.py        # Temporizador
│   │   ├── solver.py       # Solucionador/validador
│   │   ├── loader.py       # Cargador de puzzles
│   │   └── generator.py    # Generador de puzzles
│   ├── gamification/       # Sistema de gamificacion
│   │   ├── xp.py           # Sistema de XP
│   │   ├── levels.py       # Sistema de niveles
│   │   ├── badges.py       # Sistema de badges
│   │   ├── streaks.py      # Sistema de rachas
│   │   ├── achievements.py # Logros
│   │   └── leaderboard.py  # Tabla de posiciones
│   └── lessons/            # Sistema de lecciones
│       ├── content.py      # Contenido de lecciones
│       ├── loader.py       # Cargador de lecciones
│       ├── renderer.py     # Renderizador de contenido
│       └── progress.py     # Progreso de lecciones
├── static/
│   └── css/
│       └── custom.css      # Estilos personalizados
└── data/                   # Datos JSON
    ├── puzzles.json        # Definiciones de puzzles
    ├── achievements.json   # Logros y retos
    └── tips.json           # Tips y templates
```

## Como Usar

1. Abre `index.html` en un navegador web moderno
2. La aplicacion cargara automaticamente usando Brython
3. Navega usando el menu superior
4. Tu progreso se guarda automaticamente

## Tecnologias

- **Brython 3.12**: Python 3 en el navegador
- **Tailwind CSS**: Framework de utilidades CSS
- **localStorage**: Persistencia de datos del usuario

## Desarrollo

Para modificar el proyecto:

1. Edita los archivos Python en `brython_modules/`
2. Los cambios se reflejan al recargar la pagina
3. Usa la consola del navegador para debug (Brython imprime ahi)

## Contenido del Curso

### Fundamentos
- Introduccion al Prompt Engineering
- Anatomia de un Prompt

### Tecnicas
- Zero-Shot Prompting
- Few-Shot Prompting
- Chain of Thought (CoT)
- Role Prompting

### Avanzado
- Self-Consistency
- Prompt Chaining

### Aplicaciones
- Prompts para Codigo
- Prompts para Escritura

## Licencia

Proyecto educativo de uso libre.
