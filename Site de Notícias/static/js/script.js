document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        const usernameInput = document.getElementById('username');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');

        const usernameError = document.getElementById('usernameError');
        const emailError = document.getElementById('emailError');
        const passwordError = document.getElementById('passwordError');

        registrationForm.addEventListener('submit', function(event) {
            let isValid = true;

            usernameError.textContent = '';
            emailError.textContent = '';
            passwordError.textContent = '';

            if (usernameInput.value.trim() === '') {
                usernameError.textContent = 'O nome de usuário é obrigatório.';
                isValid = false;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailInput.value.trim() === '') {
                emailError.textContent = 'O e-mail é obrigatório.';
                isValid = false;
            } else if (!emailRegex.test(emailInput.value.trim())) {
                emailError.textContent = 'Por favor, insira um e-mail válido.';
                isValid = false;
            }

            if (passwordInput.value.trim() === '') {
                passwordError.textContent = 'A senha é obrigatória.';
                isValid = false;
            } else if (passwordInput.value.trim().length < 6) {
                passwordError.textContent = 'A senha deve ter pelo menos 6 caracteres.';
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }
});