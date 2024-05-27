from fastapi import  File, UploadFile, HTTPException, APIRouter
from fastapi.responses import StreamingResponse
from PIL import Image
import numpy as np
from io import BytesIO
import os
from scipy.signal import convolve2d


UPLOAD_DIR = "uploads"

router = APIRouter(
    prefix="/images",
    tags=["images"]
)

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGBA")  
        image_array = np.array(image)

        # Separar os canais R, G, B e A
        r, g, b, a = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2], image_array[:, :, 3]

        # Kernel de convolução (3x3)
        kernel = np.array([[0.3, 0.3, -0.3],
                           [0.3, -0.3, 0.3],
                           [-0.3, 0.3, 0.3]])

        # Aplicar a convolução a cada canal separadamente
        r = convolve2d(r, kernel, mode='same', boundary='wrap')
        g = convolve2d(g, kernel, mode='same', boundary='wrap')
        b = convolve2d(b, kernel, mode='same', boundary='wrap')

        # Reconstruir a imagem com os canais filtrados
        filtered_image = np.stack((r, g, b, a), axis=-1)
        filtered_image = np.clip(filtered_image, 0, 255).astype(np.uint8)

        # Converter de volta para imagem PIL
        filtered_pil_image = Image.fromarray(filtered_image)
        buffer = BytesIO()
        filtered_pil_image.save(buffer, format="PNG")
        buffer.seek(0)

        return StreamingResponse(buffer, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
