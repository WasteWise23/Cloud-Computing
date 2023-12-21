from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from io import BytesIO
from PIL import Image

model_path = "model/model_WasteWise_baru80.h5"
class_labels = ['battery', 'cardboard', 'Carton', 'glass', 'metal', 'organic', 'paper', 'plastic']

# Load the model
model = load_model(model_path)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

def preprocess_image(file_content):
    # Load and preprocess the image
    img = Image.open(BytesIO(file_content)).convert('RGB')
    img = img.resize((150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values to between 0 and 1
    return img_array

async def predict_image(file: UploadFile = File(...)):
    try:
        # Perform prediction
        img_array = preprocess_image(await file.read())
        prediction = model.predict(img_array, batch_size=10)
        class_index = np.argmax(prediction, axis=1)
        class_label_prediction = class_labels[class_index[0]]
        # Return the prediction result
        return JSONResponse(content={"prediction": class_label_prediction, "probability": float(prediction[0][class_index[0]])})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
