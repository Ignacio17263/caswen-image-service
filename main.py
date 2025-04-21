from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64

app = FastAPI()

def resize_and_crop(image: Image.Image, size: tuple) -> str:
    resized = image.copy()
    resized.thumbnail(size, Image.LANCZOS)
    background = Image.new("RGB", size, (255, 255, 255))
    background.paste(resized, ((size[0] - resized.size[0]) // 2, (size[1] - resized.size[1]) // 2))
    buffer = io.BytesIO()
    background.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

@app.post("/generate-images")
async def generate_images(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    output = {
        "portrait": resize_and_crop(image, (1080, 1920)),
        "feed": resize_and_crop(image, (1080, 1350)),
        "landscape": resize_and_crop(image, (1200, 675))
    }

    return JSONResponse(content=output)
