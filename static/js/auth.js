// Authentication JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    checkAuthStatus();
    
    // Login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Register form
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

// Check authentication status
function checkAuthStatus() {
    const token = localStorage.getItem('smartchoice_token');
    const user = localStorage.getItem('smartchoice_user');
    
    if (token && user) {
        // User is logged in
        updateUIForLoggedInUser(JSON.parse(user));
    }
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const loginData = {
        email: formData.get('email'),
        password: formData.get('password')
    };
    
    showLoading();
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Save token and user data
            localStorage.setItem('smartchoice_token', result.token);
            localStorage.setItem('smartchoice_user', JSON.stringify(result.user));
            
            // Update UI
            updateUIForLoggedInUser(result.user);
            
            // Redirect to products page
            window.location.href = '/products';
        } else {
            showError(result.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        showError('Une erreur est survenue lors de la connexion');
    } finally {
        hideLoading();
    }
}

// Handle registration
async function handleRegister(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    // Validate passwords match
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    
    if (password !== confirmPassword) {
        showError('Les mots de passe ne correspondent pas');
        return;
    }
    
    if (password.length < 6) {
        showError('Le mot de passe doit contenir au moins 6 caractères');
        return;
    }
    
    const registerData = {
        email: formData.get('email'),
        password: password,
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        age: formData.get('age') ? parseInt(formData.get('age')) : null,
        phone: formData.get('phone') || null
    };
    
    showLoading();
    
    try {
        const response = await fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registerData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            // Save token and user data
            localStorage.setItem('smartchoice_token', result.token);
            localStorage.setItem('smartchoice_user', JSON.stringify(result.user));
            
            // Update UI
            updateUIForLoggedInUser(result.user);
            
            // Redirect to products page
            window.location.href = '/products';
        } else {
            showError(result.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showError('Une erreur est survenue lors de l\'inscription');
    } finally {
        hideLoading();
    }
}

// Update UI for logged in user
function updateUIForLoggedInUser(user) {
    const loginLink = document.getElementById('login-link');
    const userDropdown = document.getElementById('user-dropdown');
    const userName = document.getElementById('user-name');
    
    if (loginLink && userDropdown) {
        loginLink.style.display = 'none';
        userDropdown.style.display = 'block';
        
        if (userName) {
            userName.textContent = `${user.first_name} ${user.last_name}`;
        }
    }
}

// Logout
function logout() {
    localStorage.removeItem('smartchoice_token');
    localStorage.removeItem('smartchoice_user');
    window.location.href = '/';
}

// Show loading
function showLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'flex';
    }
}

// Hide loading
function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.style.display = 'none';
    }
}

// Show error message
function showError(message) {
    // Remove existing error messages
    const existingErrors = document.querySelectorAll('.error-message');
    existingErrors.forEach(error => error.remove());
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        background: #fee;
        color: #c00;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        max-width: 300px;
    `;
    
    document.body.appendChild(errorDiv);
    
    // Remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Get auth token for API calls
function getAuthToken() {
    return localStorage.getItem('smartchoice_token');
}

// Check if user is authenticated
function isAuthenticated() {
    return !!localStorage.getItem('smartchoice_token');
}

// Get current user
function getCurrentUser() {
    const user = localStorage.getItem('smartchoice_user');
    return user ? JSON.parse(user) : null;
}
