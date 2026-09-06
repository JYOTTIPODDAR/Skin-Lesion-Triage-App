from fastapi import APIRouter, UploadFile, File, HTTPException
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


# =====================================
# LOAD TRAINED MODEL
# =====================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model_training",
    "models",
    "skin_lesion_model.keras"
)

model = tf.keras.models.load_model(MODEL_PATH)


# =====================================
# CLASS NAMES
# =====================================

CLASS_NAMES = [
    "AK",
    "BCC",
    "BKL",
    "DF",
    "MEL",
    "NV",
    "SCC",
    "VASC"
]


# =====================================
# TEST ROUTE
# =====================================

@router.get("/test")
def test_prediction():

    return {
        "message": "Prediction API is working"
    }


# =====================================
# PREDICT
# =====================================

@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Check image type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image"
        )

    try:

        # Read uploaded image
        image_bytes = await file.read()

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")


        # Resize image
        image = image.resize((224, 224))


        # Convert image to array
        image_array = np.array(image)


        # Normalize image
        image_array = image_array / 255.0


        # Add batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        # Model prediction
        predictions = model.predict(image_array)

        predicted_index = int(
            np.argmax(predictions)
        )

        confidence = float(
            np.max(predictions) * 100
        )


        return {

            "filename": file.filename,

            "prediction": CLASS_NAMES[predicted_index],

            "confidence": round(confidence, 2)

        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )