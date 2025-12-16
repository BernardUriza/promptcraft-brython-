# PromptCraft - Login Page Component

from browser import document, window
from brython_modules.api_client import login, TokenManager
from brython_modules.websocket_client import connect_websocket


def render_login_page(container_id="app"):
    """Render the login page."""
    container = document.getElementById(container_id)
    if not container:
        return

    container.innerHTML = """
    <div class="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center p-4">
        <div class="max-w-md w-full">
            <!-- Logo -->
            <div class="text-center mb-8">
                <div class="text-6xl mb-4">🎯</div>
                <h1 class="text-3xl font-bold text-white">PromptCraft</h1>
                <p class="text-purple-200 mt-2">Master the art of prompt engineering</p>
            </div>

            <!-- Login Card -->
            <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
                <h2 class="text-2xl font-bold text-white mb-6 text-center">Welcome Back</h2>

                <!-- Error Message -->
                <div id="login-error" class="hidden bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-4">
                    <span id="login-error-text"></span>
                </div>

                <!-- Login Form -->
                <form id="login-form" class="space-y-4">
                    <div>
                        <label class="block text-purple-200 text-sm font-medium mb-2">Email</label>
                        <input
                            type="email"
                            id="login-email"
                            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="you@example.com"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-purple-200 text-sm font-medium mb-2">Password</label>
                        <input
                            type="password"
                            id="login-password"
                            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="••••••••"
                            required
                        >
                    </div>

                    <div class="flex items-center justify-between">
                        <label class="flex items-center">
                            <input type="checkbox" id="remember-me" class="w-4 h-4 rounded border-white/20 bg-white/10 text-purple-500 focus:ring-purple-500">
                            <span class="ml-2 text-sm text-purple-200">Remember me</span>
                        </label>
                        <a href="#" class="text-sm text-purple-300 hover:text-white transition-colors">Forgot password?</a>
                    </div>

                    <button
                        type="submit"
                        id="login-submit"
                        class="w-full py-3 px-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-purple-900 transition-all disabled:opacity-50"
                    >
                        Sign In
                    </button>
                </form>

                <!-- Register Link -->
                <div class="mt-6 text-center">
                    <p class="text-purple-200">
                        Don't have an account?
                        <a href="#" id="goto-register" class="text-white font-semibold hover:underline">Sign up</a>
                    </p>
                </div>

                <!-- Social Login -->
                <div class="mt-6">
                    <div class="relative">
                        <div class="absolute inset-0 flex items-center">
                            <div class="w-full border-t border-white/20"></div>
                        </div>
                        <div class="relative flex justify-center text-sm">
                            <span class="px-2 bg-transparent text-purple-300">Or continue with</span>
                        </div>
                    </div>

                    <div class="mt-4 grid grid-cols-2 gap-4">
                        <button class="flex items-center justify-center px-4 py-2 border border-white/20 rounded-lg text-white hover:bg-white/10 transition-colors">
                            <span class="mr-2">🔗</span> Google
                        </button>
                        <button class="flex items-center justify-center px-4 py-2 border border-white/20 rounded-lg text-white hover:bg-white/10 transition-colors">
                            <span class="mr-2">🐱</span> GitHub
                        </button>
                    </div>
                </div>
            </div>

            <!-- Demo Account -->
            <div class="mt-4 text-center">
                <button id="demo-login" class="text-purple-300 text-sm hover:text-white transition-colors">
                    Try demo account
                </button>
            </div>
        </div>
    </div>
    """

    # Setup event handlers
    setup_login_handlers()


def setup_login_handlers():
    """Setup login form event handlers."""
    form = document.getElementById("login-form")
    register_link = document.getElementById("goto-register")
    demo_btn = document.getElementById("demo-login")

    def handle_submit(event):
        event.preventDefault()

        email = document.getElementById("login-email").value
        password = document.getElementById("login-password").value
        submit_btn = document.getElementById("login-submit")
        error_div = document.getElementById("login-error")
        error_text = document.getElementById("login-error-text")

        # Validate
        if not email or not password:
            error_div.classList.remove("hidden")
            error_text.textContent = "Please enter email and password"
            return

        # Disable button
        submit_btn.disabled = True
        submit_btn.textContent = "Signing in..."

        def on_success(data):
            submit_btn.disabled = False
            submit_btn.textContent = "Sign In"

            # Connect WebSocket
            connect_websocket()

            # Redirect to dashboard
            window.location.hash = "#/dashboard"

        def on_error(status, message):
            submit_btn.disabled = False
            submit_btn.textContent = "Sign In"
            error_div.classList.remove("hidden")
            error_text.textContent = message

        login(email, password, on_success=on_success, on_error=on_error)

    def goto_register(event):
        event.preventDefault()
        window.location.hash = "#/register"

    def demo_login(event):
        event.preventDefault()
        document.getElementById("login-email").value = "demo@promptcraft.com"
        document.getElementById("login-password").value = "Demo123!"

    form.bind("submit", handle_submit)
    register_link.bind("click", goto_register)
    demo_btn.bind("click", demo_login)
