document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const identifier = document.getElementById('identifier').value;
            const password = passwordInput.value;
            const isAdmin = loginForm.dataset.admin === 'true';

            if (!identifier || !password) {
                showToast('Please fill all fields', 'error');
                return;
            }

            const submitBtn = loginForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="animate-spin-slow">↻</span>';
            submitBtn.disabled = true;

            try {
                const endpoint = isAdmin ? '/auth/admin/login' : '/auth/login';
                const response = await fetch(`/api/v1${endpoint}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ [identifier.includes('@') ? 'email' : 'username']: identifier, password })
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem('scs_token', data.token);
                    localStorage.setItem('scs_user', JSON.stringify(data.user));
                    
                    if (data.user.role === 'admin') {
                        window.location.href = 'admin-dashboard.html';
                    } else {
                        window.location.href = 'dashboard.html';
                    }
                } else {
                    if (response.status === 423) {
                        showToast(`Account locked. Try again later.`, 'error');
                    } else if (response.status === 401) {
                        const emailMatches = identifier.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);
                        if (emailMatches && !isAdmin) {
                            let attempts = parseInt(localStorage.getItem(`loginAttempts_${identifier}`) || '0') + 1;
                            localStorage.setItem(`loginAttempts_${identifier}`, attempts);
                            if (attempts >= 5) {
                                await fetch('/api/v1/auth/lock-account', {
                                    method: 'POST',
                                    headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify({email: identifier})
                                });
                                showToast('Account temporarily locked due to too many failed attempts.', 'error');
                            } else {
                                showToast(data.error || 'Invalid credentials', 'error');
                            }
                        } else {
                            showToast(data.error || 'Invalid credentials', 'error');
                        }
                    } else {
                        showToast(data.error || 'Login failed', 'error');
                    }
                    submitBtn.classList.add('shake');
                    setTimeout(() => submitBtn.classList.remove('shake'), 500);
                }
            } catch (err) {
                showToast('Network error', 'error');
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }
});

// Helper for shake animation dynamically added to buttons
const style = document.createElement('style');
style.innerHTML = `
@keyframes shake { 
    0%,100%{transform:translateX(0)} 
    25%{transform:translateX(-10px)} 
    75%{transform:translateX(10px)} 
}
.shake { animation: shake 0.5s; }
`;
document.head.appendChild(style);
