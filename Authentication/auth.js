const API_URL = "http://127.0.0.1:8000";

// ================================
// ELEMENTS
// ================================

const loginTab = document.getElementById("loginTab");
const signupTab = document.getElementById("signupTab");

const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const forgotPasswordForm = document.getElementById("forgotPasswordForm");

const signupText = document.getElementById("signupText");
const loginText = document.getElementById("loginText");

const forgotPasswordLink = document.getElementById("forgotPasswordLink");
const backToLogin = document.getElementById("backToLogin");


// ================================
// TAB SWITCHING
// ================================

function showLogin() {

    loginTab.classList.add("active");
    signupTab.classList.remove("active");

    loginTab.style.display = "block";
    signupTab.style.display = "block";

    loginForm.classList.remove("hidden");
    signupForm.classList.add("hidden");
    forgotPasswordForm.classList.add("hidden");
}


function showSignup() {

    signupTab.classList.add("active");
    loginTab.classList.remove("active");

    loginTab.style.display = "block";
    signupTab.style.display = "block";

    signupForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
    forgotPasswordForm.classList.add("hidden");
}


function showForgotPassword() {

    loginForm.classList.add("hidden");
    signupForm.classList.add("hidden");

    forgotPasswordForm.classList.remove("hidden");

    // Hide tabs while resetting password
    loginTab.style.display = "none";
    signupTab.style.display = "none";
}


// ================================
// CLICK EVENTS
// ================================

loginTab.addEventListener("click", showLogin);
signupTab.addEventListener("click", showSignup);

signupText.addEventListener("click", showSignup);
loginText.addEventListener("click", showLogin);

forgotPasswordLink.addEventListener("click", function (event) {

    event.preventDefault();

    showForgotPassword();

});

backToLogin.addEventListener("click", showLogin);


// ================================
// SIGNUP
// ================================

signupForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const name = document.getElementById("signupName").value.trim();
    const email = document.getElementById("signupEmail").value.trim();
    const password = document.getElementById("signupPassword").value;

    try {

        const response = await fetch(`${API_URL}/auth/register`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Account created successfully! Please login.");

            signupForm.reset();

            showLogin();

        } else {

            alert(data.detail || "Registration failed");

        }

    } catch (error) {

        console.error(error);

        alert("Cannot connect to server. Please start the backend.");

    }

});


// ================================
// LOGIN
// ================================

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    try {

        const response = await fetch(`${API_URL}/auth/login`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })

        });

        const data = await response.json();

       if (response.ok) {
            localStorage.setItem("token", data.access_token);

            alert("Login successful!");

            window.location.href = "../Dashboard/dashboard.html";


            // आगे dashboard redirect यहां करेंगे

        } else {

            alert(data.detail || "Invalid email or password");

        }

    } catch (error) {

        console.error(error);

        alert("Cannot connect to server. Please start the backend.");

    }

});


// ================================
// FORGOT PASSWORD
// ================================

forgotPasswordForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const email = document.getElementById("forgotEmail").value.trim();
    const newPassword = document.getElementById("newPassword").value;

    try {

        const response = await fetch(`${API_URL}/auth/forgot-password`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                new_password: newPassword
            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Password reset successfully! Please login.");

            forgotPasswordForm.reset();

            showLogin();

        } else {

            alert(data.detail || "Password reset failed");

        }

    } catch (error) {

        console.error(error);

        alert("Cannot connect to server. Please start the backend.");

    }

});