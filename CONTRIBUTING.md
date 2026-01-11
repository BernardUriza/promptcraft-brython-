# Guía de Experimentación

¡Bienvenido! Este documento te guía para experimentar con el código del curso. No tengas miedo de romper cosas - siempre puedes volver a descargar el proyecto.

## Antes de empezar

1. Haz fork o descarga el proyecto
2. Abre `index.html` en tu navegador para ver cómo se ve ahora
3. Abre los archivos en un editor de texto (VS Code, Notepad++, o cualquiera)

## Experimento 1: Cambiar un mensaje

**Dificultad:** Muy fácil (2 minutos)

**Objetivo:** Cambiar el texto de un tip

1. Abre `data/tips.json`
2. Busca este texto:
```json
"title": "Sé específico",
```
3. Cámbialo por:
```json
"title": "¡Sé MUY específico!",
```
4. Guarda el archivo
5. Recarga la página en el navegador
6. Ve a la sección de Tips - ¡verás tu cambio!

**Qué aprendiste:** Los archivos JSON son listas de datos. Puedes cambiar textos sin saber programar.

---

## Experimento 2: Agregar tu propio tip

**Dificultad:** Fácil (5 minutos)

**Objetivo:** Crear un tip nuevo que aparezca en el curso

1. Abre `data/tips.json`
2. Busca la línea `"daily_tips": [`
3. Ve hasta el último tip (antes del `]`)
4. Después del `}` del último tip, agrega una coma y tu tip:

```json
    },
    {
      "id": "tip-mi-primer-tip",
      "title": "Mi Primer Consejo",
      "content": "Este es mi propio consejo para usar IA: siempre revisa lo que genera antes de usarlo.",
      "category": "fundamentals",
      "icon": "🌟"
    }
  ],
```

5. Guarda y recarga

**Qué aprendiste:** La estructura de JSON usa `{ }` para objetos y `[ ]` para listas.

---

## Experimento 3: Crear un puzzle simple

**Dificultad:** Media (15 minutos)

**Objetivo:** Agregar un puzzle nuevo sobre cualquier tema

1. Abre `data/puzzles.json`
2. Busca `"puzzles": [`
3. Antes del `]` que cierra los puzzles, agrega:

```json
    },
    {
      "id": "mi-primer-puzzle",
      "title": "Frutas y Colores",
      "description": "Relaciona cada fruta con su color típico.",
      "difficulty": "easy",
      "category": "fundamentals",
      "xp_reward": 25,
      "time_limit": 180,
      "grid_size": {
        "rows": 3,
        "cols": 3
      },
      "categories": [
        {
          "name": "Fruta",
          "items": ["Manzana", "Plátano", "Uva"]
        },
        {
          "name": "Color",
          "items": ["Rojo", "Amarillo", "Morado"]
        }
      ],
      "clues": [
        {
          "text": "La manzana es de color rojo.",
          "reveals": [["Manzana", "Rojo"]]
        },
        {
          "text": "El plátano es amarillo cuando está maduro.",
          "reveals": [["Plátano", "Amarillo"]]
        },
        {
          "text": "Las uvas pueden ser moradas.",
          "reveals": [["Uva", "Morado"]]
        }
      ],
      "solution": {
        "Manzana": "Rojo",
        "Plátano": "Amarillo",
        "Uva": "Morado"
      }
    }
```

4. Guarda y recarga
5. Ve a la sección de Puzzles - ¡tu puzzle aparecerá!

**Qué aprendiste:**
- Los puzzles tienen una estructura definida
- `categories` define las columnas
- `clues` son las pistas que revelan relaciones
- `solution` valida las respuestas correctas

---

## Experimento 4: Modificar una lección existente

**Dificultad:** Media (10 minutos)

**Objetivo:** Agregar contenido a una lección

1. Abre `brython_modules/lessons/content.py`
2. Busca `EMBEDDED_LESSONS = [`
3. Encuentra cualquier lección (busca `'id': 'intro-prompt'` por ejemplo)
4. Dentro del campo `'content':`, agrega un nuevo párrafo

El contenido usa formato especial:
- `## Título` = Título grande
- `**texto**` = Texto en negrita
- `- item` = Lista con viñetas
- ``` `código` ``` = Código inline
- `<tip>texto</tip>` = Caja de consejo

5. Guarda y recarga

---

## Experimento 5: Agregar un badge

**Dificultad:** Media-Alta (10 minutos)

**Objetivo:** Crear un badge personalizado

1. Abre `brython_modules/gamification/badges.py`
2. Busca `BADGES = {`
3. Agrega tu badge dentro del diccionario:

```python
    'mi_badge': {
        'id': 'mi_badge',
        'name': 'Mi Primer Badge',
        'description': 'Lo creé yo mismo',
        'icon': '🏅',
        'rarity': 'legendary',
        'category': 'special',
        'condition': {'type': 'xp', 'value': 1},
    },
```

4. Guarda y recarga
5. Ve a la sección de Badges

**Raridades disponibles:** `common`, `rare`, `epic`, `legendary`

---

## Estructura de archivos clave

| Archivo | Qué contiene | Para qué lo modificarías |
|---------|--------------|-------------------------|
| `data/puzzles.json` | Todos los puzzles | Agregar nuevos puzzles |
| `data/tips.json` | Tips y plantillas | Agregar consejos |
| `brython_modules/lessons/content.py` | Texto de las lecciones | Modificar contenido educativo |
| `brython_modules/gamification/badges.py` | Definición de badges | Crear nuevos logros |

## Solución de problemas comunes

### "La página no carga después de mi cambio"
- Probablemente hay un error de sintaxis
- En JSON: revisa que todas las comas estén bien
- Abre la consola del navegador (F12) para ver el error
- Compara con otros elementos similares en el archivo

### "Mi puzzle no aparece"
- Verifica que el JSON sea válido (usa un validador online)
- Asegúrate de agregar la coma antes de tu nuevo puzzle
- El `id` debe ser único

### "No veo mis cambios"
- ¿Guardaste el archivo?
- ¿Recargaste la página? (Ctrl+F5 para forzar)
- ¿Estás editando el archivo correcto?

## Próximos pasos

Una vez que domines estos experimentos, puedes:

1. **Crear un módulo completo** de lecciones sobre tu tema favorito
2. **Traducir el curso** a otro idioma
3. **Cambiar los estilos** modificando las clases de Tailwind en los templates
4. **Agregar nuevas categorías** de puzzles

## ¿Necesitas ayuda?

- Revisa el código de elementos similares como guía
- Los comentarios en el código Python explican qué hace cada cosa
- Experimenta sin miedo - siempre puedes re-descargar el proyecto

¡Diviértete experimentando!
