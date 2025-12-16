# PromptCraft - Register Page Component

from browser import document, window
from brython_modules.api_client import register
from brython_modules.websocket_client import connect_websocket


def render_register_page(container_id="app"):
    """Render the registration page."""
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
                <p class="text-purple-200 mt-2">Start your prompt engineering journey</p>
            </div>

            <!-- Register Card -->
            <div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
                <h2 class="text-2xl font-bold text-white mb-6 text-center">Create Account</h2>

                <!-- Error Message -->
                <div id="register-error" class="hidden bg-red-500/20 border border-red-500 text-red-200 px-4 py-3 rounded-lg mb-4">
                    <span id="register-error-text"></span>
                </div>

                <!-- Success Message -->
                <div id="register-success" class="hidden bg-green-500/20 border border-green-500 text-green-200 px-4 py-3 rounded-lg mb-4">
                    <span id="register-success-text"></span>
                </div>

                <!-- Register Form -->
                <form id="register-form" class="space-y-4">
                    <div>
                        <label class="block text-purple-200 text-sm font-medium mb-2">Username</label>
                        <input
                            type="text"
                            id="register-username"
                            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="johndoe"
                            pattern="[a-zA-Z0-9_-]+"
                            minlength="3"
                            maxlength="50"
                            required
                        >
                        <p class="mt-1 text-xs text-purple-300">Letters, numbers, underscores, and hyphens only</p>
                    </div>

                    <div>
                        <label class="block text-purple-200 text-sm font-medium mb-2">Email</label>
                        <input
                            type="email"
                            id="register-email"
                            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="you@example.com"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-purple-200 text-sm font-medium mb-2">Display Name (optional)</label>
                        <input
                            type="text"
                            id="register-display-name"
                            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="John Doe"
                            maxlength="100"
                        >
                    </div>

                    <div>
                        <label class="block text-purple-200 text-sm font-medium mb-2">Password</label>
                        <input
                            type="password"
                            id="register-password"
                            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="••••••••"
                            minlength="8"
                            required
                        >
                        <div id="password-strength" class="mt-2 h-1 rounded-full bg-white/20 overflow-hidden">
                            <div id="password-strength-bar" class="h-full w-0 transition-all duration-300"></div>
                        </div>
                        <p id="password-hint" class="mt-1 text-xs text-purple-300">At least 8 characters with uppercase, lowercase, and number</p>
                    </div>

                    <div>
                        <label class="block text-purple-200 text-sm font-medium mb-2">Confirm Password</label>
                        <input
                            type="password"
                            id="register-confirm-password"
                            class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                            placeholder="••••••••"
                            required
                        >
                    </div>

                    <div class="flex items-start">
                        <input type="checkbox" id="accept-terms" class="mt-1 w-4 h-4 rounded border-white/20 bg-white/10 text-purple-500 focus:ring-purple-500" required>
                        <label class="ml-2 text-sm text-purple-200">
                            I agree to the <a href="#" class="text-white hover:underline">Terms of Service</a> and <a href="#" class="text-white hover:underline">Privacy Policy</a>
                        </label>
                    </div>

                    <button
                        type="submit"
                        id="register-submit"
                        class="w-full py-3 px-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-semibold rounded-lg hover:from-purple-600 hover:to-pink-600 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-purple-900 transition-all disabled:opacity-50"
                    >
                        Create Account
                    </button>
                </form>

                <!-- Login Link -->
                <div class="mt-6 text-center">
                    <p class="text-purple-200">
                        Already have an account?
                        <a href="#" id="goto-login" class="text-white font-semibold hover:underline">Sign in</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
    """

    # Setup event handlers
    setup_register_handlers()


def setup_register_handlers():
    """Setup registration form event handlers."""
    form = document.getElementById("register-form")
    login_link = document.getElementById("goto-login")
    password_input = document.getElementById("register-password")

    def check_password_strength(event):
        password = event.target.value
        strength_bar = document.getElementById("password-strength-bar")
        hint = document.getElementById("password-hint")

        strength = 0
        if len(password) >= 8:
            strength += 25
        if any(c.isupper() for c in password):
            strength += 25
        if any(c.islower() for c in password):
            strength += 25
        if any(c.isdigit() for c in password):
            strength += 25

        strength_bar.style.width = f"{strength}%"

        if strength <= 25:
            strength_bar.className = "h-full transition-all duration-300 bg-red-500"
            hint.textContent = "Weak - add more character types"
        elif strength <= 50:
            strength_bar.className = "h-full transition-all duration-300 bg-yellow-500"
            hint.textContent = "Fair - add uppercase and numbers"
        elif strength <= 75:
            strength_bar.className = "h-full transition-all duration-300 bg-blue-500"
            hint.textContent = "Good - almost there!"
        else:
            strength_bar.className = "h-full transition-all duration-300 bg-green-500"
            hint.textContent = "Strong password!"

    def handle_submit(event):
        event.preventDefault()

        username = document.getElementById("register-username").value
        email = document.getElementById("register-email").value
        display_name = document.getElementById("register-display-name").value
        password = document.getElementById("register-password").value
        confirm_password = document.getElementById("register-confirm-password").value
        submit_btn = document.getElementById("register-submit")
        error_div = document.getElementById("register-error")
        error_text = document.getElementById("register-error-text")
        success_div = document.getElementById("register-success")

        # Hide previous messages
        error_div.classList.add("hidden")
        success_div.classList.add("hidden")

        # Validate
        if password != confirm_password:
            error_div.classList.remove("hidden")
            error_text.textContent = "Passwords do not match"
            return

        if len(password) < 8:
            error_div.classList.remove("hidden")
            error_text.textContent = "Password must be at least 8 characters"
            return

        # Disable button
        submit_btn.disabled = True
        submit_btn.textContent = "Creating account..."

        def on_success(data):
            submit_btn.disabled = False
            submit_btn.textContent = "Create Account"

            # Connect WebSocket
            connect_websocket()

            # Redirect to onboarding or dashboard
            window.location.hash = "#/dashboard"

        def on_error(status, message):
            submit_btn.disabled = False
            submit_btn.textContent = "Create Account"
            error_div.classList.remove("hidden")
            error_text.textContent = message

        register(
            email=email,
            username=username,
            password=password,
            display_name=display_name or None,
            on_success=on_success,
            on_error=on_error
        )

    def goto_login(event):
        event.preventDefault()
        window.location.hash = "#/login"

    form.bind("submit", handle_submit)
    login_link.bind("click", goto_login)
    password_input.bind("input", check_password_strength)
