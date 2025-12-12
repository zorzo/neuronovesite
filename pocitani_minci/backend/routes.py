from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from image_utils import ImageValidator
from coin_detector import CoinDetector
import logging

logger = logging.getLogger(__name__)

def register_routes(app):
    @app.get("/")
    async def root():
        return {
            "message": "Coin Detection API",
            "version": "1.0.0",
            "endpoints": {
                "POST /detect": "Detect coins in uploaded image",
                "POST /detect/steps": "Get processing steps visualization",
                "GET /health": "Health check"
            }
        }

    @app.post("/detect")
    async def detect_coins(
        file: UploadFile = File(...),
        min_area: int = 100,
        circularity_threshold: float = 0.7,
        return_image: bool = True
    ):
        image_array = ImageValidator.validate(file)
        detector = CoinDetector()
        num_coins, annotated_image, coin_data = detector.detect_coins(
            image_array, min_area, circularity_threshold
        )
        response_data = {
            "success": True,
            "coin_count": num_coins,
            "coins": coin_data,
            "parameters": {
                "min_area": min_area,
                "circularity_threshold": circularity_threshold
            }
        }
        if return_image and num_coins > 0:
            response_data["annotated_image"] = detector.array_to_base64(annotated_image)
        return JSONResponse(content=response_data)

    @app.post("/detect/steps")
    async def detect_with_steps(
        file: UploadFile = File(...),
        min_area: int = 100,
        circularity_threshold: float = 0.7
    ):
        image_array = ImageValidator.validate(file)
        detector = CoinDetector()
        num_coins, annotated_image, coin_data = detector.detect_coins(
            image_array, min_area, circularity_threshold
        )
        steps = detector.get_processing_steps(image_array)
        return JSONResponse(content={
            "success": True,
            "coin_count": num_coins,
            "coins": coin_data,
            "parameters": {
                "min_area": min_area,
                "circularity_threshold": circularity_threshold
            },
            "processing_steps": steps,
            "final_result": detector.array_to_base64(annotated_image) if num_coins > 0 else None
        })
