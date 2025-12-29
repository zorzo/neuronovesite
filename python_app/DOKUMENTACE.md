# Dokumentace projektu: Detektor Českých Mincí

Tento dokument slouží jako technická dokumentace k projektu **Detektor Mincí**, který byl vytvořen jako součást splnění podmínek předmětu XNESI/2NESI (Neuronové sítě). Aplikace demonstruje využití **Transfer Learningu** s hlubokými konvolučními neuronovými sítěmi (ResNet18) v kombinaci s klasickými metodami počítačového vidění pro robustní detekci a klasifikaci objektů.

---

## 1. Úvod

Cílem projektu je vytvořit aplikaci schopnou z fotografie identifikovat české mince, určit jejich hodnotu a spočítat celkovou sumu. Aplikace je navržena tak, aby byla robustní vůči běžným nedokonalostem fotografií, jako je rotace mincí, změna osvětlení nebo mírné rozostření.

### Klíčové technologie
*   **Python 3.x**: Hlavní programovací jazyk.
*   **Streamlit**: Framework pro tvorbu webového uživatelského rozhraní.
*   **PyTorch**: Knihovna pro hluboké učení (implementace Transfer Learningu).
*   **Torchvision**: Modely a transformace obrazu (ResNet18).
*   **OpenCV**: Knihovna pro zpracování obrazu (Hough Transform, extrakce, preprocessing).
*   **NumPy**: Práce s maticemi a numerické operace.

---

## 2. Struktura Projektu

Zdrojové kódy se nacházejí v adresáři `python_app/`. Níže je uveden popis jednotlivých souborů:

*   **`app.py`**: Vstupní bod aplikace. Obsahuje logiku uživatelského rozhraní (Streamlit), ovládací prvky pro parametry detekce, normalizaci vstupu pro neuronovou síť a vizualizaci výsledků.
*   **`model.py`**: Definuje architekturu modelu. Využívá předtrénovaný **ResNet18**, u kterého je nahrazena finální plně propojená vrstva, aby odpovídala 6 třídám českých mincí.
*   **`train.py`**: Skript pro trénování modelu (Fine-Tuning). Zajišťuje pokročilou augmentaci dat, normalizaci podle ImageNet standardů a trénovací smyčku.
*   **`utils.py`**: Obsahuje pomocné funkce pro "Computer Vision" část úlohy. Zahrnuje předzpracování obrazu (zachování poměru stran), detekci kruhů s preferencí větších objektů (bimetalické mince) a extrakci výřezů.
*   **`coin_model.pth`**: Uložené váhy natrénovaného modelu.

---

## 3. Princip Fungování

Proces zpracování obrazu probíhá v několika krocích:

1.  **Načtení obrazu**: Uživatel nahraje obrázek přes webové rozhraní.
2.  **Předzpracování (`utils.preprocess_image`)**:
    *   Obrázek je zmenšen pro detekční fázi, ale **je zachován poměr stran**, aby nedocházelo k deformaci kruhů na elipsy.
    *   Vypočtou se škálovací faktory pro mapování souřadnic zpět do originálu.
3.  **Detekce kandidátů (`utils.detect_regions`)**:
    *   Využívá se **Hough Circle Transform**.
    *   Před detekcí se aplikuje jemné rozmazání (Gaussian Blur 5x5) pro redukci šumu.
    *   **Klíčová logika**: Nalezené kruhy jsou seřazeny **sestupně podle poloměru**. To zajišťuje, že u bimetalických mincí (50 Kč) je detekována celá mince (vnější okraj), nikoliv jen vnitřní zlatý střed.
4.  **Extrakce (`utils.extract_coin_image`)**:
    *   Pro každý detekovaný kruh se provede výřez z **původního obrazu v plném rozlišení**.
    *   Přidává se **padding (30 %)**, aby výřez obsahoval i okraj mince a kousek pozadí (kontext).
    *   Výřez je změněn na velikost **224x224 px** (standard pro ResNet).
5.  **Klasifikace (`app.py`, `model.py`)**:
    *   Obrázek je normalizován pomocí statistik ImageNet (mean/std), stejně jako při trénování.
    *   Model ResNet18 určí pravděpodobnost pro jednotlivé třídy.
6.  **Vyhodnocení**:
    *   Výsledky s nízkou jistotou jsou zahozeny (prevence falešných detekcí).
    *   Detekované mince jsou vykresleny do výsledného obrázku.

---

## 4. Implementační Detaily

### A. Neuronová síť (Transfer Learning - ResNet18)
Namísto trénování sítě od nuly (které dříve vedlo k nízké přesnosti ~45 %), využíváme **Transfer Learning**.
*   **Base Model**: ResNet18 (předtrénovaný na ImageNet).
*   **Úprava**: Poslední vrstva (`fc`) je nahrazena novou lineární vrstvou s 6 výstupy (pro mince 1, 2, 5, 10, 20, 50 Kč).
*   **Výhody**: Síť již umí rozpoznávat hrany, textury a základní tvary. Učí se pouze specifické rysy mincí.

### B. Robustnost a Augmentace (`train.py`)
Aby model fungoval v reálných podmínkách, trénovací proces zahrnuje silnou augmentaci dat:
*   **Rotace**: Náhodná rotace o 0–180° (mince nemají "správnou" orientaci).
*   **Affine**: Mírné posuny a změny měřítka (simulace různých vzdáleností).
*   **Color Jitter**: Změny jasu a kontrastu (simulace různého osvětlení).
*   **Omezení odstínu (Hue)**: Změna odstínu je omezena na minimum, aby model rozlišoval mezi materiály.
*   **Random Grayscale**: Náhodný převod na černobílou (pravděpodobnost 50 %) nutí model soustředit se na tvar a ražbu mince, nikoliv pouze na barvu (což pomáhá u mincí s patinou nebo divným nasvícením).

### C. Ladění Parametrů (UI)
Aplikace umožňuje ladit detekční algoritmus:
*   **Max Poloměr**: Zvýšený limit (až 400px), aby bylo možné detekovat mince i na makro snímcích.
*   **Canny/Accumulator**: Slidery pro nastavení citlivosti detekce hran.

---

## 5. Instalace a Spuštění

### Prerekvizity
*   Nainstalovaný Python (3.8+).
*   Knihovny:
    ```bash
    pip install streamlit opencv-python numpy torch torchvision pillow
    ```

### Trénování (volitelné)
Model je již natrénován (`coin_model.pth`). Pokud jej chcete přetrénovat:
1.  Ujistěte se, že složka `czech-coins` je o úroveň výše než `python_app`.
2.  Spusťte:
    ```bash
    cd python_app
    python train.py
    ```

### Spuštění aplikace
```bash
cd python_app
streamlit run app.py
```

---

## 6. Závěr

Projekt úspěšně řeší problém detekce mincí využitím moderních metod hlubokého učení. Přechod na ResNet18 a implementace robustní augmentace zvýšila přesnost klasifikace v náročných podmínkách (rotace, špatné světlo) na úroveň přesahující **95 %** (na validačním setu při tréninku).
