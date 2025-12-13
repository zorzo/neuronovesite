# Dokumentace projektu: Detektor Českých Mincí

Tento dokument slouží jako technická dokumentace k projektu **Detektor Mincí**, který byl vytvořen jako součást splnění podmínek předmětu XNESI/2NESI (Neuronové sítě). Aplikace demonstruje využití konvolučních neuronových sítí (CNN) v kombinaci s klasickými metodami počítačového vidění pro detekci a klasifikaci objektů.

---

## 1. Úvod

Cílem projektu je vytvořit aplikaci schopnou z fotografie identifikovat české mince, určit jejich hodnotu a spočítat celkovou sumu. Aplikace je navržena tak, aby byla uživatelsky přívětivá a zároveň poskytovala technický vhled do procesu detekce.

### Klíčové technologie
*   **Python 3.x**: Hlavní programovací jazyk.
*   **Streamlit**: Framework pro tvorbu webového uživatelského rozhraní.
*   **PyTorch**: Knihovna pro hluboké učení (návrh a trénink neuronové sítě).
*   **OpenCV**: Knihovna pro zpracování obrazu (předzpracování, detekce kandidátů).
*   **NumPy**: Práce s maticemi a numerické operace.

---

## 2. Struktura Projektu

Zdrojové kódy se nacházejí v adresáři `python_app/`. Níže je uveden popis jednotlivých souborů:

*   **`app.py`**: Vstupní bod aplikace. Obsahuje logiku uživatelského rozhraní (Streamlit), ovládací prvky pro parametry detekce a propojuje vizuální část s logikou detekce a klasifikace.
*   **`model.py`**: Definuje architekturu neuronové sítě (`CoinCNN`). Obsahuje třídu modelu a pomocnou funkci pro načtení vah.
*   **`train.py`**: Skript určený pro trénování neuronové sítě. Zajišťuje načtení datasetu, augmentaci dat, trénovací smyčku a validaci modelu.
*   **`utils.py`**: Obsahuje pomocné funkce pro "Computer Vision" část úlohy. Zahrnuje předzpracování obrazu, detekci kruhů (mincí) a extrakci výřezů pro model.
*   **`coin_model.pth`**: Uložené váhy natrénovaného modelu (soubor vznikne po spuštění trénování).

---

## 3. Princip Fungování

Proces zpracování obrazu probíhá v několika krocích:

1.  **Načtení obrazu**: Uživatel nahraje obrázek přes webové rozhraní.
2.  **Předzpracování (`utils.preprocess_image`)**:
    *   Obrázek je převeden do formátu vhodného pro OpenCV.
    *   Je změněna velikost na standardizované rozlišení (512x512) pro konzistentní výsledky detekce kruhů.
3.  **Detekce kandidátů (`utils.detect_regions`)**:
    *   Využívá se **Hough Circle Transform** (Houghova transformace pro kruhy).
    *   Obraz je převeden do odstínů šedi a rozmazán (Blur) pro redukci šumu.
    *   Algoritmus hledá kruhové útvary na základě nastavených parametrů (citlivost, poloměr).
    *   Nalezené kruhy jsou filtrovány, aby se zamezilo duplicitám (překrývající se detekce).
4.  **Extrakce a Klasifikace (`app.py`, `utils.extract_coin_image`, `model.py`)**:
    *   Pro každý detekovaný kruh (kandidáta) se provede výřez z původního obrazu.
    *   Výřez je změněn na velikost **128x128 px**, kterou vyžaduje neuronová síť.
    *   Výřez je normalizován a předán modelu `CoinCNN`.
    *   Model vrátí pravděpodobnosti pro jednotlivé třídy mincí (1, 2, 5, 10, 20, 50 Kč).
5.  **Vyhodnocení a Vizualizace**:
    *   Pokud je "jistota" (confidence) modelu vyšší než nastavený práh, mince je považována za rozpoznanou.
    *   Výsledek je vykreslen do obrazu (zelená kružnice + hodnota).
    *   Aplikace zobrazí celkovou sečtenou hodnotu.

---

## 4. Implementační Detaily

### A. Neuronová síť (`CoinCNN`)
Architektura vychází z klasických konvolučních sítí. Skládá se ze čtyř konvolučních bloků následovaných plně propojenými vrstvami.

*   **Vstup**: 3x128x128 (RGB obrázek).
*   **Vrstvy**:
    1.  Conv2d (3→32) + BatchNorm + ReLU + MaxPool
    2.  Conv2d (32→64) + BatchNorm + ReLU + MaxPool
    3.  Conv2d (64→128) + BatchNorm + ReLU + MaxPool
    4.  Conv2d (128→128) + BatchNorm + ReLU + MaxPool
*   **Klasifikátor**:
    *   Flatten (zploštění).
    *   Linear (Fully Connected) vrstva s 512 neurony + Dropout (0.5).
    *   Výstupní Linear vrstva (počet tříd = 6).

### B. Ladění Parametrů (UI)
Aplikace umožňuje v postranním panelu ladit parametry Houghovy transformace v reálném čase:
*   **Canny Threshold**: Ovlivňuje detekci hran. Vyšší hodnota najde jen velmi výrazné hrany.
*   **Accumulator Threshold**: Ovlivňuje "přísnost" detekce kruhu. Nižší hodnota najde více kruhů (i falešných), vyšší hodnota je konzervativnější.
*   **Threshold Spolehlivosti (Confidence)**: Filtruje predikce modelu, kde si síť není jistá.

---

## 5. Instalace a Spuštění

### Prerekvizity
*   Nainstalovaný Python (doporučeno 3.8+).
*   Nainstalované knihovny ze souboru `requirements.txt` (bude-li k dispozici) nebo ručně:
    ```bash
    pip install streamlit opencv-python-headless numpy torch torchvision pillow
    ```
    *(Poznámka: `opencv-python-headless` je vhodnější pro serverová prostředí, lokálně lze použít i `opencv-python`)*.

### Trénování modelu
Pokud nemáte soubor `coin_model.pth`, je nutné model nejprve natrénovat. Ujistěte se, že máte dataset mincí ve složce `czech-coins` (o úroveň výše než `python_app`).
```bash
cd python_app
python train.py
```
Trénování proběhne po dobu nastaveného počtu epoch (výchozí 60) a model se uloží.

### Spuštění aplikace
```bash
cd python_app
streamlit run app.py
```
Aplikace se otevře ve výchozím webovém prohlížeči (obvykle na adrese `http://localhost:8501`).

---

## 6. Závěr

Tento projekt spojuje teorii zpracování obrazu (Hough Transform pro lokalizaci) s moderním přístupem hlubokého učení (CNN pro klasifikaci). Díky interaktivnímu rozhraní umožňuje uživateli experimentovat s limity obou technologií a sledovat, jak parametry ovlivňují úspěšnost detekce.
