# Assessment Page - Examen Diagnóstico
from browser import html, window
from ..state import get_state

# Preguntas del examen diagnóstico (15 preguntas)
ASSESSMENT_QUESTIONS = [
    # Fundamentos (5 preguntas)
    {
        'id': 1,
        'category': 'fundamentals',
        'question': '¿Qué es un "prompt" en el contexto de IA?',
        'options': [
            'Un tipo de base de datos',
            'Una instrucción o texto que le das a un modelo de IA',
            'Un lenguaje de programación',
            'Un tipo de red neuronal'
        ],
        'correct': 1,
        'explanation': 'Un prompt es el texto o instrucción que envías a un modelo de IA para obtener una respuesta.'
    },
    {
        'id': 2,
        'category': 'fundamentals',
        'question': '¿Por qué es importante ser específico en un prompt?',
        'options': [
            'Para que el modelo procese más rápido',
            'Para obtener respuestas más relevantes y precisas',
            'Para usar menos tokens',
            'No es importante, cualquier prompt funciona igual'
        ],
        'correct': 1,
        'explanation': 'La especificidad ayuda al modelo a entender exactamente qué necesitas, resultando en respuestas más útiles.'
    },
    {
        'id': 3,
        'category': 'fundamentals',
        'question': '¿Qué información es útil incluir como contexto en un prompt?',
        'options': [
            'Solo la pregunta principal',
            'Tu rol, la audiencia, el propósito y restricciones',
            'La fecha y hora actual',
            'Tu nombre y ubicación'
        ],
        'correct': 1,
        'explanation': 'El contexto (rol, audiencia, propósito, restricciones) ayuda al modelo a dar respuestas más apropiadas.'
    },
    {
        'id': 4,
        'category': 'fundamentals',
        'question': '¿Qué significa que un LLM pueda "alucinar"?',
        'options': [
            'Que procesa imágenes',
            'Que genera información falsa o inventada con confianza',
            'Que entiende múltiples idiomas',
            'Que responde muy rápido'
        ],
        'correct': 1,
        'explanation': 'Los LLMs pueden generar información que parece correcta pero es falsa. Siempre verifica datos importantes.'
    },
    {
        'id': 5,
        'category': 'fundamentals',
        'question': '¿Cuál es un buen verbo para iniciar un prompt?',
        'options': [
            '"Intenta"',
            '"Podrías"',
            '"Analiza" o "Resume"',
            '"Tal vez"'
        ],
        'correct': 2,
        'explanation': 'Verbos de acción claros como "Analiza", "Resume", "Compara" dan instrucciones directas al modelo.'
    },

    # Técnicas (5 preguntas)
    {
        'id': 6,
        'category': 'techniques',
        'question': '¿Qué es "Zero-Shot Prompting"?',
        'options': [
            'Un prompt sin ninguna palabra',
            'Pedir una tarea sin dar ejemplos previos',
            'Un prompt que siempre falla',
            'Usar exactamente cero tokens'
        ],
        'correct': 1,
        'explanation': 'Zero-shot significa pedir al modelo que realice una tarea sin proporcionarle ejemplos de cómo hacerla.'
    },
    {
        'id': 7,
        'category': 'techniques',
        'question': '¿Cuándo usarías "Few-Shot Prompting"?',
        'options': [
            'Cuando quieres respuestas cortas',
            'Cuando necesitas un formato o estilo específico',
            'Cuando el modelo es lento',
            'Cuando no tienes internet'
        ],
        'correct': 1,
        'explanation': 'Few-shot es ideal cuando necesitas que el modelo siga un patrón específico, proporcionando 2-5 ejemplos.'
    },
    {
        'id': 8,
        'category': 'techniques',
        'question': '¿Qué técnica usarías para resolver un problema matemático complejo?',
        'options': [
            'Zero-shot',
            'Role prompting',
            'Chain of Thought (pensar paso a paso)',
            'Prompt muy corto'
        ],
        'correct': 2,
        'explanation': 'Chain of Thought hace que el modelo razone paso a paso, mejorando la precisión en problemas complejos.'
    },
    {
        'id': 9,
        'category': 'techniques',
        'question': '¿Qué es "Role Prompting"?',
        'options': [
            'Pedirle al modelo que actúe como un experto específico',
            'Usar emojis en el prompt',
            'Escribir el prompt en mayúsculas',
            'Repetir la misma pregunta varias veces'
        ],
        'correct': 0,
        'explanation': 'Role prompting asigna una identidad al modelo ("Actúa como un experto en X") para obtener respuestas especializadas.'
    },
    {
        'id': 10,
        'category': 'techniques',
        'question': '¿Qué es "Prompt Chaining"?',
        'options': [
            'Escribir prompts muy largos',
            'Dividir tareas complejas en pasos secuenciales',
            'Usar muchos emojis encadenados',
            'Copiar y pegar el mismo prompt'
        ],
        'correct': 1,
        'explanation': 'Prompt chaining divide tareas complejas en pasos, donde la salida de uno alimenta al siguiente.'
    },

    # Claude Code (5 preguntas)
    {
        'id': 11,
        'category': 'claude-code',
        'question': '¿Qué es Claude Code?',
        'options': [
            'Un lenguaje de programación',
            'Una herramienta de IA para programar desde la terminal',
            'Un editor de texto',
            'Una base de datos'
        ],
        'correct': 1,
        'explanation': 'Claude Code es un asistente de IA que te ayuda a programar directamente desde tu terminal.'
    },
    {
        'id': 12,
        'category': 'claude-code',
        'question': '¿Qué comando usarías para instalar Claude Code?',
        'options': [
            'pip install claude',
            'npm install -g @anthropic-ai/claude-code',
            'brew install claude',
            'apt-get install claude'
        ],
        'correct': 1,
        'explanation': 'Claude Code se instala globalmente con npm: npm install -g @anthropic-ai/claude-code'
    },
    {
        'id': 13,
        'category': 'claude-code',
        'question': '¿Qué es un MCP en el contexto de Claude Code?',
        'options': [
            'Un tipo de archivo de código',
            'Un protocolo que da capacidades extra a Claude',
            'Un mensaje de error',
            'Una métrica de rendimiento'
        ],
        'correct': 1,
        'explanation': 'MCP (Model Context Protocol) son plugins que dan superpoderes a Claude, como acceso a GitHub o bases de datos.'
    },
    {
        'id': 14,
        'category': 'claude-code',
        'question': '¿Qué deberías hacer antes de aceptar código generado por Claude Code?',
        'options': [
            'Ejecutarlo inmediatamente',
            'Borrarlo todo',
            'Revisar y entender los cambios propuestos',
            'Ignorar las advertencias'
        ],
        'correct': 2,
        'explanation': 'Siempre revisa el código generado. Tú eres responsable del código final en tu proyecto.'
    },
    {
        'id': 15,
        'category': 'claude-code',
        'question': '¿Cómo le pedirías a Claude Code que explique un error?',
        'options': [
            'Solo diciendo "error"',
            'Pegando el mensaje de error completo incluyendo stack trace',
            'Describiendo el error de memoria',
            'No se puede, hay que buscarlo en Google'
        ],
        'correct': 1,
        'explanation': 'Pegar el error completo con stack trace permite a Claude rastrear exactamente el origen del problema.'
    }
]


def assessment_page(params):
    """Renderiza la página de evaluación diagnóstica."""
    state = get_state()
    container = html.DIV(Class="max-w-3xl mx-auto py-8 px-4")

    # Verificar si ya completó la evaluación
    assessment_data = state.data.get('assessment', {})

    if assessment_data.get('completed'):
        return _render_results(container, assessment_data)

    # Si hay un examen en progreso, continuarlo
    current_question = assessment_data.get('current_question', 0)
    answers = assessment_data.get('answers', {})

    return _render_question(container, current_question, answers)


def _render_question(container, question_idx, answers):
    """Renderiza una pregunta del examen."""
    state = get_state()

    if question_idx >= len(ASSESSMENT_QUESTIONS):
        # Calcular resultados y mostrarlos
        _finish_assessment()
        return container

    question = ASSESSMENT_QUESTIONS[question_idx]
    progress = (question_idx / len(ASSESSMENT_QUESTIONS)) * 100

    # Header
    header = html.DIV(Class="mb-8")
    header <= html.H1("🎯 Evaluación Diagnóstica", Class="text-3xl font-bold text-gray-800 mb-2")
    header <= html.P("Descubre tu nivel actual y recibe recomendaciones personalizadas",
                     Class="text-gray-600")
    container <= header

    # Barra de progreso
    progress_container = html.DIV(Class="mb-8")
    progress_container <= html.DIV(
        f"Pregunta {question_idx + 1} de {len(ASSESSMENT_QUESTIONS)}",
        Class="text-sm text-gray-600 mb-2"
    )
    progress_bar = html.DIV(Class="w-full bg-gray-200 rounded-full h-3")
    progress_fill = html.DIV(
        Class="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full transition-all duration-500",
        style=f"width: {progress}%"
    )
    progress_bar <= progress_fill
    progress_container <= progress_bar
    container <= progress_container

    # Categoría badge
    category_colors = {
        'fundamentals': 'bg-blue-100 text-blue-800',
        'techniques': 'bg-green-100 text-green-800',
        'claude-code': 'bg-purple-100 text-purple-800'
    }
    category_names = {
        'fundamentals': '📚 Fundamentos',
        'techniques': '🎯 Técnicas',
        'claude-code': '🤖 Claude Code'
    }

    # Card de pregunta
    card = html.DIV(Class="bg-white rounded-2xl shadow-lg p-8")

    category_badge = html.SPAN(
        category_names.get(question['category'], question['category']),
        Class=f"inline-block px-3 py-1 rounded-full text-sm font-medium mb-4 {category_colors.get(question['category'], 'bg-gray-100')}"
    )
    card <= category_badge

    card <= html.H2(question['question'], Class="text-xl font-semibold text-gray-800 mb-6")

    # Opciones
    options_container = html.DIV(Class="space-y-3")

    for idx, option in enumerate(question['options']):
        option_id = f"option-{question['id']}-{idx}"

        # Verificar si ya fue seleccionada
        is_selected = answers.get(str(question['id'])) == idx

        option_btn = html.BUTTON(
            Class=f"w-full text-left p-4 rounded-xl border-2 transition-all hover:border-indigo-400 hover:bg-indigo-50 " +
                  ("border-indigo-500 bg-indigo-50" if is_selected else "border-gray-200 bg-white")
        )

        option_content = html.DIV(Class="flex items-center")

        # Radio visual
        radio = html.DIV(
            Class=f"w-5 h-5 rounded-full border-2 mr-4 flex items-center justify-center " +
                  ("border-indigo-500 bg-indigo-500" if is_selected else "border-gray-300")
        )
        if is_selected:
            radio <= html.DIV(Class="w-2 h-2 rounded-full bg-white")

        option_content <= radio
        option_content <= html.SPAN(option, Class="text-gray-700")
        option_btn <= option_content

        def make_handler(opt_idx, q_id):
            def handler(ev):
                _select_answer(q_id, opt_idx)
            return handler

        option_btn.bind('click', make_handler(idx, question['id']))
        options_container <= option_btn

    card <= options_container
    container <= card

    # Botones de navegación
    nav_buttons = html.DIV(Class="flex justify-between mt-6")

    if question_idx > 0:
        prev_btn = html.BUTTON(
            "← Anterior",
            Class="px-6 py-3 text-gray-600 hover:text-gray-800 font-medium"
        )
        prev_btn.bind('click', lambda ev: _go_to_question(question_idx - 1))
        nav_buttons <= prev_btn
    else:
        nav_buttons <= html.DIV()  # Spacer

    # Botón siguiente (solo si hay respuesta)
    if str(question['id']) in answers or answers.get(str(question['id'])) is not None:
        if question_idx < len(ASSESSMENT_QUESTIONS) - 1:
            next_btn = html.BUTTON(
                "Siguiente →",
                Class="px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 font-medium"
            )
            next_btn.bind('click', lambda ev: _go_to_question(question_idx + 1))
        else:
            next_btn = html.BUTTON(
                "Ver Resultados 🎉",
                Class="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 font-medium"
            )
            next_btn.bind('click', lambda ev: _finish_assessment())
        nav_buttons <= next_btn

    container <= nav_buttons

    return container


def _select_answer(question_id, option_idx):
    """Guarda la respuesta seleccionada."""
    state = get_state()
    assessment_data = state.data.get('assessment', {})
    answers = assessment_data.get('answers', {})
    answers[str(question_id)] = option_idx

    assessment_data['answers'] = answers
    state.data['assessment'] = assessment_data
    state.save()

    # Re-render
    from ..router import get_router
    router = get_router()
    router.navigate('assessment')


def _go_to_question(idx):
    """Navega a una pregunta específica."""
    state = get_state()
    assessment_data = state.data.get('assessment', {})
    assessment_data['current_question'] = idx
    state.data['assessment'] = assessment_data
    state.save()

    from ..router import get_router
    router = get_router()
    router.navigate('assessment')


def _finish_assessment():
    """Finaliza el examen y calcula resultados."""
    state = get_state()
    assessment_data = state.data.get('assessment', {})
    answers = assessment_data.get('answers', {})

    # Calcular scores por categoría
    scores = {'fundamentals': 0, 'techniques': 0, 'claude-code': 0}
    totals = {'fundamentals': 0, 'techniques': 0, 'claude-code': 0}

    for q in ASSESSMENT_QUESTIONS:
        category = q['category']
        totals[category] += 1

        user_answer = answers.get(str(q['id']))
        if user_answer == q['correct']:
            scores[category] += 1

    # Calcular porcentajes
    percentages = {}
    for cat in scores:
        if totals[cat] > 0:
            percentages[cat] = int((scores[cat] / totals[cat]) * 100)
        else:
            percentages[cat] = 0

    # Total general
    total_correct = sum(scores.values())
    total_questions = len(ASSESSMENT_QUESTIONS)
    overall_percentage = int((total_correct / total_questions) * 100)

    # Guardar resultados
    assessment_data['completed'] = True
    assessment_data['scores'] = scores
    assessment_data['percentages'] = percentages
    assessment_data['overall'] = overall_percentage
    assessment_data['total_correct'] = total_correct
    assessment_data['completed_at'] = str(window.Date.new().toISOString())

    state.data['assessment'] = assessment_data
    state.save()

    # Dar XP por completar
    from ..gamification.xp import award_xp
    award_xp(state, 'assessment', 50, None, "Completar evaluación diagnóstica")

    from ..router import get_router
    router = get_router()
    router.navigate('assessment')


def _render_results(container, assessment_data):
    """Renderiza los resultados del examen."""
    percentages = assessment_data.get('percentages', {})
    overall = assessment_data.get('overall', 0)

    # Header
    header = html.DIV(Class="text-center mb-8")
    header <= html.H1("📊 Tus Resultados", Class="text-3xl font-bold text-gray-800 mb-2")
    header <= html.P("Basado en tu evaluación, aquí está tu nivel actual", Class="text-gray-600")
    container <= header

    # Score general
    score_card = html.DIV(Class="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 text-white text-center mb-8")
    score_card <= html.DIV(f"{overall}%", Class="text-6xl font-bold mb-2")
    score_card <= html.P("Puntuación General", Class="text-indigo-200")

    # Mensaje según score
    if overall >= 80:
        message = "¡Excelente! Ya tienes bases sólidas. 🌟"
    elif overall >= 60:
        message = "¡Buen inicio! Hay áreas por mejorar. 💪"
    elif overall >= 40:
        message = "Estás aprendiendo. ¡El curso te ayudará mucho! 📚"
    else:
        message = "¡Perfecto para empezar desde cero! 🚀"

    score_card <= html.P(message, Class="mt-4 text-lg")
    container <= score_card

    # Desglose por categoría
    breakdown = html.DIV(Class="bg-white rounded-2xl shadow-lg p-6 mb-8")
    breakdown <= html.H2("Desglose por Área", Class="text-xl font-bold text-gray-800 mb-6")

    categories_info = [
        ('fundamentals', '📚 Fundamentos', 'from-blue-500 to-blue-600'),
        ('techniques', '🎯 Técnicas', 'from-green-500 to-green-600'),
        ('claude-code', '🤖 Claude Code', 'from-purple-500 to-purple-600')
    ]

    for cat_id, cat_name, gradient in categories_info:
        pct = percentages.get(cat_id, 0)

        cat_row = html.DIV(Class="mb-4")
        cat_header = html.DIV(Class="flex justify-between mb-2")
        cat_header <= html.SPAN(cat_name, Class="font-medium text-gray-700")
        cat_header <= html.SPAN(f"{pct}%", Class="font-bold text-gray-800")
        cat_row <= cat_header

        bar_bg = html.DIV(Class="w-full bg-gray-200 rounded-full h-4")
        bar_fill = html.DIV(
            Class=f"bg-gradient-to-r {gradient} h-4 rounded-full transition-all duration-1000",
            style=f"width: {pct}%"
        )
        bar_bg <= bar_fill
        cat_row <= bar_bg

        breakdown <= cat_row

    container <= breakdown

    # Recomendaciones
    recs = html.DIV(Class="bg-white rounded-2xl shadow-lg p-6 mb-8")
    recs <= html.H2("💡 Recomendaciones", Class="text-xl font-bold text-gray-800 mb-4")

    recommendations = []

    if percentages.get('fundamentals', 0) < 60:
        recommendations.append({
            'icon': '📚',
            'title': 'Comienza por Fundamentos',
            'desc': 'Las bases son esenciales. Empieza con las lecciones de conceptos básicos.',
            'link': '#lessons'
        })

    if percentages.get('techniques', 0) < 60:
        recommendations.append({
            'icon': '🎯',
            'title': 'Practica las Técnicas',
            'desc': 'Zero-shot, Few-shot y Chain of Thought son herramientas poderosas.',
            'link': '#practice'
        })

    if percentages.get('claude-code', 0) < 60:
        recommendations.append({
            'icon': '🤖',
            'title': 'Explora Claude Code',
            'desc': 'Aprende a programar con IA directamente en tu terminal.',
            'link': '#lessons'
        })

    if overall >= 60:
        recommendations.append({
            'icon': '✨',
            'title': 'Listo para Practicar',
            'desc': 'Ve al sandbox de práctica para escribir tus propios prompts.',
            'link': '#practice'
        })

    if not recommendations:
        recommendations.append({
            'icon': '🚀',
            'title': '¡Empieza el curso!',
            'desc': 'Estás listo para comenzar. Ve a las lecciones.',
            'link': '#lessons'
        })

    for rec in recommendations:
        rec_card = html.A(
            href=rec['link'],
            Class="block p-4 border border-gray-200 rounded-xl hover:border-indigo-300 hover:bg-indigo-50 transition-all mb-3"
        )
        rec_content = html.DIV(Class="flex items-start gap-4")
        rec_content <= html.SPAN(rec['icon'], Class="text-2xl")
        rec_text = html.DIV()
        rec_text <= html.H3(rec['title'], Class="font-semibold text-gray-800")
        rec_text <= html.P(rec['desc'], Class="text-sm text-gray-600")
        rec_content <= rec_text
        rec_card <= rec_content
        recs <= rec_card

    container <= recs

    # Botones de acción
    actions = html.DIV(Class="flex flex-col sm:flex-row gap-4 justify-center")

    start_btn = html.A(
        "📚 Comenzar Lecciones",
        href="#lessons",
        Class="px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 font-medium text-center"
    )
    actions <= start_btn

    practice_btn = html.A(
        "✍️ Ir a Práctica",
        href="#practice",
        Class="px-6 py-3 border-2 border-indigo-600 text-indigo-600 rounded-xl hover:bg-indigo-50 font-medium text-center"
    )
    actions <= practice_btn

    retake_btn = html.BUTTON(
        "🔄 Repetir Evaluación",
        Class="px-6 py-3 text-gray-600 hover:text-gray-800 font-medium"
    )
    retake_btn.bind('click', _reset_assessment)
    actions <= retake_btn

    container <= actions

    return container


def _reset_assessment(ev):
    """Reinicia la evaluación."""
    state = get_state()
    state.data['assessment'] = {}
    state.save()

    from ..router import get_router
    router = get_router()
    router.navigate('assessment')
