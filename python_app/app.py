import streamlit as st
import os
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import utils
import model

# Coin classes (CZK)
COIN_CLASSES = [1, 2, 5, 10, 20, 50]
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coin_model.pth")

st.set_page_config(page_title="Detektor Mincí (Neural Network)", page_icon="🪙")

@st.cache_resource
def load_nn_model():
    """
    Loads the PyTorch model.
    """
    # Try to load trained weights
    # Try to load trained weights
    if os.path.exists(MODEL_PATH):
        net = model.load_model(MODEL_PATH, num_classes=len(COIN_CLASSES))
    else:
        st.warning("Model 'coin_model.pth' nenalezen. Používám náhodné váhy.")
        net = model.load_model(num_classes=len(COIN_CLASSES))
    return net

def main():
    st.title("🪙 Detektor Mincí s Neuronovou Sítí")
    st.write("Nahrajte obrázek českých mincí pro jejich detekci a spočítání.")

    # Sidebar parameters
    st.sidebar.header("Nastavení Detekce (Hough)")
    st.sidebar.info("Hough Transform je robustnější pro kruhové objekty.")
    
    param1 = st.sidebar.slider("Canny Threshold (Hrany)", 10, 200, 100, help="Vyšší hodnota = méně hran. Snižte, pokud se mince nenajdou.")
    param2 = st.sidebar.slider("Accumulator Threshold (Senzitivita)", 10, 100, 70, help="Nižší hodnota = více kruhů (i falešných). Vyšší = přísnější detekce.")
    min_radius = st.sidebar.slider("Min Poloměr (px)", 10, 100, 30)
    max_radius = st.sidebar.slider("Max Poloměr (px)", 50, 300, 150)
    
    st.sidebar.header("Filtrace Výsledků")
    conf_threshold = st.sidebar.slider("Minimální Jistota Modelu", 0.0, 1.0, 0.30, help="Zahoď detekce, kde si model není jistý (méně než X %). Pomáhá odstranit falešné detekce na pozadí.")

    st.sidebar.header("Model")
    if os.path.exists(MODEL_PATH):
         st.sidebar.success("Model načten!")
    else:
         st.sidebar.warning("Model nenalezen (používám náhodné váhy).")

    uploaded_file = st.file_uploader("Vyberte obrázek...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)
        st.image(image, caption="Původní obrázek", use_container_width=True)

        if st.button("Analyzovat Mince"):
            with st.spinner("Zpracovávám obraz a běžím inferenci..."):
                # 1. Preprocess using OpenCV
                image_cv, (orig_w, orig_h) = utils.preprocess_image(image)
                
                # 2. Detect Candidates
                candidates, debug_image = utils.detect_regions(
                    image_cv, 
                    param1=param1, 
                    param2=param2, 
                    min_radius=min_radius, 
                    max_radius=max_radius
                )
                
                if not candidates:
                    st.warning("Nebyly nalezeny žádné mince. Zkuste upravit parametry detekce v postranním panelu.")
                    st.image(debug_image, caption="Debug: Detekované kontury", use_container_width=True)
                    return

                # 3. Neural Network Inference
                net = load_nn_model()
                results = []
                
                output_image = image_cv.copy()
                
                for (x, y, r) in candidates:
                    # Extract crop
                    crop = utils.extract_coin_image(image_cv, x, y, r)
                    
                    # Prepare for PyTorch (HWC -> CHW, Normalize)
                    tensor = torch.from_numpy(crop).float() / 255.0
                    tensor = tensor.permute(2, 0, 1).unsqueeze(0) # [1, 3, 64, 64]
                    
                    # Inference
                    with torch.no_grad():
                        outputs = net(tensor)
                        probs = F.softmax(outputs, dim=1)
                        predicted_idx = torch.argmax(probs, dim=1).item()
                        predicted_value = COIN_CLASSES[predicted_idx]
                        confidence = probs[0][predicted_idx].item()
                    
                    # Apply confidence filtering
                    if confidence < conf_threshold:
                         # Draw ignored candidate in red (debug)
                         cv2.circle(output_image, (x, y), r, (0, 0, 255), 2)
                         cv2.putText(output_image, f"Ignored ({confidence:.2f})", (x - 40, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                         continue

                    results.append({
                        "value": predicted_value,
                        "confidence": confidence,
                        "position": (x, y)
                    })
                    
                    # Draw result
                    cv2.circle(output_image, (x, y), r, (0, 255, 0), 2)
                    cv2.putText(output_image, f"{predicted_value} Kc", (x - 20, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                # 4. Show Results
                # Convert BGR to RGB for Streamlit
                output_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
                st.image(output_rgb, caption="Výsledek Detekce", use_container_width=True)
                
                st.subheader("Statistika")
                total_sum = sum(r['value'] for r in results)
                st.metric("Celková hodnota", f"{total_sum} Kč")
                st.metric("Počet mincí", len(results))
                
                st.write("Detailní detekce:")
                st.dataframe(results)

if __name__ == "__main__":
    main()
