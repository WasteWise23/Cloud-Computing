from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from model.predict import predict_image  # Menggunakan path relatif dari direktori model-api

app = FastAPI()

@app.get("/")
def welcome():
    return{"Message":"Welcome"} 

@app.post("/predict")
async def main(file: UploadFile = File(...)):
    try:
        # Call the predict_image function from predict.py
        result = await predict_image(file)
        return result
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
