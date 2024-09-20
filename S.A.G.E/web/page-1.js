document.addEventListener('DOMContentLoaded', () => {
    const techLines = document.querySelector('.tech-lines');

    // Create tech lines
    for (let i = 0; i < 50; i++) {
        const line = document.createElement('div');
        line.classList.add('line');
        line.style.width = `${Math.random() * 150 + 50}px`;
        line.style.height = `${Math.random() * 2 + 1}px`;
        line.style.top = `${Math.random() * 100}vh`;
        line.style.left = `${Math.random() * 100}vw`;
        line.style.animationDuration = `${Math.random() * 10 + 5}s`;
        line.style.animationDirection = Math.random() < 0.5 ? 'normal' : 'reverse';
        techLines.appendChild(line);
    }

    const loginBtn = document.querySelector("#login");
    const registerBtn = document.querySelector("#register");
    const loginForm = document.querySelector(".login-form");
    const registerForm = document.querySelector(".register-form");

    loginBtn.addEventListener('click', () => {
        loginBtn.style.backgroundColor = "#21264D";
        registerBtn.style.backgroundColor = "rgba(255, 255, 255, 0.2)";

        loginForm.style.left = "50%";
        registerForm.style.left = "150%";

        loginForm.style.opacity = 1;
        registerForm.style.opacity = 0;
    });

    registerBtn.addEventListener('click', () => {
        loginBtn.style.backgroundColor = "rgba(255, 255, 255, 0.2)";
        registerBtn.style.backgroundColor = "#21264D";

        loginForm.style.left = "-50%";
        registerForm.style.left = "50%";

        loginForm.style.opacity = 0;
        registerForm.style.opacity = 1;
    });

    document.querySelector("#login-submit").addEventListener('click', loginuser);
    document.querySelector("#register-submit").addEventListener('click', registeruser);
});

async function loginuser() {
    var uname = document.getElementById('lname').value;
    var pass = document.getElementById('lpassword').value;
    const result = await eel.loginuser(uname, pass)();
    if (result) {
        window.location = "page-2.html";
    } else {
        alert('Login failed');
    }
    
}

// Function to handle registration
async function registeruser() {
    var mail = document.getElementById('email').value;
    var uname = document.getElementById('rname').value;
    var pass = document.getElementById('rpassword').value;
    const result = await eel.registeruser(mail, uname, pass)();
    if (result) {
        alert('Registration successful');
        document.getElementById('email').value = '';
        document.getElementById('rname').value = '';
        document.getElementById('rpassword').value = '';
        // Switch to login form
        document.querySelector("#login").click();
    } else {
        alert('Registration failed');
    }
}