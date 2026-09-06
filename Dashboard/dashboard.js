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


        if (!response.ok) {

            localStorage.removeItem("token");

            alert("Session expired. Please login again!");

            window.location.href = "../Authentication/auth.html";

            return;

        }


        // SHOW USER NAME

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


// ================================
// IMAGE UPLOAD & PREDICTION
// ================================

const uploadBtn = document.getElementById("uploadBtn");
const imageInput = document.getElementById("imageInput");
const resultContainer = document.getElementById("resultContainer");


uploadBtn.addEventListener("click", function () {

    imageInput.click();

});


imageInput.addEventListener("change", async function () {

    const file = imageInput.files[0];

    if (!file) return;


    // CHECK FILE TYPE

    if (!file.type.startsWith("image/")) {

        alert("Please select a valid image!");

        return;

    }


    // CHECK FILE SIZE

    if (file.size > 5 * 1024 * 1024) {

        alert("Image size must be less than 5MB!");

        return;

    }


    // CREATE FORM DATA

    const formData = new FormData();

    formData.append("file", file);


    // BUTTON LOADING

    uploadBtn.textContent = "Analyzing...";

    uploadBtn.disabled = true;


    // HIDE OLD RESULT

    resultContainer.style.display = "none";


    try {

        const response = await fetch(

            `${API_URL}/prediction/predict`,

            {
                method: "POST",
                body: formData
            }

        );


        const data = await response.json();


        // =====================================
        // SUCCESSFUL RESPONSE
        // =====================================

        if (response.ok) {


            // INVALID / UNCERTAIN IMAGE

            if (data.valid_image === false) {

                resultContainer.innerHTML = `
                    <div class="result-card invalid-result">

                        <h2>⚠️ Unable to Analyze Image</h2>

                        <p>${data.message}</p>

                        <p class="confidence">
                            Confidence: ${data.confidence}%
                        </p>

                        <p>
                            Please upload a clear close-up image of a skin lesion.
                        </p>

                    </div>
                `;

                resultContainer.style.display = "block";

                return;

            }


            // =====================================
            // RISK COLOR
            // =====================================

            let riskClass = "";

            if (data.risk_level === "LOW") {

                riskClass = "low-risk";

            } else if (data.risk_level === "MEDIUM") {

                riskClass = "medium-risk";

            } else if (data.risk_level === "HIGH") {

                riskClass = "high-risk";

            }


            // =====================================
            // SHOW RESULT
            // =====================================

            resultContainer.innerHTML = `

                <div class="result-card ${riskClass}">

                    <h2>🔍 Skin Analysis Result</h2>

                    <div class="result-row">

                        <span>Prediction:</span>

                        <strong>${data.prediction}</strong>

                    </div>


                    <div class="result-row">

                        <span>Risk Level:</span>

                        <strong>${data.risk_level}</strong>

                    </div>


                    <div class="result-row">

                        <span>Confidence:</span>

                        <strong>${data.confidence}%</strong>

                    </div>


                    <hr>


                    <h3>${data.result_title}</h3>


                    <p class="recommendation">

                        ${data.recommendation}

                    </p>


                    <div class="disclaimer">

                        ⚕️ ${data.disclaimer}

                    </div>

                </div>

            `;


            resultContainer.style.display = "block";


            // RESULT TAKES USER TO CARD

            resultContainer.scrollIntoView({

                behavior: "smooth"

            });


        } else {

            alert(data.detail || "Prediction failed!");

        }


    } catch (error) {

        console.error(error);

        alert("Cannot connect to prediction server!");

    } finally {


        // RESET BUTTON

        uploadBtn.textContent = "⇧ Upload Image";

        uploadBtn.disabled = false;

        imageInput.value = "";

    }

});


// ================================
// CALL FUNCTION
// ================================

getCurrentUser();