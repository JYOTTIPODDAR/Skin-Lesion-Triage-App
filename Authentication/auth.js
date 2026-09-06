const loginTab = document.getElementById("loginTab");
const signupTab = document.getElementById("signupTab");

const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");

const signupText = document.getElementById("signupText");
const loginText = document.getElementById("loginText");


function showLogin() {

    loginTab.classList.add("active");
    signupTab.classList.remove("active");

    loginForm.classList.remove("hidden");
    signupForm.classList.add("hidden");

}


function showSignup() {

    signupTab.classList.add("active");
    loginTab.classList.remove("active");

    signupForm.classList.remove("hidden");
    loginForm.classList.add("hidden");

}


loginTab.addEventListener("click", showLogin);

signupTab.addEventListener("click", showSignup);


signupText.addEventListener("click", showSignup);

loginText.addEventListener("click", showLogin);