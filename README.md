# PromptCraft - Aprende Prompt Engineering + Claude Code

Un curso interactivo y divertido para aprender a comunicarte con inteligencias artificiales.

## ¿Qué vas a aprender?

- **Prompt Engineering**: Cómo escribir instrucciones efectivas para ChatGPT, Claude, y otros modelos de IA
- **Claude Code**: Programar asistido por IA directamente en tu terminal
- **Práctica con puzzles**: Resuelve retos lógicos mientras aprendes conceptos

## Comenzar en 2 minutos

### Opción 1: Ver online (más fácil)
1. Ve a la página del curso: `https://TU_USUARIO.github.io/promptcraft-brython-/`

### Opción 2: Tu propia copia (para modificar)
1. Haz clic en el botón **Fork** arriba a la derecha
2. En tu fork, ve a **Settings** → **Pages**
3. En "Source" selecciona **Deploy from a branch**
4. Selecciona la rama `main` y carpeta `/ (root)`
5. Espera 1-2 minutos y visita `https://TU_USUARIO.github.io/promptcraft-brython-/`

### Opción 3: En tu computadora
1. Descarga o clona el repositorio
2. Abre el archivo `index.html` en tu navegador
3. ¡Listo! No necesitas instalar nada

## ¿Qué incluye el curso?

| Módulo | Descripción | Lecciones |
|--------|-------------|-----------|
| Fundamentos | Qué es Prompt Engineering y cómo empezar | 3 |
| Técnicas | Zero-shot, Few-shot, Chain of Thought | 4 |
| Claude Code | Programar con IA en tu terminal | 6 |
| Avanzado | Técnicas profesionales | 2 |
| Aplicaciones | Código, escritura, análisis | 2 |

También incluye:
- 12 puzzles interactivos de lógica
- Sistema de XP y niveles (como Duolingo)
- Badges coleccionables
- Rachas diarias para mantener el hábito

## Estructura simplificada

```
promptcraft-brython-/
├── index.html          ← Abre esto en el navegador
├── data/
│   ├── puzzles.json    ← Los puzzles están aquí
│   └── tips.json       ← Tips y consejos
└── brython_modules/
    └── lessons/
        └── content.py  ← El contenido de las lecciones
```

## Cómo modificar el contenido

### Agregar un tip nuevo

1. Abre `data/tips.json`
2. Busca `"daily_tips": [`
3. Agrega tu tip al final:
```json
{
  "id": "tip-mi-consejo",
  "title": "Mi Consejo",
  "content": "El texto de tu consejo aquí...",
  "category": "fundamentals",
  "icon": "💡"
}
```
4. Guarda y recarga la página

### Modificar una lección

1. Abre `brython_modules/lessons/content.py`
2. Busca `EMBEDDED_LESSONS = [`
3. Encuentra la lección que quieres modificar
4. Edita el contenido en el campo `'content':`
5. Guarda y recarga la página

## Preguntas Frecuentes

### ¿Por qué no funciona al abrir el archivo?
Algunos navegadores bloquean archivos locales. Prueba con Firefox o usa un servidor simple:
```bash
python -m http.server 8000
```
Luego abre `http://localhost:8000`

### ¿Dónde se guarda mi progreso?
En el almacenamiento local de tu navegador (localStorage). Si borras los datos del navegador, perderás el progreso.

### ¿Puedo usarlo sin internet?
Sí, una vez cargado funciona completamente offline.

### ¿Cómo contribuyo con más contenido?
¡Mira el archivo [CONTRIBUTING.md](CONTRIBUTING.md) para una guía paso a paso!

### ¿Qué es Brython?
Es Python que corre en el navegador. No necesitas saber Python para usar el curso, pero si lo sabes, puedes ver cómo funciona todo.

## Tecnologías usadas

- **Brython**: Python en el navegador (sin servidor)
- **Tailwind CSS**: Estilos bonitos sin escribir CSS
- **localStorage**: Guarda tu progreso localmente

## Licencia

Proyecto educativo de uso libre. Modifícalo, compártelo, aprende con él.

---

¿Te fue útil? Dale una estrella en GitHub.
