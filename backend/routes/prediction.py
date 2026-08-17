from fastapi import APIRouter,UploadFile,File
router=APIRouter()
@router.get("/test")
def test_prediction():
    return{"Message":"Prediction Route is working"}

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    return{
        "filename": file.filename,
        "message": "Image received successfully"
    }