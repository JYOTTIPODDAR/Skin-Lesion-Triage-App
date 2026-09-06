from fastapi import FastAPI

from routes.auth import router as auth_router

app = FastAPI()


# Authentication Routes
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Skin Lesion Triage Backend is Running"
    }