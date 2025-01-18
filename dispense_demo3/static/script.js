document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const responseMessage = document.getElementById('responseMessage');
    const passwordField = document.getElementById('password');
    const togglePasswordButton = document.getElementById('togglePassword');

    // Handle toggle password visibility
    togglePasswordButton.addEventListener('click', () => {
        const isHidden = passwordField.getAttribute('type') === 'password';

        if (isHidden) {
            // Switch to SHOW mode
            passwordField.setAttribute('type', 'text');
            togglePasswordButton.textContent = 'Hide';
        } else {
            // Switch to HIDE mode
            passwordField.setAttribute('type', 'password');
            togglePasswordButton.textContent = 'Show';
        }
    });

    // Handle form submission
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const result = await response.json();
            responseMessage.textContent = result.message;
            responseMessage.style.color = result.statusType === 'success' ? 'green' : 'red';
        } catch (error) {
            responseMessage.textContent = 'An error occurred while logging in.';
            responseMessage.style.color = 'red';
        }
    });
});
