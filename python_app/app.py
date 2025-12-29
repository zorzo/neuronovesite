import streamlit as st
import os
import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
import utils
import model

# Kategorie mincí (CZK)
COIN_CLASSES = [1, 2, 5, 10, 20, 50]
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "coin_model.pth")

st.set_page_config(page_title="Detektor Mincí (Neural Network)", page_icon="🪙")

from torchvision import transforms

def load_nn_model():
    """
    Načte PyTorch model.
    """
    # Pokus o načtení natrénovaných vah
    if os.path.exists(MODEL_PATH):
        net = model.load_model(MODEL_PATH, num_classes=len(COIN_CLASSES))
    else:
        st.warning("Model 'coin_model.pth' nenalezen. Používám náhodné váhy.")
        net = model.load_model(num_classes=len(COIN_CLASSES))
    return net

def main():
    st.title("🪙 Detektor Mincí s Neuronovou Sítí")
    st.write("Nahrajte obrázek českých mincí pro jejich detekci a spočítání.")

    # Parametry postranního panelu
    st.sidebar.header("Nastavení Detekce (Hough)")
    st.sidebar.info("Hough Transform je robustnější pro kruhové objekty.")
    
    param1 = st.sidebar.slider("Canny Threshold (Hrany)", 10, 200, 80, help="Vyšší hodnota = méně hran. Snižte, pokud se mince nenajdou.")
    param2 = st.sidebar.slider("Accumulator Threshold (Senzitivita)", 10, 100, 60, help="Nižší hodnota = více kruhů (i falešných). Vyšší = přísnější detekce.")
    min_radius = st.sidebar.slider("Min Poloměr (px)", 10, 100, 30)
    max_radius = st.sidebar.slider("Max Poloměr (px)", 50, 400, 260)
    
    st.sidebar.header("Filtrace Výsledků")
    conf_threshold = st.sidebar.slider("Minimální Jistota Modelu", 0.0, 1.0, 0.30, help="Zahoď detekce, kde si model není jistý (méně než X %). Pomáhá odstranit falešné detekce na pozadí.")

    st.sidebar.header("Model")
    if os.path.exists(MODEL_PATH):
         st.sidebar.success("Model načten!")
    else:
         st.sidebar.warning("Model nenalezen (používám náhodné váhy).")

    uploaded_file = st.file_uploader("Vyberte obrázek...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Načtení obrázku
        image = Image.open(uploaded_file)
        st.image(image, caption="Původní obrázek", use_container_width=True)

        if st.button("Analyzovat Mince"):
            with st.spinner("Zpracovávám obraz a běžím inferenci..."):
                # 1. Předzpracování pomocí OpenCV
                image_cv, (orig_w, orig_h) = utils.preprocess_image(image)
                
                # Příprava původního obrázku pro extrakci ve vysokém rozlišení
                original_cv = np.array(image)
                # Převod RGB na BGR (OpenCV formát)
                if len(original_cv.shape) == 3 and original_cv.shape[2] == 3:
                     original_cv = cv2.cvtColor(original_cv, cv2.COLOR_RGB2BGR)
                elif len(original_cv.shape) == 3 and original_cv.shape[2] == 4:
                     original_cv = cv2.cvtColor(original_cv, cv2.COLOR_RGBA2BGR)
                
                # Výpočet faktorů škálování (Původní / Zmenšený)
                # Použití skutečných rozměrů zmenšeného obrázku
                resized_h, resized_w = image_cv.shape[:2]
                scale_x = orig_w / float(resized_w)
                scale_y = orig_h / float(resized_h)
                
                # 2. Detekce kandidátů
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

                # 3. Inference neuronové sítě
                net = load_nn_model()
                results = []
                
                output_image = image_cv.copy()
                
                # Příprava transformace odpovídající trénování
                transform_pipeline = transforms.Compose([
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])

                for (x, y, r) in candidates:
                    # Mapování souřadnic zpět na původní obrázek
                    real_x = int(x * scale_x)
                    real_y = int(y * scale_y)
                    # Průměrné měřítko pro poloměr, pokud se poměr stran liší (přibližně)
                    real_r = int(r * max(scale_x, scale_y))
                    
                    # Extrakce výřezu z PŮVODNÍHO obrázku ve vysokém rozlišení
                    crop = utils.extract_coin_image(original_cv, real_x, real_y, real_r)
                    
                    # Příprava pro PyTorch (HWC -> CHW, Normalizace pro ResNet)
                    # Použití standardní pipeline
                    tensor = transform_pipeline(crop)
                    tensor = tensor.unsqueeze(0) # [1, 3, 128, 128]
                    
                    # Odhad (Inference)
                    with torch.no_grad():
                        outputs = net(tensor)
                        probs = F.softmax(outputs, dim=1)
                        predicted_idx = torch.argmax(probs, dim=1).item()
                        predicted_value = COIN_CLASSES[predicted_idx]
                        confidence = probs[0][predicted_idx].item()
                    
                    # Aplikace filtrace podle jistoty
                    if confidence < conf_threshold:
                         # Vykreslení ignorovaného kandidáta červeně (debug)
                         cv2.circle(output_image, (x, y), r, (0, 0, 255), 2)
                         cv2.putText(output_image, f"Ignored ({confidence:.2f})", (x - 40, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                         continue

                    results.append({
                        "value": predicted_value,
                        "confidence": confidence,
                        "position": (x, y)
                    })
                    
                    # Vykreslení výsledku
                    cv2.circle(output_image, (x, y), r, (0, 255, 0), 2)
                    cv2.putText(output_image, f"{predicted_value} Kc", (x - 20, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                # 4. Zobrazení výsledků
                # Převod BGR na RGB pro Streamlit
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
