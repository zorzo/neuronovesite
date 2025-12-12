import cv2
import numpy as np
import base64
import logging

logger = logging.getLogger(__name__)

STANDARD_SIZE = (512, 512)
BLUR_KERNEL = (3, 3)
BLUR_KERNEL_STEPS = (11, 11)
CANNY_THRESHOLDS = (30, 150)
DILATE_ITER = 2

class CoinDetector:
    def detect_coins(self, image_array: np.ndarray, min_area: int, circularity_threshold: float):
        try:
            orig_h, orig_w = image_array.shape[:2]
            scale_x, scale_y = orig_w / STANDARD_SIZE[0], orig_h / STANDARD_SIZE[1]
            gray, blurred, edges, dilated = self._preprocess(image_array, BLUR_KERNEL)
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            coin_data, output = [], image_array.copy()

            for i, contour in enumerate(contours):
                area, perimeter = cv2.contourArea(contour), cv2.arcLength(contour, True)
                if area < min_area or perimeter == 0:
                    continue
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                if circularity > circularity_threshold:
                    ((x, y), radius) = cv2.minEnclosingCircle(contour)
                    orig_x, orig_y = x * scale_x, y * scale_y
                    avg_scale = (scale_x + scale_y) / 2
                    orig_radius = radius * avg_scale
                    coin_data.append({
                        "id": i + 1,
                        "center_x": float(orig_x),
                        "center_y": float(orig_y),
                        "radius": float(orig_radius),
                        "area": float(area * scale_x * scale_y),
                        "circularity": float(circularity)
                    })
                    circle_thickness = int(2 * avg_scale)
                    font_scale = 0.5 * avg_scale
                    text_thickness = int(1.5 * avg_scale)
                    cv2.circle(output, (int(orig_x), int(orig_y)), int(orig_radius), (0, 255, 255), circle_thickness)
                    cv2.putText(
                        output, f"#{len(coin_data)}",
                        (int(orig_x) - int(20 * avg_scale), int(orig_y) - int(20 * avg_scale)),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 255), text_thickness
                    )
            return len(coin_data), output, coin_data
        except Exception as e:
            logger.error(f"Error in coin detection: {str(e)}")
            raise

    def get_processing_steps(self, image_array: np.ndarray):
        orig_h, orig_w = image_array.shape[:2]
        gray, blurred, edges, dilated = self._preprocess(image_array, BLUR_KERNEL_STEPS)
        steps = {
            'original': self.array_to_base64(image_array),
            'grayscale': self.array_to_base64(cv2.resize(cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR), (orig_w, orig_h))),
            'blurred': self.array_to_base64(cv2.resize(cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR), (orig_w, orig_h))),
            'edges': self.array_to_base64(cv2.resize(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), (orig_w, orig_h))),
            'dilated': self.array_to_base64(cv2.resize(cv2.cvtColor(dilated, cv2.COLOR_GRAY2BGR), (orig_w, orig_h))),
        }
        return steps

    def _preprocess(self, image_array: np.ndarray, blur_kernel):
        resized = cv2.resize(image_array, STANDARD_SIZE)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, blur_kernel, 0)
        edges = cv2.Canny(blurred, *CANNY_THRESHOLDS)
        dilated = cv2.dilate(edges, None, iterations=DILATE_ITER)
        return gray, blurred, edges, dilated

    @staticmethod
    def array_to_base64(image_array: np.ndarray) -> str:
        _, buffer = cv2.imencode('.png', image_array)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/png;base64,{image_base64}"
