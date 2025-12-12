import io
import numpy as np
from fastapi import UploadFile, HTTPException
from PIL import Image
import cv2

class ImageValidator:
    @staticmethod
    def validate(file: UploadFile) -> np.ndarray:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        try:
            contents = file.file.read()
            pil_image = Image.open(io.BytesIO(contents))
            image_array = np.array(pil_image)
            if len(image_array.shape) == 3:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            return image_array
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
