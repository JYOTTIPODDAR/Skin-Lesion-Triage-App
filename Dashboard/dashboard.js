const API_URL = "http://127.0.0.1:8000";

// ================================
// CHECK LOGIN TOKEN
// ================================

const token = localStorage.getItem("token");

if (!token) {

    alert("Please login first!");

    window.location.href = "../Authentication/auth.html";

}


// ================================
// GET CURRENT USER
// ================================

async function getCurrentUser() {

    try {

        const response = await fetch(`${API_URL}/auth/me`, {

            method: "GET",

            headers: {
                "Authorization": `Bearer ${token}`
            }

        });

        const data = await response.json();


        // TOKEN INVALID OR EXPIRED

        if (!response.ok) {

            localStorage.removeItem("token");

            alert("Session expired. Please login again!");

            window.location.href = "../Authentication/auth.html";

            return;

        }


        // ================================
        // SHOW USER NAME
        // ================================

        document.getElementById("welcomeUser").textContent =
            `Hello, ${data.username}!`;


        document.getElementById("userName").textContent =
            data.username;


        // PROFILE INITIAL

        document.querySelector(".profile-circle").textContent =
            data.username.charAt(0).toUpperCase();


    } catch (error) {

        console.error(error);

        alert("Cannot connect to server!");

    }

}

// ================================
// LOGOUT
// ================================

const logoutBtn = document.getElementById("logoutBtn");

logoutBtn.addEventListener("click", function () {

    localStorage.removeItem("token");

    alert("Logged out successfully!");

    window.location.href = "../Authentication/auth.html";

});

// CALL FUNCTION

getCurrentUser();