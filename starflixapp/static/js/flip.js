
const card = document.getElementById('card');
const flipToRegister = document.getElementById('flipToRegister');
const flipToLogin = document.getElementById('flipToLogin');

flipToRegister.addEventListener('click', function () {
    card.classList.add('flip');
});

flipToLogin.addEventListener('click', function () {
    card.classList.remove('flip');
});

document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    // Your login logic here
    console.log('Login submitted');
});

document.getElementById('registerForm').addEventListener('submit', function (event) {
    event.preventDefault();
    // Your register logic here
    console.log('Register submitted');
});
