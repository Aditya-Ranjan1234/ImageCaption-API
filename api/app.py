from fastapi import FastAPI, File, UploadFile
from img import ImageProcessor

app = FastAPI()
processor = ImageProcessor()

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    image_path = f"/tmp/{file.filename}"
    with open(image_path, "wb") as image_file:
        image_file.write(await file.read())
    processor.image_documents = [image_path]
    result = processor.generate_image_analysis()
    return result

@app.post("/generate-caption-genre")
async def generate_caption_genre(context: str, file: UploadFile = File(...)):
    image_path = f"/tmp/{file.filename}"
    with open(image_path, "wb") as image_file:
        image_file.write(await file.read())
    processor.image_documents = [image_path]
    result = processor.generate_image_caption_genre(context)
    return result
