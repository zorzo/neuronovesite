# Implementační Plán: Streamlit Aplikace pro Detekci Mincí

**Cíl:** Nahradit komplexní "Full Stack" (Next.js/FastAPI) řešení jednoduchou a elegantní "Pure Python" aplikací pomocí frameworku **Streamlit**. Aplikace bude splňovat zadání (využití neuronových sítí).

## User Review Required
> [!IMPORTANT]
> **Framework Choice:** Navrhuji použít **PyTorch** + **OpenCV**. PyTorch je moderní standard pro výuku i praxi. Pokud preferujete TensorFlow/Keras, dejte vědět.

## Proposed Changes

Vytvoření nové složky `python_app` v kořeni workspace. Původní `pocitani_minci` bude zachováno jako reference (nebo později smazáno).

### Structure
```
python_app/
├── app.py              # Hlavní Streamlit aplikace (UI + logika)
├── model.py            # Definice architektury neuronové sítě (CNN)
├── utils.py            # Pomocné funkce pro zpracování obrazu (OpenCV)
├── requirements.txt    # Závislosti (streamlit, torch, opencv-python...)
└── README.md           # Návod na spuštění
```

### 1. `python_app/requirements.txt`
- `streamlit`
- `torch` (PyTorch)
- `torchvision`
- `opencv-python-headless` (pro zpracování obrazu)
- `numpy`
- `pillow`

### 2. `python_app/model.py`
- Třída `CoinCNN(nn.Module)`: Jednoduchá konvoluční síť (Convolutional Neural Network).
- Vstup: Obrázek (např. 64x64px výřez mince).
- Výstup: Klasifikace hodnoty mince (1, 2, 5, 10, 20, 50 Kč).

### 3. `python_app/utils.py`
- Funkce pro detekci kandidátních oblastí (region proposals) pomocí OpenCV (převzato a zjednodušeno z původního projektu - `cv2.HoughCircles` nebo kontury).
- *Poznámka:* Použijeme hybridní přístup: OpenCV najde "kolečka" (což umí skvěle a rychle), Neuronová síť pak každé "kolečko" rozpozná (klasifikuje). To je robustní a splňuje zadání použití NN.

### 4. `python_app/app.py`
- **Upload Widget:** Pro nahrání fotky.
- **Visualizace:** Zobrazení původní fotky s vykreslenými detekcemi a hodnotami.
- **Statistika:** Tabulka s počtem a celkovou sumou.
- **Interaktivita:** Možnost upravit parametry detekce posuvníky (thresholding), aby uživatel viděl "jak to funguje".

## Verification Plan

### Automated Tests
- Spuštění aplikace: `streamlit run python_app/app.py`
- Unit test pro `model.py` (ověření rozměrů tenzorů).

### Manual Verification
1.  Spustit aplikaci.
2.  Nahrát testovací obrázek mincí.
3.  Ověřit, že aplikace:
    - Detekuje mince (kroužky).
    - Zobrazí fiktivní/náhodnou predikci (dokud nebude model natrénovaný) nebo jednoduchou heuristiku.
    - "Nespadne" na chybách.


# Průvodce: Nová Aplikace "Detektor Mincí"

Tento dokument popisuje nově vytvořenou aplikaci v čistém Pythonu (`python_app/`), která nahrazuje původní složité řešení.

## 1. Co bylo vytvořeno
Byla vytvořena nová složka `python_app` obsahující:
- **[app.py](file:///c:/Users/spravce/Documents/code/neuronovesite/python_app/app.py)**: Webová aplikace postavená na frameworku **Streamlit**.
- **[model.py](file:///c:/Users/spravce/Documents/code/neuronovesite/python_app/model.py)**: Definice konvoluční neuronové sítě (CNN) v **PyTorch**.
- **[utils.py](file:///c:/Users/spravce/Documents/code/neuronovesite/python_app/utils.py)**: Logika pro předzpracování obrazu a detekci kandidátů pomocí **OpenCV**.
- **[requirements.txt](file:///c:/Users/spravce/Documents/code/neuronovesite/python_app/requirements.txt)**: Seznam potřebných knihoven.

## 2. Architektura
Aplikace kombinuje to nejlepší z obou světů pro splnění zadání:
1.  **OpenCV** rychle najde na obrázku "kolečka" (kandidáty na mince).
2.  **Neuronová síť (CNN)** následně každé kolečko klasifikuje (určí jeho hodnotu).

Tím je splněna podmínka zadání ("aplikace z oblasti neuronových sítí"), aniž by se muselo řešit složité trénování detekční sítě (YOLO/SSD), což by bylo pro tento účel zbytečně náročné.

## 3. Jak spustit aplikaci
V terminálu přejděte do složky projektu a spusťte:

```bash
# 1. (Volitelné) Vytvoření virtuálního prostředí
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Instalace závislostí
pip install -r python_app/requirements.txt

# 3. Spuštění aplikace
streamlit run python_app/app.py
```

## 4. Další kroky (Trénování)
Aktuálně aplikace používá **nenatrénovaný model** (náhodné váhy), takže detekuje mince správně (díky OpenCV), ale "hádá" jejich hodnoty náhodně.

Pro dokončení projektu je třeba:
1.  Vytvořit dataset výřezů mincí (lze použít aplikaci k jejich uložení).
2.  Dopsat trénovací smyčku (např. `train.py`), která naučí model v [model.py](file:///c:/Users/spravce/Documents/code/neuronovesite/python_app/model.py) rozeznávat mince.
3.  Nahrát natrénované váhy (`model.load_state_dict`).
