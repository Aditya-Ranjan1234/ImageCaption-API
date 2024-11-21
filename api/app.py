from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Dict
import os
from img import ImageProcessor

app = FastAPI()
processor = ImageProcessor()

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    image_path = os.path.join("images", file.filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    try:
        with open(image_path, "wb") as image_file:
            image_file.write(await file.read())
        
        processor.load_uploaded_image(image_path)
        result = processor.generate_image_analysis()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")

@app.post("/generate-caption-genre")
async def generate_caption_genre(context: str = Form(...), file: UploadFile = File(...)) -> Dict:
    image_path = os.path.join("images", file.filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    try:
        with open(image_path, "wb") as image_file:
            image_file.write(await file.read())
        
        processor.load_uploaded_image(image_path)
        result = processor.generate_image_caption_genre(context)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating caption and genre: {str(e)}")
