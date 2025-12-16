# PromptCraft - Lesson Content
# Contenido de lecciones embebido

LESSON_CATEGORIES = [
    {
        'id': 'fundamentals',
        'name': 'Fundamentos',
        'icon': '📚',
        'description': 'Conceptos básicos de Prompt Engineering',
        'order': 1
    },
    {
        'id': 'techniques',
        'name': 'Técnicas',
        'icon': '🎯',
        'description': 'Técnicas avanzadas de prompting',
        'order': 2
    },
    {
        'id': 'advanced',
        'name': 'Avanzado',
        'icon': '🚀',
        'description': 'Estrategias avanzadas y optimización',
        'order': 3
    },
    {
        'id': 'applications',
        'name': 'Aplicaciones',
        'icon': '💼',
        'description': 'Casos de uso prácticos',
        'order': 4
    }
]

EMBEDDED_LESSONS = {
    # ============================================
    # FUNDAMENTOS
    # ============================================
    'intro-prompt-engineering': {
        'id': 'intro-prompt-engineering',
        'title': 'Introducción al Prompt Engineering',
        'category': 'fundamentals',
        'difficulty': 'beginner',
        'duration': 10,
        'xp_reward': 50,
        'icon': '🎯',
        'description': 'Aprende qué es el Prompt Engineering y por qué es importante.',
        'objectives': [
            'Entender qué es un prompt',
            'Conocer la importancia del Prompt Engineering',
            'Identificar los componentes de un buen prompt'
        ],
        'sections': [
            {
                'type': 'text',
                'title': '¿Qué es un Prompt?',
                'content': '''Un **prompt** es la instrucción o entrada que le das a un modelo de lenguaje (LLM) para obtener una respuesta.

Piensa en el prompt como una pregunta o solicitud que haces a un asistente muy capaz pero literal: la calidad de la respuesta depende directamente de cómo formules tu solicitud.

El **Prompt Engineering** es el arte y ciencia de diseñar prompts efectivos para obtener los mejores resultados posibles de los modelos de IA.'''
            },
            {
                'type': 'tip',
                'content': 'Los LLMs son como genios de las lámparas: hacen exactamente lo que pides, no necesariamente lo que quieres. La precisión es clave.'
            },
            {
                'type': 'text',
                'title': '¿Por qué es importante?',
                'content': '''El mismo modelo puede dar respuestas muy diferentes dependiendo de cómo le preguntes. Un buen prompt puede:

• **Mejorar la precisión** de las respuestas
• **Reducir alucinaciones** (información inventada)
• **Ahorrar tiempo** al obtener lo que necesitas al primer intento
• **Desbloquear capacidades** que no sabías que el modelo tenía'''
            },
            {
                'type': 'example',
                'title': 'Ejemplo: Prompt básico vs mejorado',
                'bad_example': {
                    'prompt': 'Escribe sobre perros',
                    'issue': 'Demasiado vago. ¿Qué tipo de contenido? ¿Qué extensión? ¿Qué tono?'
                },
                'good_example': {
                    'prompt': 'Escribe un párrafo de 100 palabras explicando los beneficios de tener un perro como mascota para niños, usando un tono amigable y educativo.',
                    'why': 'Específico en: tipo de contenido, extensión, audiencia y tono.'
                }
            },
            {
                'type': 'text',
                'title': 'Componentes de un Buen Prompt',
                'content': '''Un prompt efectivo generalmente incluye:

1. **Contexto**: Información de fondo relevante
2. **Instrucción clara**: Qué quieres que haga exactamente
3. **Formato de salida**: Cómo quieres la respuesta
4. **Restricciones**: Límites o condiciones a seguir

No todos los prompts necesitan los 4 componentes, pero tenerlos en mente te ayudará a crear mejores instrucciones.'''
            }
        ],
        'exercise': {
            'type': 'improve_prompt',
            'instruction': 'Mejora el siguiente prompt aplicando lo aprendido:',
            'original_prompt': 'Dame ideas de negocios',
            'hints': [
                'Añade contexto sobre tu situación',
                'Especifica el tipo de negocio que buscas',
                'Indica restricciones como presupuesto o tiempo'
            ],
            'solution_keywords': ['específico', 'contexto', 'formato', 'restricción']
        },
        'next_lesson': 'anatomy-of-prompt'
    },

    'anatomy-of-prompt': {
        'id': 'anatomy-of-prompt',
        'title': 'Anatomía de un Prompt',
        'category': 'fundamentals',
        'difficulty': 'beginner',
        'duration': 15,
        'xp_reward': 75,
        'icon': '🔬',
        'description': 'Desglosa las partes que componen un prompt efectivo.',
        'objectives': [
            'Identificar las partes de un prompt',
            'Entender el rol de cada componente',
            'Construir prompts estructurados'
        ],
        'sections': [
            {
                'type': 'text',
                'title': 'Las 6 Partes de un Prompt',
                'content': '''Un prompt completo puede tener hasta 6 componentes. No todos son obligatorios, pero conocerlos te da más herramientas:

1. **Rol/Persona** - Quién debe ser el modelo
2. **Contexto** - Información de fondo
3. **Tarea** - La instrucción principal
4. **Formato** - Cómo estructurar la salida
5. **Ejemplos** - Demostraciones del resultado esperado
6. **Restricciones** - Límites y condiciones'''
            },
            {
                'type': 'code',
                'title': 'Estructura Visual',
                'language': 'text',
                'code': '''[ROL] Actúa como un experto en marketing digital.

[CONTEXTO] Tengo una tienda online de productos orgánicos
que lleva 6 meses operando con ventas bajas.

[TAREA] Analiza posibles causas y sugiere 3 estrategias
de mejora.

[FORMATO] Presenta cada estrategia con:
- Nombre de la estrategia
- Descripción breve
- Pasos de implementación
- Resultado esperado

[RESTRICCIONES]
- Presupuesto limitado ($500/mes)
- Equipo de 2 personas
- Enfoque en redes sociales'''
            },
            {
                'type': 'tip',
                'content': 'No necesitas usar etiquetas como [ROL] o [CONTEXTO] en tus prompts reales. Son útiles para aprender, pero puedes escribirlo de forma más natural.'
            },
            {
                'type': 'text',
                'title': '1. Rol/Persona',
                'content': '''Asignar un rol al modelo cambia su "perspectiva" y el tipo de respuesta que da.

**Ejemplos de roles:**
• "Actúa como un profesor de primaria"
• "Eres un crítico gastronómico exigente"
• "Responde como un desarrollador senior de Python"

El rol afecta el vocabulario, nivel de detalle y enfoque de la respuesta.'''
            },
            {
                'type': 'example',
                'title': 'Impacto del Rol',
                'bad_example': {
                    'prompt': 'Explica qué es la fotosíntesis',
                    'issue': 'Respuesta genérica, sin nivel definido'
                },
                'good_example': {
                    'prompt': 'Actúa como un profesor de biología de secundaria. Explica qué es la fotosíntesis a estudiantes de 14 años, usando analogías simples.',
                    'why': 'El rol define el nivel y estilo de explicación'
                }
            },
            {
                'type': 'text',
                'title': '2. Contexto',
                'content': '''El contexto es la información de fondo que el modelo necesita para dar una respuesta relevante.

**Incluye:**
• Tu situación actual
• Información relevante del problema
• Intentos previos (si aplica)
• Público objetivo

**Ejemplo:** "Estoy preparando una presentación para inversores de mi startup de tecnología educativa que lleva 2 años en el mercado..."'''
            },
            {
                'type': 'text',
                'title': '3. Tarea',
                'content': '''La tarea es el corazón del prompt: qué quieres que el modelo haga.

**Usa verbos de acción claros:**
• Analiza, Compara, Resume
• Genera, Crea, Diseña
• Explica, Describe, Define
• Traduce, Convierte, Transforma
• Revisa, Corrige, Mejora

**Sé específico:** "Escribe" es vago. "Escribe un email de seguimiento de 3 párrafos" es mejor.'''
            },
            {
                'type': 'text',
                'title': '4. Formato de Salida',
                'content': '''Especificar el formato evita tener que reformatear la respuesta.

**Opciones comunes:**
• Lista numerada o con viñetas
• Tabla comparativa
• Código con comentarios
• Párrafos con subtítulos
• JSON o estructura de datos
• Paso a paso

**Ejemplo:** "Presenta la información en una tabla con columnas: Ventaja, Desventaja, Ejemplo"'''
            },
            {
                'type': 'text',
                'title': '5. Ejemplos (Few-Shot)',
                'content': '''Los ejemplos muestran exactamente qué tipo de respuesta esperas. Son especialmente útiles para:

• Tareas de clasificación
• Formatos específicos
• Tono particular
• Transformaciones de texto

Veremos esto en detalle en la lección de Few-Shot Prompting.'''
            },
            {
                'type': 'text',
                'title': '6. Restricciones',
                'content': '''Las restricciones definen límites y condiciones:

• **Longitud:** "máximo 200 palabras"
• **Estilo:** "sin jerga técnica"
• **Contenido:** "no menciones competidores"
• **Idioma:** "responde en español formal"
• **Recursos:** "usa solo información verificable"

Las restricciones ayudan a acotar la respuesta y evitar contenido no deseado.'''
            }
        ],
        'exercise': {
            'type': 'build_prompt',
            'instruction': 'Construye un prompt completo usando al menos 4 de los 6 componentes para la siguiente tarea: Necesitas ideas para mejorar la productividad de tu equipo remoto.',
            'required_components': ['rol', 'contexto', 'tarea', 'formato'],
            'hints': [
                '¿Qué tipo de experto podría ayudarte?',
                '¿Qué información sobre tu equipo es relevante?',
                '¿En qué formato quieres las ideas?'
            ]
        },
        'next_lesson': 'zero-shot-prompting'
    },

    # ============================================
    # TÉCNICAS
    # ============================================
    'zero-shot-prompting': {
        'id': 'zero-shot-prompting',
        'title': 'Zero-Shot Prompting',
        'category': 'techniques',
        'difficulty': 'beginner',
        'duration': 12,
        'xp_reward': 60,
        'icon': '0️⃣',
        'description': 'Aprende a crear prompts efectivos sin necesidad de ejemplos.',
        'objectives': [
            'Entender qué es Zero-Shot',
            'Saber cuándo usarlo',
            'Crear prompts Zero-Shot efectivos'
        ],
        'sections': [
            {
                'type': 'text',
                'title': '¿Qué es Zero-Shot?',
                'content': '''**Zero-Shot Prompting** es cuando le pides al modelo que realice una tarea sin darle ejemplos previos de cómo hacerlo.

"Zero" se refiere a cero ejemplos. Confías en que el modelo ya sabe cómo hacer la tarea basándose en su entrenamiento.

Es la forma más simple y directa de prompting, y funciona sorprendentemente bien para muchas tareas comunes.'''
            },
            {
                'type': 'example',
                'title': 'Ejemplo de Zero-Shot',
                'bad_example': {
                    'prompt': 'Sentimiento',
                    'issue': 'No hay contexto ni instrucción clara'
                },
                'good_example': {
                    'prompt': 'Clasifica el sentimiento del siguiente texto como positivo, negativo o neutro:\n\n"El servicio fue excelente y la comida deliciosa, aunque los precios son algo elevados."',
                    'why': 'Instrucción clara con opciones definidas, sin necesidad de ejemplos'
                }
            },
            {
                'type': 'text',
                'title': 'Cuándo Usar Zero-Shot',
                'content': '''Zero-Shot funciona bien cuando:

✅ La tarea es común y bien definida
✅ El modelo probablemente ha visto tareas similares
✅ No necesitas un formato muy específico
✅ Quieres rapidez y simplicidad

**Tareas ideales para Zero-Shot:**
• Traducción
• Resumen
• Clasificación simple
• Preguntas factuales
• Generación de texto general'''
            },
            {
                'type': 'text',
                'title': 'Cuándo NO Usar Zero-Shot',
                'content': '''Considera otras técnicas cuando:

❌ Necesitas un formato muy específico
❌ La tarea es poco común o especializada
❌ Requieres consistencia exacta en el estilo
❌ El modelo falla repetidamente

En estos casos, Few-Shot o Chain of Thought pueden ser mejores opciones.'''
            },
            {
                'type': 'tip',
                'content': 'Siempre intenta Zero-Shot primero. Es más simple y a menudo suficiente. Solo añade complejidad si es necesario.'
            },
            {
                'type': 'code',
                'title': 'Patrones Zero-Shot Efectivos',
                'language': 'text',
                'code': '''# Patrón de Clasificación
"Clasifica el siguiente [tipo] como [categoría A], [categoría B] o [categoría C]:
[contenido]"

# Patrón de Extracción
"Extrae [información específica] del siguiente texto:
[texto]"

# Patrón de Transformación
"Convierte el siguiente [formato A] a [formato B]:
[contenido]"

# Patrón de Generación
"Genera [tipo de contenido] sobre [tema] que sea [características]."'''
            }
        ],
        'exercise': {
            'type': 'create_prompt',
            'instruction': 'Crea un prompt Zero-Shot para clasificar emails como "urgente", "importante" o "puede esperar".',
            'test_input': 'Email: "Hola, te envío el informe mensual como acordamos. Revísalo cuando puedas."',
            'expected_classification': 'puede esperar',
            'hints': [
                'Define claramente las 3 categorías',
                'Incluye el email a clasificar',
                'Pide solo la clasificación como respuesta'
            ]
        },
        'next_lesson': 'few-shot-prompting'
    },

    'few-shot-prompting': {
        'id': 'few-shot-prompting',
        'title': 'Few-Shot Prompting',
        'category': 'techniques',
        'difficulty': 'intermediate',
        'duration': 18,
        'xp_reward': 100,
        'icon': '📝',
        'description': 'Usa ejemplos para guiar al modelo hacia mejores respuestas.',
        'objectives': [
            'Entender el poder de los ejemplos',
            'Crear ejemplos efectivos',
            'Saber cuántos ejemplos usar'
        ],
        'sections': [
            {
                'type': 'text',
                'title': '¿Qué es Few-Shot?',
                'content': '''**Few-Shot Prompting** consiste en dar al modelo algunos ejemplos de la tarea antes de pedirle que la realice.

"Few" significa "pocos" - típicamente entre 2 y 5 ejemplos.

Los ejemplos actúan como una "demostración" de lo que esperas, permitiendo al modelo:
• Entender el formato exacto deseado
• Captar patrones sutiles
• Replicar un estilo específico'''
            },
            {
                'type': 'code',
                'title': 'Estructura Básica',
                'language': 'text',
                'code': '''[Instrucción opcional]

Ejemplo 1:
Entrada: [input 1]
Salida: [output 1]

Ejemplo 2:
Entrada: [input 2]
Salida: [output 2]

Ahora procesa:
Entrada: [tu caso real]
Salida:'''
            },
            {
                'type': 'example',
                'title': 'Few-Shot en Acción',
                'bad_example': {
                    'prompt': 'Convierte a lenguaje formal: "Eso está super cool"',
                    'issue': 'Sin ejemplos, el modelo puede interpretar "formal" de muchas maneras'
                },
                'good_example': {
                    'prompt': '''Convierte expresiones informales a lenguaje formal profesional.

Informal: "Eso está super cool"
Formal: "Eso es sumamente impresionante"

Informal: "No tengo ni idea"
Formal: "Desconozco esa información"

Informal: "Me late mucho tu propuesta"
Formal:''',
                    'why': 'Los ejemplos muestran exactamente el nivel de formalidad esperado'
                }
            },
            {
                'type': 'text',
                'title': 'Cuántos Ejemplos Usar',
                'content': '''La cantidad óptima de ejemplos depende de la complejidad:

• **2-3 ejemplos:** Tareas simples, patrones claros
• **4-5 ejemplos:** Tareas con variaciones importantes
• **6+ ejemplos:** Solo si tienes muchas categorías o casos edge

⚠️ **Más no siempre es mejor:**
• Más ejemplos = más tokens = más costo
• Demasiados ejemplos pueden confundir
• La calidad importa más que la cantidad'''
            },
            {
                'type': 'tip',
                'content': 'Incluye ejemplos diversos que cubran los casos más importantes. Un ejemplo de cada "tipo" de situación es mejor que 5 ejemplos similares.'
            },
            {
                'type': 'text',
                'title': 'Características de Buenos Ejemplos',
                'content': '''**Buenos ejemplos son:**

✅ **Representativos** - Cubren casos típicos
✅ **Diversos** - Muestran variaciones importantes
✅ **Claros** - Sin ambigüedad en entrada/salida
✅ **Consistentes** - Mismo formato en todos
✅ **Correctos** - Verificados y sin errores

**Evita:**
❌ Ejemplos demasiado similares entre sí
❌ Casos extremadamente raros como ejemplos principales
❌ Ejemplos con errores (el modelo los replicará)'''
            },
            {
                'type': 'code',
                'title': 'Ejemplo Completo: Extracción de Datos',
                'language': 'text',
                'code': '''Extrae la información de contacto del siguiente texto.

Texto: "Puedes contactarme al 555-1234 o escribirme a juan@email.com"
Resultado:
- Teléfono: 555-1234
- Email: juan@email.com

Texto: "Mi correo es ana.garcia@empresa.mx"
Resultado:
- Teléfono: No especificado
- Email: ana.garcia@empresa.mx

Texto: "Llámame al celular 555-9876, mi correo ya no lo uso"
Resultado:
- Teléfono: 555-9876
- Email: No especificado

Texto: "Contáctanos en soporte@tienda.com o al 800-123-4567"
Resultado:'''
            }
        ],
        'exercise': {
            'type': 'create_few_shot',
            'instruction': 'Crea un prompt Few-Shot con 3 ejemplos para convertir títulos de artículos a formato SEO-friendly (slug).',
            'test_case': {
                'input': 'Las 10 Mejores Recetas de Verano 2024',
                'expected_output': 'las-10-mejores-recetas-de-verano-2024'
            },
            'hints': [
                'Los slugs usan guiones en lugar de espacios',
                'Todo en minúsculas',
                'Sin caracteres especiales'
            ]
        },
        'next_lesson': 'chain-of-thought'
    },

    'chain-of-thought': {
        'id': 'chain-of-thought',
        'title': 'Chain of Thought (CoT)',
        'category': 'techniques',
        'difficulty': 'intermediate',
        'duration': 20,
        'xp_reward': 120,
        'icon': '🔗',
        'description': 'Mejora el razonamiento del modelo pidiéndole que piense paso a paso.',
        'objectives': [
            'Entender cómo funciona Chain of Thought',
            'Aplicar CoT a problemas complejos',
            'Combinar CoT con otras técnicas'
        ],
        'sections': [
            {
                'type': 'text',
                'title': '¿Qué es Chain of Thought?',
                'content': '''**Chain of Thought (CoT)** es una técnica que mejora el razonamiento del modelo pidiéndole que muestre sus pasos de pensamiento antes de dar una respuesta final.

En lugar de saltar directamente a la respuesta, el modelo "piensa en voz alta", lo que:

• Reduce errores en problemas complejos
• Hace el razonamiento verificable
• Mejora respuestas en matemáticas y lógica
• Ayuda a identificar dónde falla el razonamiento'''
            },
            {
                'type': 'example',
                'title': 'CoT en Acción',
                'bad_example': {
                    'prompt': 'Si tengo 3 manzanas, doy 1 y luego compro 4, ¿cuántas tengo?',
                    'issue': 'El modelo puede dar una respuesta incorrecta al intentar calcular todo de una vez'
                },
                'good_example': {
                    'prompt': 'Si tengo 3 manzanas, doy 1 y luego compro 4, ¿cuántas tengo?\n\nPiensa paso a paso antes de dar la respuesta final.',
                    'why': 'El modelo mostrará: "Empiezo con 3. Doy 1, quedan 2. Compro 4, tengo 2+4=6. Respuesta: 6 manzanas."'
                }
            },
            {
                'type': 'text',
                'title': 'Frases Mágicas para Activar CoT',
                'content': '''Estas frases simples activan el razonamiento paso a paso:

• "Piensa paso a paso"
• "Razona antes de responder"
• "Muestra tu trabajo"
• "Explica tu razonamiento"
• "Vamos a resolver esto paso a paso"
• "Let's think step by step" (funciona incluso en español)

A veces basta con añadir una de estas frases al final de tu prompt.'''
            },
            {
                'type': 'code',
                'title': 'Ejemplo: Problema de Lógica',
                'language': 'text',
                'code': '''Problema: En una carrera, Ana llegó antes que Carlos pero después
de Beatriz. David llegó inmediatamente después de Ana.
¿Quién llegó en tercer lugar?

Resuelve paso a paso:

1. Beatriz llegó antes que Ana → Beatriz está antes que Ana
2. Ana llegó antes que Carlos → Orden: Beatriz → Ana → Carlos
3. David llegó inmediatamente después de Ana → Beatriz → Ana → David → Carlos
4. Tercera posición = David

Respuesta: David llegó en tercer lugar.'''
            },
            {
                'type': 'text',
                'title': 'Cuándo Usar CoT',
                'content': '''**CoT es especialmente útil para:**

✅ Problemas matemáticos
✅ Puzzles de lógica
✅ Razonamiento multi-paso
✅ Análisis de pros y contras
✅ Debugging de código
✅ Toma de decisiones complejas

**Menos útil para:**
❌ Tareas creativas simples
❌ Traducciones directas
❌ Clasificación simple
❌ Generación de contenido breve'''
            },
            {
                'type': 'tip',
                'content': 'CoT puede hacer las respuestas más largas y costosas. Úsalo cuando la precisión importa más que la brevedad.'
            },
            {
                'type': 'text',
                'title': 'Zero-Shot CoT vs Few-Shot CoT',
                'content': '''**Zero-Shot CoT:**
Solo añades "piensa paso a paso" sin ejemplos.
→ Más simple, funciona para problemas claros.

**Few-Shot CoT:**
Das ejemplos que incluyen el razonamiento completo.
→ Más potente, mejor para tareas específicas.

Puedes combinar ambos: dar ejemplos con razonamiento Y pedir que piense paso a paso para el nuevo problema.'''
            }
        ],
        'exercise': {
            'type': 'solve_with_cot',
            'instruction': 'Crea un prompt CoT para resolver: "Un tren sale a las 9:00 y viaja a 80 km/h. Otro tren sale a las 10:00 del mismo punto viajando a 100 km/h en la misma dirección. ¿A qué hora el segundo tren alcanza al primero?"',
            'hints': [
                'Pide que identifique qué información tiene',
                'Solicita que plantee las ecuaciones',
                'Que muestre los cálculos intermedios'
            ]
        },
        'next_lesson': 'role-prompting'
    },

    'role-prompting': {
        'id': 'role-prompting',
        'title': 'Role Prompting',
        'category': 'techniques',
        'difficulty': 'beginner',
        'duration': 14,
        'xp_reward': 70,
        'icon': '🎭',
        'description': 'Asigna roles y personalidades al modelo para mejores respuestas.',
        'objectives': [
            'Entender el impacto de los roles',
            'Elegir roles efectivos',
            'Combinar roles con otras técnicas'
        ],
        'sections': [
            {
                'type': 'text',
                'title': '¿Qué es Role Prompting?',
                'content': '''**Role Prompting** consiste en pedirle al modelo que adopte una identidad, profesión o perspectiva específica antes de responder.

Cuando dices "Actúa como un chef profesional", el modelo:
• Ajusta su vocabulario al dominio
• Considera aspectos que ese rol consideraría
• Responde desde esa experiencia y perspectiva

Es como darle un "disfraz mental" que cambia cómo procesa y responde.'''
            },
            {
                'type': 'example',
                'title': 'Impacto del Rol',
                'bad_example': {
                    'prompt': '¿Qué opinas del café?',
                    'issue': 'Respuesta genérica sin perspectiva definida'
                },
                'good_example': {
                    'prompt': 'Actúa como un barista profesional con 10 años de experiencia. ¿Qué opinas del café instantáneo versus el café de especialidad?',
                    'why': 'Respuesta desde perspectiva experta con detalles técnicos y matices'
                }
            },
            {
                'type': 'text',
                'title': 'Tipos de Roles Efectivos',
                'content': '''**Roles Profesionales:**
• "Actúa como un abogado especializado en..."
• "Eres un médico explicando a un paciente..."
• "Responde como un desarrollador senior de Python..."

**Roles Educativos:**
• "Eres un profesor de primaria..."
• "Actúa como un tutor paciente..."
• "Explica como si fueras un divulgador científico..."

**Roles Creativos:**
• "Eres un copywriter publicitario..."
• "Actúa como un guionista de comedia..."
• "Responde como un poeta romántico..."'''
            },
            {
                'type': 'tip',
                'content': 'Cuanto más específico el rol, mejor. "Experto en marketing" es bueno. "Experto en marketing digital B2B con enfoque en SaaS" es mejor.'
            },
            {
                'type': 'code',
                'title': 'Plantilla de Role Prompting',
                'language': 'text',
                'code': '''Actúa como [ROL ESPECÍFICO] con [AÑOS/NIVEL] de experiencia
en [ÁREA ESPECIALIZADA].

Tu audiencia es [TIPO DE AUDIENCIA].
Tu objetivo es [OBJETIVO ESPECÍFICO].

[INSTRUCCIÓN/PREGUNTA]

Responde [RESTRICCIONES DE FORMATO O TONO].'''
            },
            {
                'type': 'text',
                'title': 'Roles para Diferentes Objetivos',
                'content': '''**Para explicaciones simples:**
→ "Eres un profesor de primaria explicando a niños de 8 años"

**Para análisis técnico:**
→ "Actúa como un ingeniero senior revisando código"

**Para creatividad:**
→ "Eres un director creativo de una agencia top"

**Para empatía:**
→ "Responde como un terapeuta comprensivo y paciente"

**Para rigor:**
→ "Actúa como un científico escéptico que requiere evidencia"'''
            },
            {
                'type': 'text',
                'title': 'Combinando Roles con Otras Técnicas',
                'content': '''Los roles funcionan excelente combinados con:

**Rol + CoT:**
"Actúa como un detective. Analiza estas pistas paso a paso..."

**Rol + Few-Shot:**
"Eres un traductor. Aquí hay ejemplos de mi estilo preferido..."

**Rol + Restricciones:**
"Como editor senior, revisa este texto. Máximo 3 sugerencias, enfócate en claridad."'''
            }
        ],
        'exercise': {
            'type': 'role_design',
            'instruction': 'Diseña un prompt con rol para obtener retroalimentación constructiva sobre una idea de negocio de comida saludable a domicilio.',
            'scenario': 'Quieres feedback honesto pero constructivo, considerando aspectos de mercado, operaciones y diferenciación.',
            'hints': [
                '¿Qué tipo de experto daría el mejor feedback?',
                '¿Qué experiencia específica debería tener?',
                '¿Qué aspectos quieres que evalúe?'
            ]
        },
        'next_lesson': 'self-consistency'
    },

    # ============================================
    # AVANZADO
    # ============================================
    'self-consistency': {
        'id': 'self-consistency',
        'title': 'Self-Consistency',
        'category': 'advanced',
        'difficulty': 'advanced',
        'duration': 15,
        'xp_reward': 100,
        'icon': '🔄',
        'description': 'Mejora la precisión generando múltiples respuestas y encontrando consenso.',
        'objectives': [
            'Entender el concepto de self-consistency',
            'Implementar votación por mayoría',
            'Saber cuándo aplicar esta técnica'
        ],
        'sections': [
            {
                'type': 'text',
                'title': '¿Qué es Self-Consistency?',
                'content': '''**Self-Consistency** es una técnica donde generas múltiples respuestas al mismo problema y eliges la más común o consensuada.

Es como pedir opinión a varios expertos y quedarte con lo que la mayoría dice.

Funciona especialmente bien con Chain of Thought, donde diferentes caminos de razonamiento pueden llegar a la misma respuesta correcta.'''
            },
            {
                'type': 'code',
                'title': 'Proceso de Self-Consistency',
                'language': 'text',
                'code': '''1. Ejecuta el mismo prompt 3-5 veces
2. Recolecta todas las respuestas
3. Identifica la respuesta más frecuente
4. Esa es tu respuesta final

Ejemplo con un problema de matemáticas:
- Ejecución 1: 42 ✓
- Ejecución 2: 42 ✓
- Ejecución 3: 38
- Ejecución 4: 42 ✓
- Ejecución 5: 42 ✓

Respuesta por consenso: 42 (4 de 5)'''
            },
            {
                'type': 'text',
                'title': 'Cuándo Usar Self-Consistency',
                'content': '''**Ideal para:**
✅ Problemas con una respuesta correcta definida
✅ Matemáticas y razonamiento lógico
✅ Clasificación donde hay incertidumbre
✅ Decisiones importantes que requieren alta precisión

**Menos útil para:**
❌ Tareas creativas (no hay "respuesta correcta")
❌ Generación de texto largo
❌ Cuando el costo es una preocupación (múltiples llamadas)'''
            },
            {
                'type': 'tip',
                'content': 'Usa temperature > 0 para obtener variación en las respuestas. Si todas las respuestas son idénticas, self-consistency no aporta valor.'
            }
        ],
        'exercise': {
            'type': 'apply_technique',
            'instruction': 'Describe cómo aplicarías self-consistency para verificar si un código tiene un bug específico.',
            'hints': [
                'Piensa en qué prompt usarías',
                'Cuántas ejecuciones harías',
                'Cómo interpretarías resultados mixtos'
            ]
        },
        'next_lesson': 'prompt-chaining'
    },

    'prompt-chaining': {
        'id': 'prompt-chaining',
        'title': 'Prompt Chaining',
        'category': 'advanced',
        'difficulty': 'advanced',
        'duration': 22,
        'xp_reward': 130,
        'icon': '⛓️',
        'description': 'Divide tareas complejas en cadenas de prompts más simples.',
        'objectives': [
            'Diseñar cadenas de prompts efectivas',
            'Pasar contexto entre prompts',
            'Manejar errores en la cadena'
        ],
        'sections': [
            {
                'type': 'text',
                'title': '¿Qué es Prompt Chaining?',
                'content': '''**Prompt Chaining** consiste en dividir una tarea compleja en una serie de prompts más simples, donde la salida de uno alimenta al siguiente.

Es como una línea de ensamblaje: cada paso hace una parte del trabajo, pasando el resultado al siguiente.

**Ventajas:**
• Cada paso es más simple y confiable
• Puedes verificar resultados intermedios
• Más fácil de debuggear
• Mejor control del proceso'''
            },
            {
                'type': 'code',
                'title': 'Ejemplo: Análisis de Reseña',
                'language': 'text',
                'code': '''# CADENA DE 3 PROMPTS

## Prompt 1: Extracción
"Extrae los puntos principales de esta reseña de producto:
[reseña completa]"

↓ Resultado: Lista de puntos

## Prompt 2: Clasificación
"Clasifica cada punto como positivo, negativo o neutro:
[lista de puntos del paso anterior]"

↓ Resultado: Puntos clasificados

## Prompt 3: Síntesis
"Genera un resumen de una oración basado en estos puntos clasificados:
[puntos clasificados del paso anterior]"

↓ Resultado Final: Resumen conciso'''
            },
            {
                'type': 'text',
                'title': 'Diseñando Cadenas Efectivas',
                'content': '''**Principios clave:**

1. **Cada paso debe tener un objetivo claro**
   No mezcles extracción con análisis en el mismo paso

2. **Salidas estructuradas facilitan el encadenamiento**
   JSON o formatos claros son más fáciles de pasar

3. **Valida entre pasos si es crítico**
   Puedes verificar la salida antes de continuar

4. **Mantén contexto necesario**
   Pasa solo la información relevante, no todo'''
            },
            {
                'type': 'tip',
                'content': 'Una buena regla: si un prompt tiene más de 2 instrucciones principales, considera dividirlo en una cadena.'
            }
        ],
        'exercise': {
            'type': 'design_chain',
            'instruction': 'Diseña una cadena de prompts para: Tomar un artículo largo, resumirlo, traducirlo al inglés, y generar 5 tweets promocionales.',
            'hints': [
                '¿Cuántos pasos necesitas?',
                '¿Qué información pasa de un paso al siguiente?',
                '¿En qué orden tiene más sentido?'
            ]
        },
        'next_lesson': 'meta-prompting'
    },

    # ============================================
    # APLICACIONES
    # ============================================
    'prompts-for-code': {
        'id': 'prompts-for-code',
        'title': 'Prompts para Código',
        'category': 'applications',
        'difficulty': 'intermediate',
        'duration': 25,
        'xp_reward': 110,
        'icon': '💻',
        'description': 'Técnicas específicas para generación y revisión de código.',
        'objectives': [
            'Escribir prompts efectivos para código',
            'Revisar y debuggear con prompts',
            'Documentar código con IA'
        ],
        'sections': [
            {
                'type': 'text',
                'title': 'Principios para Prompts de Código',
                'content': '''Cuando trabajas con código, la precisión es crítica. Los prompts deben ser:

• **Específicos sobre el lenguaje y versión**
• **Claros sobre el contexto** (framework, librerías)
• **Explícitos sobre requisitos** (manejo de errores, tipos)
• **Definidos en estilo** (convenciones de nombrado)'''
            },
            {
                'type': 'code',
                'title': 'Plantilla para Generación de Código',
                'language': 'text',
                'code': '''Escribe una función en [LENGUAJE] que:

Propósito: [descripción clara de qué hace]

Entrada:
- [parámetro 1]: [tipo] - [descripción]
- [parámetro 2]: [tipo] - [descripción]

Salida:
- [tipo de retorno] - [descripción]

Requisitos:
- [requisito 1, ej: manejar errores]
- [requisito 2, ej: ser eficiente para N grande]

Ejemplo de uso:
[ejemplo concreto de input/output esperado]'''
            },
            {
                'type': 'example',
                'title': 'Prompt de Código Efectivo',
                'bad_example': {
                    'prompt': 'Escribe una función para validar emails',
                    'issue': 'Sin lenguaje, sin especificar qué cuenta como válido, sin manejo de errores'
                },
                'good_example': {
                    'prompt': '''Escribe una función en Python 3.10+ que valide direcciones de email.

Requisitos:
- Usar regex para validación básica
- Verificar que el dominio tenga al menos un punto
- Retornar True/False
- Incluir type hints
- Añadir docstring con ejemplos

Ejemplo:
validate_email("user@example.com") → True
validate_email("invalid-email") → False''',
                    'why': 'Lenguaje específico, requisitos claros, ejemplos concretos'
                }
            },
            {
                'type': 'text',
                'title': 'Prompts para Debugging',
                'content': '''Para debuggear código efectivamente:

1. **Incluye el código completo relevante**
2. **Describe el comportamiento esperado vs actual**
3. **Incluye el mensaje de error exacto**
4. **Menciona qué ya intentaste**

Frase útil: "Actúa como un debugger experto. Analiza este código paso a paso y encuentra el bug."'''
            },
            {
                'type': 'code',
                'title': 'Plantilla para Code Review',
                'language': 'text',
                'code': '''Actúa como un senior developer haciendo code review.

Revisa el siguiente código considerando:
1. Bugs potenciales
2. Mejoras de rendimiento
3. Legibilidad y mantenibilidad
4. Seguridad
5. Mejores prácticas de [LENGUAJE]

Código:
```[lenguaje]
[código a revisar]
```

Para cada issue encontrado, indica:
- Línea(s) afectada(s)
- Problema
- Sugerencia de mejora
- Severidad (crítico/importante/menor)'''
            }
        ],
        'exercise': {
            'type': 'code_prompt',
            'instruction': 'Escribe un prompt para generar una función que calcule el factorial de un número, con validación de entrada y manejo de casos edge.',
            'language': 'python',
            'hints': [
                'Especifica el lenguaje y versión',
                'Define qué pasa con números negativos',
                'Menciona si debe ser recursiva o iterativa',
                'Incluye type hints y docstring'
            ]
        },
        'next_lesson': 'prompts-for-writing'
    },

    'prompts-for-writing': {
        'id': 'prompts-for-writing',
        'title': 'Prompts para Escritura',
        'category': 'applications',
        'difficulty': 'intermediate',
        'duration': 20,
        'xp_reward': 90,
        'icon': '✍️',
        'description': 'Mejora tu contenido escrito con prompts especializados.',
        'objectives': [
            'Generar contenido con estilo consistente',
            'Editar y mejorar textos existentes',
            'Adaptar contenido a diferentes audiencias'
        ],
        'sections': [
            {
                'type': 'text',
                'title': 'El Triángulo del Contenido',
                'content': '''Todo contenido escrito tiene tres dimensiones que debes especificar:

**1. Audiencia** - ¿Para quién escribes?
**2. Propósito** - ¿Qué quieres lograr?
**3. Tono** - ¿Cómo debe sentirse?

Especificar estos tres elementos mejora dramáticamente la calidad del contenido generado.'''
            },
            {
                'type': 'code',
                'title': 'Plantilla para Contenido',
                'language': 'text',
                'code': '''Escribe [TIPO DE CONTENIDO] sobre [TEMA].

Audiencia: [descripción del lector ideal]
Propósito: [qué debe pensar/sentir/hacer el lector]
Tono: [formal/casual/técnico/amigable/etc.]
Extensión: [palabras o párrafos]

Estructura:
- [elemento 1, ej: hook inicial]
- [elemento 2, ej: puntos principales]
- [elemento 3, ej: llamada a la acción]

Evitar: [lo que NO debe incluir]'''
            },
            {
                'type': 'text',
                'title': 'Prompts para Edición',
                'content': '''La IA es excelente para mejorar textos existentes:

**Para claridad:**
"Reescribe este párrafo para que sea más claro y directo, manteniendo el mensaje principal."

**Para tono:**
"Ajusta este texto para que suene más [profesional/casual/entusiasta]."

**Para extensión:**
"Condensa este texto a la mitad sin perder información clave."
"Expande este resumen a un artículo completo de 500 palabras."'''
            },
            {
                'type': 'example',
                'title': 'Adaptando a Audiencias',
                'bad_example': {
                    'prompt': 'Explica machine learning',
                    'issue': 'Sin audiencia definida, explicación genérica'
                },
                'good_example': {
                    'prompt': 'Explica qué es machine learning para un gerente de marketing de 45 años que nunca ha trabajado en tecnología pero necesita entender cómo podría beneficiar sus campañas. Usa analogías del mundo del marketing y evita jerga técnica.',
                    'why': 'Audiencia específica, contexto relevante, restricciones claras'
                }
            }
        ],
        'exercise': {
            'type': 'writing_prompt',
            'instruction': 'Crea un prompt para escribir un email de seguimiento después de una entrevista de trabajo, que sea profesional pero memorable.',
            'hints': [
                'Define el tono exacto',
                'Especifica la extensión',
                'Incluye qué elementos debe tener',
                'Menciona qué evitar'
            ]
        },
        'next_lesson': 'prompts-for-analysis'
    }
}

# Función helper para obtener lecciones por categoría
def get_lessons_by_category_data(category_id):
    """Retorna lecciones filtradas por categoría."""
    return [
        lesson for lesson in EMBEDDED_LESSONS.values()
        if lesson.get('category') == category_id
    ]

# Función helper para obtener siguiente lección
def get_next_lesson_id(current_lesson_id):
    """Retorna el ID de la siguiente lección."""
    lesson = EMBEDDED_LESSONS.get(current_lesson_id)
    if lesson:
        return lesson.get('next_lesson')
    return None
