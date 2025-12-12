import cv2
import numpy as np
from PIL import Image

STANDARD_SIZE = (512, 512)
BLUR_KERNEL = (5, 5)  # Slightly larger kernel for better noise reduction
CANNY_THRESHOLDS = (30, 150)
DILATE_ITER = 2

def preprocess_image(image_pil):
    """
    Converts PIL image to OpenCV format and resizes it.
    """
    # Convert PIL Image to numpy array (OpenCV format)
    image_np = np.array(image_pil)
    
    # Convert RGB to BGR (OpenCV uses BGR)
    if len(image_np.shape) == 3 and image_np.shape[2] == 3:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    elif len(image_np.shape) == 3 and image_np.shape[2] == 4:
         image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)

    # Resize for consistent processing
    orig_h, orig_w = image_np.shape[:2]
    resized = cv2.resize(image_np, STANDARD_SIZE)
    
    return resized, (orig_w, orig_h)

def detect_regions(image_cv, param1=50, param2=30, min_radius=10, max_radius=100):
    """
    Detects coin-like regions using Hough Circle Transform.
    Returns: list of (x, y, r) tuples and the debug image.
    """
    # Preprocessing
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    # Apply slightly stronger blur to reduce noise from texture
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # Hough Circle Transform
    # method=cv2.HOUGH_GRADIENT
    # dp=1: Inverse ratio of the accumulator resolution to the image resolution.
    # minDist=param: Minimum distance between the centers of the detected circles.
    circles = cv2.HoughCircles(
        blurred, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=min_radius * 2,  # Assume coins don't overlap more than this
        param1=param1, # Higher threshold for Canny edge detector
        param2=param2, # Accumulator threshold (lower = more circles, higher = fewer/better)
        minRadius=min_radius,
        maxRadius=max_radius
    )
    
    candidates = []
    debug_image = image_cv.copy()
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        # Sort circles by radius (ascending) to prefer smaller, tighter circles
        # This helps avoiding selecting large "background" circles first
        sorted_indices = np.argsort(circles[0, :, 2])
        sorted_circles = circles[0, sorted_indices, :]

        selected_circles = []
        for i in range(sorted_circles.shape[0]):
            x, y, r = int(sorted_circles[i, 0]), int(sorted_circles[i, 1]), int(sorted_circles[i, 2])
            
            is_duplicate = False
            for (sx, sy, sr) in selected_circles:
                # Calculate distance between centers
                dist = np.sqrt((x - sx)**2 + (y - sy)**2)
                
                # Check for significant overlap
                # If centers are closer than the larger radius, one is likely inside the other
                # Use a factor (e.g., 0.85) to allow slight overlap but reject concentric
                max_r = max(r, sr)
                if dist < max_r * 0.85: 
                     is_duplicate = True
                     break
            
            if not is_duplicate:
                selected_circles.append((x, y, r))
                candidates.append((x, y, r))
                # Draw outer circle
                cv2.circle(debug_image, (x, y), r, (0, 255, 0), 2)
                # Draw center
                cv2.circle(debug_image, (x, y), 2, (0, 0, 255), 3)
            
    return candidates, debug_image

def extract_coin_image(image_cv, center_x, center_y, radius, target_size=(64, 64)):
    """
    Extracts a square crop around the coin and resizes it for the CNN.
    """
    h, w = image_cv.shape[:2]
    
    # Add some padding to capture the edge
    padding = int(radius * 0.2)
    x1 = max(0, center_x - radius - padding)
    y1 = max(0, center_y - radius - padding)
    x2 = min(w, center_x + radius + padding)
    y2 = min(h, center_y + radius + padding)
    
    crop = image_cv[y1:y2, x1:x2]
    
    if crop.size == 0:
        return np.zeros((target_size[0], target_size[1], 3), dtype=np.uint8)
        
    crop_resized = cv2.resize(crop, target_size)
    
    # Convert back to RGB for the model (assuming model trained on RGB)
    crop_rgb = cv2.cvtColor(crop_resized, cv2.COLOR_BGR2RGB)
    
    return crop_rgb
