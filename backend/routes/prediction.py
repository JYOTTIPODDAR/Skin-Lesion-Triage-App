from fastapi import APIRouter, UploadFile, File, HTTPException
import tensorflow as tf
import numpy as np
from PIL import Image, UnidentifiedImageError
import io
import os


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


# =====================================
# BASE DIRECTORY
# =====================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# =====================================
# MODEL PATHS
# =====================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model_training",
    "models",
    "skin_lesion_model.keras"
)

VALIDATOR_MODEL_PATH = os.path.join(
    BASE_DIR,
    "model_training",
    "models",
    "skin_validator.keras"
)


# =====================================
# LOAD MODELS
# =====================================

model = tf.keras.models.load_model(MODEL_PATH)
validator_model = tf.keras.models.load_model(VALIDATOR_MODEL_PATH)


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
# RISK INFORMATION
# =====================================

RISK_INFO = {

    "NV": {
        "risk_level": "LOW",
        "title": "Lower-risk pattern",
        "recommendation": (
            "Monitor the area regularly. If you notice changes in size, "
            "shape, color, bleeding, itching, or other unusual changes, "
            "consult a dermatologist."
        )
    },

    "DF": {
        "risk_level": "LOW",
        "title": "Lower-risk pattern",
        "recommendation": (
            "Continue monitoring the lesion. Seek medical advice if it "
            "changes noticeably or causes symptoms."
        )
    },

    "BKL": {
        "risk_level": "MEDIUM",
        "title": "Needs attention",
        "recommendation": (
            "Consider scheduling a dermatologist consultation, especially "
            "if the lesion is new or changing."
        )
    },

    "VASC": {
        "risk_level": "MEDIUM",
        "title": "Needs attention",
        "recommendation": (
            "Monitor the area and consider consulting a healthcare "
            "professional if it changes, bleeds, or causes discomfort."
        )
    },

    "AK": {
        "risk_level": "MEDIUM",
        "title": "Professional evaluation recommended",
        "recommendation": (
            "Arrange a dermatologist consultation for proper evaluation."
        )
    },

    "BCC": {
        "risk_level": "HIGH",
        "title": "Prompt medical evaluation recommended",
        "recommendation": (
            "Please arrange a dermatologist appointment as soon as possible."
        )
    },

    "SCC": {
        "risk_level": "HIGH",
        "title": "Prompt medical evaluation recommended",
        "recommendation": (
            "Please seek prompt evaluation from a dermatologist or qualified "
            "healthcare professional."
        )
    },

    "MEL": {
        "risk_level": "HIGH",
        "title": "Urgent professional evaluation recommended",
        "recommendation": (
            "Please arrange prompt evaluation by a dermatologist."
        )
    }
}


# =====================================
# VALIDATE IMAGE FILE
# =====================================

def validate_image(image_bytes):

    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        return True

    except (UnidentifiedImageError, OSError):
        return False


# =====================================
# PREPROCESS IMAGE
# =====================================

def preprocess_image(image_bytes):

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    image = image.resize((224, 224))

    image_array = np.array(image).astype("float32")

    image_array = image_array / 255.0

    image_array = np.expand_dims(image_array, axis=0)

    return image_array


# =====================================
# CHECK SKIN LESION
# =====================================

def check_skin_lesion(image_array):

    prediction = validator_model.predict(
        image_array,
        verbose=0
    )

    # 0 = not_skin_lesion
    # 1 = skin_lesion
    skin_probability = float(prediction[0][0])

    return skin_probability


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

    # FILE TYPE CHECK
    allowed_types = [
        "image/jpeg",
        "image/png"
    ]

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG, JPEG, or PNG image."
        )


    # READ FILE
    image_bytes = await file.read()


    # EMPTY FILE CHECK
    if not image_bytes:

        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty."
        )


    # SIZE CHECK
    if len(image_bytes) > 5 * 1024 * 1024:

        raise HTTPException(
            status_code=400,
            detail="Image must be smaller than 5 MB."
        )


    # VALID IMAGE CHECK
    if not validate_image(image_bytes):

        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted image."
        )


    try:

        # =================================
        # PREPROCESS
        # =================================

        image_array = preprocess_image(image_bytes)


        # =================================
        # STEP 1: VALIDATOR
        # =================================

        skin_probability = check_skin_lesion(image_array)


        # Debugging - backend terminal
        print(
            f"Skin lesion probability: {skin_probability:.4f}"
        )


        # =================================
        # REJECT RANDOM IMAGE
        # =================================

        VALIDATOR_THRESHOLD = 0.50

        if skin_probability < VALIDATOR_THRESHOLD:

            return {

                "valid_image": False,

                "message": (
                    "Invalid image. This does not appear to be a skin "
                    "lesion image. Please upload a clear skin lesion image."
                ),

                "skin_lesion_confidence": round(
                    skin_probability * 100,
                    2
                )
            }


        # =================================
        # STEP 2: MAIN MODEL
        # =================================

        predictions = model.predict(
            image_array,
            verbose=0
        )

        predicted_index = int(
            np.argmax(predictions[0])
        )

        confidence = float(
            np.max(predictions[0]) * 100
        )

        predicted_class = CLASS_NAMES[predicted_index]


        # =================================
        # LOW CONFIDENCE CHECK
        # =================================

        if confidence < 50:

            return {

                "valid_image": False,

                "message": (
                    "The AI could not confidently classify this skin lesion. "
                    "Please upload a clearer image."
                ),

                "confidence": round(confidence, 2)
            }


        # =================================
        # GET RISK DATA
        # =================================

        risk_data = RISK_INFO[predicted_class]


        # =================================
        # SUCCESS RESPONSE
        # =================================

        return {

            "valid_image": True,

            "filename": file.filename,

            "prediction": predicted_class,

            "confidence": round(confidence, 2),

            "skin_lesion_confidence": round(
                skin_probability * 100,
                2
            ),

            "risk_level": risk_data["risk_level"],

            "result_title": risk_data["title"],

            "recommendation": risk_data["recommendation"],

            "disclaimer": (
                "This is an AI-based preliminary screening result and "
                "not a medical diagnosis. Please consult a qualified "
                "healthcare professional for medical advice."
            )
        }


    except Exception as error:

        print("Prediction Error:", error)

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )