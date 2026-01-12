# PromptCraft - Guides Page
# Página de guías de inicio

from browser import document, html, window


def guides_page(params):
    """
    Renderiza la página de guías.
    Muestra las guías disponibles para diferentes niveles de usuario.
    """
    container = html.DIV(Class="space-y-8")

    # Header
    header = html.DIV(Class="text-center mb-8")
    header <= html.H1(
        html.SPAN("📖", Class="mr-3") + "Guías de Inicio",
        Class="text-3xl font-bold text-gray-800 mb-2"
    )
    header <= html.P(
        "Recursos para comenzar tu aprendizaje según tu nivel de experiencia.",
        Class="text-gray-600 max-w-2xl mx-auto"
    )
    container <= header

    # Guías Grid
    guides_grid = html.DIV(Class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto")

    # Guía para principiantes
    beginner_guide = _create_guide_card(
        icon="🌱",
        title="Guía para Principiantes",
        subtitle="¿Nuevo en IA?",
        description="Aprende qué es la Inteligencia Artificial, cómo usar ChatGPT, Claude y Gemini, y descubre cómo ganar dinero con estas herramientas.",
        features=[
            "Introducción a la IA",
            "Uso de ChatGPT, Claude y Gemini",
            "Cómo monetizar tus habilidades",
            "Primeros pasos prácticos"
        ],
        button_text="Ver Guía de Principiantes →",
        url="guia.html",
        color_scheme="green"
    )
    guides_grid <= beginner_guide

    # Guía técnica avanzada
    advanced_guide = _create_guide_card(
        icon="🚀",
        title="Guía Técnica Avanzada",
        subtitle="¿Ya programas?",
        description="Aprende a usar GitHub, hacer fork del proyecto, configurar Claude Code y trabajar con MCPs (Model Context Protocols).",
        features=[
            "Configuración de GitHub",
            "Fork y personalización",
            "Claude Code desde terminal",
            "MCPs y extensiones"
        ],
        button_text="Ver Guía Técnica →",
        url="guia-claude-code.html",
        color_scheme="purple"
    )
    guides_grid <= advanced_guide

    container <= guides_grid

    # Sección de ayuda adicional
    help_section = _create_help_section()
    container <= help_section

    return container


def _create_guide_card(icon, title, subtitle, description, features, button_text, url, color_scheme):
    """Crea una tarjeta de guía."""

    # Definir colores según el esquema
    colors = {
        "green": {
            "bg": "bg-green-50",
            "border": "border-green-200",
            "icon_bg": "bg-green-100",
            "icon_text": "text-green-600",
            "button": "bg-green-600 hover:bg-green-700",
            "check": "text-green-500"
        },
        "purple": {
            "bg": "bg-purple-50",
            "border": "border-purple-200",
            "icon_bg": "bg-purple-100",
            "icon_text": "text-purple-600",
            "button": "bg-purple-600 hover:bg-purple-700",
            "check": "text-purple-500"
        }
    }

    c = colors.get(color_scheme, colors["green"])

    card = html.DIV(Class=f"rounded-2xl border-2 {c['border']} {c['bg']} p-6 hover:shadow-lg transition-shadow")

    # Header con icono
    card_header = html.DIV(Class="flex items-start gap-4 mb-4")

    icon_div = html.DIV(
        html.SPAN(icon, Class="text-3xl"),
        Class=f"w-14 h-14 {c['icon_bg']} rounded-xl flex items-center justify-center"
    )
    card_header <= icon_div

    title_div = html.DIV()
    title_div <= html.H3(title, Class="text-xl font-bold text-gray-800")
    title_div <= html.SPAN(subtitle, Class=f"text-sm {c['icon_text']} font-medium")
    card_header <= title_div

    card <= card_header

    # Descripción
    card <= html.P(description, Class="text-gray-600 mb-4")

    # Features list
    features_list = html.UL(Class="space-y-2 mb-6")
    for feature in features:
        features_list <= html.LI(
            html.SPAN("✓", Class=f"{c['check']} mr-2 font-bold") +
            html.SPAN(feature, Class="text-gray-700"),
            Class="flex items-center text-sm"
        )
    card <= features_list

    # Botón
    button = html.A(
        button_text,
        href=url,
        target="_blank",
        Class=f"block text-center py-3 px-6 {c['button']} text-white rounded-lg font-medium transition-colors"
    )
    card <= button

    return card


def _create_help_section():
    """Crea la sección de ayuda adicional."""
    section = html.DIV(Class="bg-white rounded-xl border border-gray-200 p-6 max-w-4xl mx-auto mt-8")

    section <= html.H2(
        html.SPAN("💡", Class="mr-2") + "¿No sabes cuál elegir?",
        Class="text-xl font-bold text-gray-800 mb-4"
    )

    help_grid = html.DIV(Class="grid grid-cols-1 md:grid-cols-2 gap-4")

    # Opción principiante
    opt1 = html.DIV(Class="p-4 bg-gray-50 rounded-lg")
    opt1 <= html.P(
        html.STRONG("Elige la Guía de Principiantes si:"),
        Class="text-gray-800 mb-2"
    )
    opt1 <= html.UL(
        html.LI("• Nunca has usado ChatGPT o Claude", Class="text-gray-600 text-sm") +
        html.LI("• No sabes qué es un 'prompt'", Class="text-gray-600 text-sm") +
        html.LI("• Quieres aprender desde cero", Class="text-gray-600 text-sm"),
        Class="space-y-1"
    )
    help_grid <= opt1

    # Opción avanzada
    opt2 = html.DIV(Class="p-4 bg-gray-50 rounded-lg")
    opt2 <= html.P(
        html.STRONG("Elige la Guía Técnica si:"),
        Class="text-gray-800 mb-2"
    )
    opt2 <= html.UL(
        html.LI("• Ya usas Git/GitHub", Class="text-gray-600 text-sm") +
        html.LI("• Sabes usar la terminal", Class="text-gray-600 text-sm") +
        html.LI("• Quieres personalizar PromptCraft", Class="text-gray-600 text-sm"),
        Class="space-y-1"
    )
    help_grid <= opt2

    section <= help_grid

    return section
