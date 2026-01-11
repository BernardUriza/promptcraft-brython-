# Claude Code Exercises - Ejercicios Interactivos de Claude Code
from browser import html, document
from ..state import get_state

# Ejercicios tipo "¿Qué comando usarías?"
CLAUDE_EXERCISES = [
    {
        'id': 'claude-ex-1',
        'title': 'Entender código existente',
        'scenario': 'Acabas de unirte a un proyecto y hay un archivo `auth_handler.py` que no entiendes.',
        'question': '¿Cómo le pedirías a Claude Code que te explique este archivo?',
        'options': [
            {'text': '"Explica auth_handler.py"', 'correct': True, 'feedback': '¡Correcto! Claude leerá el archivo y te dará una explicación clara.'},
            {'text': '"¿Qué es auth?"', 'correct': False, 'feedback': 'Muy vago. Claude no sabría a qué archivo te refieres.'},
            {'text': 'Buscar en Google primero', 'correct': False, 'feedback': 'Claude Code puede leer TU código específico, no código genérico de internet.'},
            {'text': '"cat auth_handler.py"', 'correct': False, 'feedback': 'Esto solo mostraría el código, no lo explicaría.'}
        ],
        'xp': 15
    },
    {
        'id': 'claude-ex-2',
        'title': 'Agregar una función',
        'scenario': 'Necesitas agregar validación de contraseña en `utils/validators.py`.',
        'question': '¿Cuál es la mejor forma de pedirle esto a Claude?',
        'options': [
            {'text': '"Agrega validación de contraseña"', 'correct': False, 'feedback': 'Falta especificar dónde y los requisitos de la validación.'},
            {'text': '"En utils/validators.py, agrega una función validate_password que verifique: mínimo 8 caracteres, al menos una mayúscula y un número"', 'correct': True, 'feedback': '¡Perfecto! Específico sobre archivo, función y requisitos.'},
            {'text': '"Necesito validar passwords"', 'correct': False, 'feedback': 'Muy vago. ¿Dónde? ¿Qué criterios?'},
            {'text': '"Crea un nuevo archivo para passwords"', 'correct': False, 'feedback': 'El archivo ya existe. Mejor agregar a la estructura existente.'}
        ],
        'xp': 15
    },
    {
        'id': 'claude-ex-3',
        'title': 'Debuggear un error',
        'scenario': 'Tu código lanza: `KeyError: \'user_id\' at line 42 in api.py`',
        'question': '¿Cómo le pides ayuda a Claude?',
        'options': [
            {'text': '"Mi código no funciona"', 'correct': False, 'feedback': 'Muy vago. ¿Qué error? ¿Dónde?'},
            {'text': '"Tengo un KeyError"', 'correct': False, 'feedback': 'Falta el mensaje completo y contexto.'},
            {'text': 'Pegar el error completo: "En api.py línea 42 tengo KeyError: \'user_id\'. El código intenta acceder a datos de una API. ¿Por qué falla?"', 'correct': True, 'feedback': '¡Excelente! Error completo + ubicación + contexto = diagnóstico preciso.'},
            {'text': '"Arréglalo"', 'correct': False, 'feedback': 'Claude no es mago, necesita saber QUÉ arreglar.'}
        ],
        'xp': 15
    },
    {
        'id': 'claude-ex-4',
        'title': 'Refactorizar código',
        'scenario': 'Tienes una función de 100 líneas que hace demasiadas cosas.',
        'question': '¿Cuál es el mejor approach?',
        'options': [
            {'text': '"Refactoriza todo el proyecto"', 'correct': False, 'feedback': 'Demasiado amplio. Empieza por una cosa.'},
            {'text': '"Esta función es muy larga"', 'correct': False, 'feedback': 'Observación, no instrucción.'},
            {'text': '"Explica qué hace process_data() en handlers.py. Luego sugiere cómo dividirla en funciones más pequeñas y específicas"', 'correct': True, 'feedback': '¡Correcto! Primero entender, luego refactorizar paso a paso.'},
            {'text': '"Borra process_data y escríbela de nuevo"', 'correct': False, 'feedback': 'Riesgoso. Mejor mejorar incrementalmente.'}
        ],
        'xp': 15
    },
    {
        'id': 'claude-ex-5',
        'title': 'Escribir tests',
        'scenario': 'Acabas de crear `calculate_discount()` y necesitas asegurar que funciona.',
        'question': '¿Cómo le pides a Claude que escriba tests?',
        'options': [
            {'text': '"Escribe tests"', 'correct': False, 'feedback': '¿Para qué función? ¿Qué casos?'},
            {'text': '"Escribe tests unitarios para calculate_discount() en pricing.py. Incluye casos: descuento normal, 0%, 100%, y valores inválidos"', 'correct': True, 'feedback': '¡Perfecto! Función específica + casos de prueba claros.'},
            {'text': '"¿Funciona calculate_discount?"', 'correct': False, 'feedback': 'Esto pide verificación manual, no tests automatizados.'},
            {'text': '"Agrega pytest al proyecto"', 'correct': False, 'feedback': 'Instalación, no tests específicos.'}
        ],
        'xp': 15
    },
    {
        'id': 'claude-ex-6',
        'title': 'Revisar antes de aceptar',
        'scenario': 'Claude propone cambiar 15 archivos para implementar una feature.',
        'question': '¿Qué deberías hacer?',
        'options': [
            {'text': 'Aceptar todo inmediatamente - Claude sabe lo que hace', 'correct': False, 'feedback': '¡Nunca! Siempre revisa. Eres responsable del código.'},
            {'text': 'Revisar cada archivo, entender los cambios, y aceptar solo si tienen sentido', 'correct': True, 'feedback': '¡Correcto! Tú eres el dueño del código. Claude es asistente, no jefe.'},
            {'text': 'Rechazar todo - 15 archivos es demasiado', 'correct': False, 'feedback': 'La cantidad no importa, la calidad sí. Revisa primero.'},
            {'text': 'Pedir que lo haga en menos archivos', 'correct': False, 'feedback': 'A veces 15 archivos es correcto. Lo importante es revisar.'}
        ],
        'xp': 20
    },
    {
        'id': 'claude-ex-7',
        'title': 'Instalar MCP de GitHub',
        'scenario': 'Quieres que Claude pueda crear issues en tu repositorio.',
        'question': '¿Qué necesitas configurar?',
        'options': [
            {'text': 'Darle tu contraseña de GitHub', 'correct': False, 'feedback': '¡Nunca compartas contraseñas! Los MCPs usan tokens.'},
            {'text': 'Configurar el GitHub MCP en claude_desktop_config.json con tu token de acceso', 'correct': True, 'feedback': '¡Correcto! Los MCPs se configuran en el archivo de config con tokens específicos.'},
            {'text': 'No se puede, Claude no accede a GitHub', 'correct': False, 'feedback': '¡Sí puede! Con el MCP de GitHub configurado.'},
            {'text': 'Instalar una extensión del navegador', 'correct': False, 'feedback': 'Claude Code es de terminal, no de navegador.'}
        ],
        'xp': 20
    },
    {
        'id': 'claude-ex-8',
        'title': 'Trabajar en equipo',
        'scenario': 'Tu compañero hizo cambios y ahora tu código tiene conflictos de merge.',
        'question': '¿Cómo usarías Claude Code para resolverlos?',
        'options': [
            {'text': '"Arregla los conflictos"', 'correct': False, 'feedback': 'Claude necesita ver los conflictos específicos.'},
            {'text': '"Hay conflictos de merge en user_service.py entre mi versión y main. Muéstrame las diferencias y sugiere cómo resolver manteniendo ambas funcionalidades"', 'correct': True, 'feedback': '¡Excelente! Contexto del conflicto + pedir análisis + criterio de resolución.'},
            {'text': 'Hacer git reset --hard', 'correct': False, 'feedback': '¡Perderías tus cambios! Resolver > resetear.'},
            {'text': 'Esperar a que el compañero lo arregle', 'correct': False, 'feedback': 'Es tu responsabilidad resolver conflictos en tu branch.'}
        ],
        'xp': 20
    },
    {
        'id': 'claude-ex-9',
        'title': 'Documentar código',
        'scenario': 'Tu función `process_payment()` funciona pero no tiene documentación.',
        'question': '¿Cómo le pides a Claude que la documente?',
        'options': [
            {'text': '"Documenta"', 'correct': False, 'feedback': '¿Qué función? ¿Qué estilo de documentación?'},
            {'text': '"Agrega docstring a process_payment() en payments.py. Incluye descripción, parámetros, return value, y posibles excepciones. Sigue el estilo Google docstring"', 'correct': True, 'feedback': '¡Perfecto! Función + qué incluir + estilo específico.'},
            {'text': '"Agrega comentarios al código"', 'correct': False, 'feedback': 'Comentarios inline ≠ documentación de API.'},
            {'text': '"Escribe un README"', 'correct': False, 'feedback': 'README es para el proyecto, docstrings son para funciones.'}
        ],
        'xp': 15
    },
    {
        'id': 'claude-ex-10',
        'title': 'Crear proyecto nuevo',
        'scenario': 'Quieres empezar un proyecto Python para una API REST.',
        'question': '¿Cuál es el mejor primer paso con Claude Code?',
        'options': [
            {'text': '"Crea una API"', 'correct': False, 'feedback': 'Muy vago. ¿Qué framework? ¿Qué endpoints?'},
            {'text': '"Inicializa un proyecto Python con FastAPI. Crea la estructura de carpetas, requirements.txt con las dependencias básicas, y un endpoint de health check"', 'correct': True, 'feedback': '¡Excelente! Framework + estructura + primer endpoint funcional.'},
            {'text': '"¿Cuál es el mejor framework para APIs?"', 'correct': False, 'feedback': 'Pregunta válida, pero no avanza el proyecto.'},
            {'text': 'Copiar código de un tutorial', 'correct': False, 'feedback': 'Claude puede crear código específico para TU proyecto.'}
        ],
        'xp': 20
    }
]


def claude_exercises_page(params):
    """Renderiza la página de ejercicios de Claude Code."""
    state = get_state()
    container = html.DIV(Class="max-w-4xl mx-auto py-8 px-4")

    # Header
    header = html.DIV(Class="mb-8")
    header <= html.H1("🤖 Ejercicios de Claude Code", Class="text-3xl font-bold text-gray-800 mb-2")
    header <= html.P("Practica situaciones reales que encontrarás al usar Claude Code",
                     Class="text-gray-600")
    container <= header

    # Progreso
    exercise_data = state.data.get('claude_exercises', {})
    completed = exercise_data.get('completed', [])
    total = len(CLAUDE_EXERCISES)
    done = len(completed)
    total_xp = sum(ex['xp'] for ex in CLAUDE_EXERCISES if ex['id'] in completed)

    progress_card = html.DIV(Class="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl p-6 text-white mb-8")

    progress_stats = html.DIV(Class="flex justify-between items-center mb-4")
    progress_stats <= html.DIV(html.SPAN(f"{done}/{total}", Class="text-3xl font-bold") +
                               html.SPAN(" ejercicios completados", Class="ml-2 text-purple-200"))
    progress_stats <= html.DIV(html.SPAN(f"+{total_xp}", Class="text-2xl font-bold") +
                               html.SPAN(" XP", Class="ml-1 text-purple-200"))
    progress_card <= progress_stats

    progress_bar = html.DIV(Class="w-full bg-purple-400 bg-opacity-50 rounded-full h-3")
    pct = (done / total * 100) if total > 0 else 0
    progress_bar <= html.DIV(Class="bg-white h-3 rounded-full", style=f"width: {pct}%")
    progress_card <= progress_bar

    container <= progress_card

    # Lista de ejercicios
    for i, exercise in enumerate(CLAUDE_EXERCISES):
        is_completed = exercise['id'] in completed
        is_current = i == done and not is_completed

        card = html.DIV(
            Class=f"bg-white rounded-xl shadow-sm border-2 p-6 mb-4 transition-all " +
                  (("border-green-300" if is_completed else "border-indigo-400 ring-2 ring-indigo-200") if is_current or is_completed else "border-gray-100")
        )

        # Header
        card_header = html.DIV(Class="flex items-center justify-between mb-3")

        title_section = html.DIV(Class="flex items-center gap-3")
        number_badge = html.SPAN(
            f"#{i+1}",
            Class=f"w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold " +
                  ("bg-green-100 text-green-700" if is_completed else
                   "bg-indigo-100 text-indigo-700" if is_current else "bg-gray-100 text-gray-500")
        )
        title_section <= number_badge
        title_section <= html.H3(exercise['title'], Class="font-semibold text-gray-800")
        card_header <= title_section

        if is_completed:
            card_header <= html.SPAN("✅", Class="text-2xl")
        else:
            card_header <= html.SPAN(f"+{exercise['xp']} XP", Class="text-sm text-indigo-600 font-medium")

        card <= card_header

        # Escenario
        card <= html.P(exercise['scenario'], Class="text-gray-600 text-sm mb-4")

        # Botón
        if is_completed:
            btn = html.BUTTON("Repetir →", Class="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200")
        elif is_current:
            btn = html.BUTTON("Resolver →", Class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium")
        else:
            btn = html.BUTTON("Bloqueado 🔒", Class="px-4 py-2 bg-gray-100 text-gray-400 rounded-lg cursor-not-allowed",
                              disabled=True)

        def make_handler(ex_id, locked):
            def handler(ev):
                if not locked:
                    from ..router import get_router
                    get_router().navigate(f'claude-exercise/{ex_id}')
            return handler

        if not (not is_completed and not is_current):  # Si no está bloqueado
            btn.bind('click', make_handler(exercise['id'], False))

        card <= btn
        container <= card

    return container


def claude_exercise_detail_page(params):
    """Renderiza un ejercicio individual de Claude Code."""
    state = get_state()
    exercise_id = params.get('id', '')

    # Buscar ejercicio
    exercise = None
    for ex in CLAUDE_EXERCISES:
        if ex['id'] == exercise_id:
            exercise = ex
            break

    if not exercise:
        container = html.DIV(Class="max-w-3xl mx-auto py-8 px-4")
        container <= html.H1("Ejercicio no encontrado", Class="text-2xl text-gray-800")
        return container

    container = html.DIV(Class="max-w-3xl mx-auto py-8 px-4")

    # Back button
    back_btn = html.A("← Volver a Ejercicios", href="#claude-exercises",
                      Class="text-indigo-600 hover:text-indigo-800 mb-4 inline-block")
    container <= back_btn

    # Header
    header = html.DIV(Class="mb-6")
    header <= html.H1(exercise['title'], Class="text-2xl font-bold text-gray-800 mb-2")
    header <= html.SPAN(f"+{exercise['xp']} XP", Class="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium")
    container <= header

    # Escenario
    scenario_card = html.DIV(Class="bg-purple-50 border border-purple-200 rounded-xl p-4 mb-6")
    scenario_card <= html.H3("📋 Situación", Class="font-semibold text-purple-800 mb-2")
    scenario_card <= html.P(exercise['scenario'], Class="text-purple-700")
    container <= scenario_card

    # Pregunta
    question_card = html.DIV(Class="bg-white border border-gray-200 rounded-xl p-6 mb-6")
    question_card <= html.H3("🤔 " + exercise['question'], Class="font-semibold text-gray-800 mb-6")

    # Opciones
    options_container = html.DIV(Class="space-y-3", id="options-container")

    for idx, option in enumerate(exercise['options']):
        option_btn = html.BUTTON(
            Class="w-full text-left p-4 rounded-xl border-2 border-gray-200 hover:border-indigo-400 hover:bg-indigo-50 transition-all",
            id=f"option-{idx}"
        )
        option_btn <= html.P(option['text'], Class="text-gray-700")

        def make_handler(opt_idx, opt_data, ex):
            def handler(ev):
                _handle_answer(opt_idx, opt_data, ex)
            return handler

        option_btn.bind('click', make_handler(idx, option, exercise))
        options_container <= option_btn

    question_card <= options_container
    container <= question_card

    # Área de feedback
    feedback_area = html.DIV(id="exercise-feedback")
    container <= feedback_area

    return container


def _handle_answer(option_idx, option_data, exercise):
    """Maneja la selección de una respuesta."""
    state = get_state()

    # Marcar la opción seleccionada
    for i in range(len(exercise['options'])):
        btn = document.getElementById(f"option-{i}")
        if btn:
            btn.classList.remove("border-green-500", "bg-green-50", "border-red-500", "bg-red-50", "border-indigo-500")
            btn.classList.add("border-gray-200")

    selected_btn = document.getElementById(f"option-{option_idx}")
    if selected_btn:
        if option_data['correct']:
            selected_btn.classList.remove("border-gray-200")
            selected_btn.classList.add("border-green-500", "bg-green-50")
        else:
            selected_btn.classList.remove("border-gray-200")
            selected_btn.classList.add("border-red-500", "bg-red-50")

    # Mostrar feedback
    feedback_area = document.getElementById("exercise-feedback")
    feedback_area.innerHTML = ""

    feedback_card = html.DIV(
        Class=f"rounded-xl p-4 mb-4 " +
              ("bg-green-100 border border-green-300" if option_data['correct'] else "bg-red-100 border border-red-300")
    )

    icon = "✅" if option_data['correct'] else "❌"
    feedback_card <= html.P(f"{icon} {option_data['feedback']}",
                            Class=f"font-medium " + ("text-green-800" if option_data['correct'] else "text-red-800"))

    feedback_area <= feedback_card

    # Si es correcto, guardar y dar XP
    if option_data['correct']:
        exercise_data = state.data.get('claude_exercises', {})
        completed = exercise_data.get('completed', [])

        if exercise['id'] not in completed:
            completed.append(exercise['id'])
            exercise_data['completed'] = completed
            state.data['claude_exercises'] = exercise_data
            state.save()

            # Dar XP
            from ..gamification.xp import award_xp
            award_xp(state, 'claude_exercise', exercise['xp'], None, f"Ejercicio Claude Code: {exercise['title']}")

            xp_msg = html.DIV(Class="bg-indigo-100 border border-indigo-300 rounded-xl p-4 text-center")
            xp_msg <= html.P(f"🎉 +{exercise['xp']} XP ganados", Class="text-indigo-800 font-bold")
            feedback_area <= xp_msg

        # Botón siguiente
        next_btn = html.A(
            "Siguiente ejercicio →",
            href="#claude-exercises",
            Class="inline-block mt-4 px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 font-medium"
        )
        feedback_area <= next_btn

    else:
        # Mostrar cuál era la correcta
        for i, opt in enumerate(exercise['options']):
            if opt['correct']:
                correct_btn = document.getElementById(f"option-{i}")
                if correct_btn:
                    correct_btn.classList.remove("border-gray-200")
                    correct_btn.classList.add("border-green-500")

        retry_btn = html.BUTTON(
            "Intentar de nuevo",
            Class="mt-4 px-6 py-3 bg-gray-600 text-white rounded-xl hover:bg-gray-700 font-medium"
        )

        def retry(ev):
            from ..router import get_router
            get_router().navigate(f'claude-exercise/{exercise["id"]}')

        retry_btn.bind('click', retry)
        feedback_area <= retry_btn
