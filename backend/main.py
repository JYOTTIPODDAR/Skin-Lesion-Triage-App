from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth import router as auth_router
from routes.prediction import router as prediction_router


app = FastAPI()


# ================================
# CORS
# ================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# AUTHENTICATION ROUTES
# ================================

app.include_router(auth_router)


# ================================
# PREDICTION ROUTES
# ================================

app.include_router(prediction_router)


# ================================
# HOME ROUTE
# ================================

@app.get("/")
def home():

    return {
        "message": "Skin Lesion Triage Backend is Running"
    }