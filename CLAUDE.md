# CLAUDE.md - Guía para Claude Code

## Resumen del Proyecto

**PromptCraft** es un curso interactivo de Prompt Engineering construido con Brython (Python en el navegador) y Tailwind CSS. Está diseñado para desplegarse en **GitHub Pages** sin backend.

## Stack Técnico

- **Frontend**: Brython 3.12.0 (Python → JavaScript)
- **Estilos**: Tailwind CSS via CDN
- **Persistencia**: localStorage (sin backend)
- **Hosting**: GitHub Pages (estático)

## Estructura del Proyecto

```
promptcraft-brython-/
├── index.html              # Punto de entrada principal
├── guia.html               # Guía para principiantes (IA, chats, ganar dinero)
├── guia-claude-code.html   # Guía avanzada (GitHub, Claude Code, MCPs)
├── brython_modules/        # Código Python principal
│   ├── app.py              # Aplicación principal y rutas
│   ├── state.py            # Estado global (localStorage)
│   ├── router.py           # Router SPA basado en hash
│   ├── pages/              # Páginas de la aplicación
│   │   ├── home.py
│   │   ├── lessons.py
│   │   ├── practice.py
│   │   ├── assessment.py
│   │   ├── claude_exercises.py
│   │   ├── final_project.py
│   │   └── ...
│   ├── gamification/       # Sistema de XP, badges, niveles
│   │   ├── xp.py
│   │   ├── badges.py
│   │   └── levels.py
│   └── lessons/
│       └── content.py      # Contenido de las lecciones
├── data/
│   ├── puzzles.json
│   └── tips.json
└── static/
    └── css/custom.css
```

## Comandos Útiles

```bash
# Servidor local para desarrollo (requerido para Brython)
python3 -m http.server 8000

# Verificar sintaxis Python
python3 -m py_compile brython_modules/pages/*.py

# Ver en navegador
open http://localhost:8000
```

## Convenciones de Código

### Brython (Python en navegador)

```python
# Imports de Brython
from browser import document, html, window
from browser.local_storage import storage

# Crear elementos DOM
container = html.DIV(Class="my-class")
container <= html.P("Texto")  # <= es como appendChild

# Eventos
button.bind('click', lambda e: handle_click())

# Acceder al DOM
element = document.getElementById("my-id")
element.innerHTML = ""
```

### Patrón de Páginas

```python
def my_page(params):
    """Cada página recibe params del router."""
    state = get_state()
    container = html.DIV(Class="...")
    # ... construir UI
    return container
```

### Sistema de XP

```python
# Firma correcta de award_xp
from ..gamification.xp import award_xp
award_xp(state, 'activity_type', amount, modifiers, "Razón")

# Ejemplo
award_xp(state, 'lesson_complete', 50, None, "Lección completada")
```

## Rutas Registradas

| Ruta | Página | Descripción |
|------|--------|-------------|
| `#home` | home_page | Página principal |
| `#lessons` | lessons_page | Lista de lecciones |
| `#lesson/:id` | lesson_detail_page | Detalle de lección |
| `#practice` | practice_page | Sandbox de práctica |
| `#practice/:id` | practice_exercise_page | Ejercicio específico |
| `#assessment` | assessment_page | Evaluación diagnóstica |
| `#claude-exercises` | claude_exercises_page | Ejercicios Claude Code |
| `#puzzles` | puzzles_page | Lista de puzzles |
| `#playground` | playground_page | Área libre |
| `#final-project` | final_project_page | Proyecto final |
| `#profile` | profile_page | Perfil del usuario |
| `#badges` | badges_page | Colección de badges |

## Notas Importantes

### Brython NO funciona con file://
Siempre usar servidor HTTP local. El navegador bloquea AJAX desde `file://`.

### Debug de Brython
En `index.html`, cambiar `debug: 0` a `debug: 2` para ver errores:
```html
<body onload="brython({debug: 2, cache: false})">
```

### Imports relativos
Dentro de `brython_modules/pages/`:
```python
from ..state import get_state          # Un nivel arriba
from ..gamification.xp import award_xp # Dos niveles arriba + carpeta
```

### localStorage
El estado se guarda automáticamente:
```python
state = get_state()
state.data['key'] = value
state.save()  # Persiste en localStorage
```

## Guías HTML

- **guia.html**: Para principiantes absolutos (qué es IA, usar ChatGPT/Claude/Gemini, ganar dinero)
- **guia-claude-code.html**: Para usuarios técnicos (GitHub, fork, Claude Code, MCPs)

Ambas guías son standalone HTML con Tailwind CDN.

## Despliegue

El proyecto está configurado para GitHub Pages:
1. `.nojekyll` presente para evitar procesamiento Jekyll
2. Todo es estático, no requiere build
3. Push a `main` → automáticamente disponible en GitHub Pages

## Problemas Comunes

| Problema | Solución |
|----------|----------|
| Página muestra fallback estático | Usar servidor HTTP, no abrir file:// |
| Botones no responden | Revisar consola (F12), habilitar debug: 2 |
| award_xp no funciona | Verificar firma: `award_xp(state, activity, amount, modifiers, reason)` |
| Import error | Verificar rutas relativas (`..` para subir nivel) |
