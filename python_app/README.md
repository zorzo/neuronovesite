# Detektor Mincí (Python Streamlit App)

Jednoduchá webová aplikace pro detekci a počítání českých mincí pomocí Počítačového vidění (OpenCV) a Neuronové sítě (PyTorch).
streamlit run c:/Users/spravce/Documents/code/neuronovesite/python_app/app.py

## Instalace

1. Vytvořte virtuální prostředí (doporučeno):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

2. Nainstalujte závislosti:
   ```bash
   pip install -r requirements.txt
   ```

## Spuštění

Spusťte aplikaci pomocí příkazu:
```bash
streamlit run app.py
```

Aplikace se otevře ve vašem prohlížeči (obvykle `http://localhost:8501`).

## Jak to funguje
1. **Nahrání:** Uživatel nahraje obrázek.
2. **Detekce:** OpenCV (`utils.py`) najde "kolečka" (kandidáty na mince).
3. **Klasifikace:** Neuronová síť (`model.py`) určí hodnotu každé mince.
4. **Výsledek:** Zobrazí se anotovaný obrázek a celková suma.


## Trénování Modelu

Pokud chcete model přetrénovat (např. po stažení datasetu):

1. Ujistěte se, že máte dataset ve složce `../czech-coins` (nebo upravte cestu v `train.py`).
2. Spusťte trénování:
   ```bash
   python train.py
   ```
3. Script automaticky uloží nejlepší model do `coin_model.pth`, který aplikace načte.



Dataset z Kaggle se přes Kaggle API stahuje tak, že nejdřív vygeneruješ API token (`kaggle.json`), umístíš ho na správné místo a pak použiješ příkaz `kaggle datasets download -d ...`.[1][2][3]

## 1. Instalace a nastavení API

- Nainstaluj balíček Kaggle API příkazem `pip install kaggle` (Python prostředí / terminál).[2][4]
- Na stránce účtu na Kaggle v sekci „API“ klikni na „Create New API Token“, stáhne se soubor `kaggle.json` a ten ulož:  
  - Linux/macOS: `~/.kaggle/kaggle.json`  
  - Windows: `C:\Users\<uživatel>\.kaggle\kaggle.json`  
  Soubor má obsahovat uživatelské jméno a klíč, které API používá k autentizaci.[5][6][1]

## 2. Stažení datasetu přes CLI

- V terminálu ověř instalaci příkazem `kaggle --help`; pokud proběhla autentizace správně, příkaz proběhne bez chyby.[1][2]
- Pro dataset (např. `janstol/czech-coins`) použij:  
  - `kaggle datasets download -d janstol/czech-coins` – stáhne ZIP do aktuální složky; můžeš přidat `-p cesta/` pro cílovou složku a `--unzip` pro automatické rozbalení.[7][3][8]

## 3. Použití v Pythonu / Colab

- V Jupyter/Colab nejprve nainstaluj CLI příkazem `!pip install kaggle` a nahraj `kaggle.json` do `~/.kaggle/` (v Colabu typicky přes `files.upload()` a `!mkdir -p ~/.kaggle && mv kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json`).[8][7]
- Pak v buňce spusť například `!kaggle datasets download -d janstol/czech-coins --unzip -p data/` a soubory datasetu se rozbalí do adresáře `data/`, odkud je načteš v Pythonu.[9][10][7]

[1](https://www.kaggle.com/docs/api)
[2](https://github.com/Kaggle/kaggle-api)
[3](https://www.kaggle.com/docs/datasets)
[4](https://www.youtube.com/watch?v=LRGwvGQaUiQ)
[5](https://thedeveloperyt.com/how-to-set-up-kaggle-api-in-your-system/)
[6](https://lindevs.com/set-up-kaggle-api)
[7](https://www.youtube.com/watch?v=McAaWvQMG3A)
[8](https://stackoverflow.com/questions/49310470/using-kaggle-datasets-in-google-colab)
[9](https://stackoverflow.com/questions/49310470/using-kaggle-datasets-in-google-colab/50650918)
[10](https://stackoverflow.com/questions/49386920/download-kaggle-dataset-by-using-python)
[11](https://stackoverflow.com/questions/70014366/manually-authenticate-kaggle-api)
[12](https://kaggledatasets.github.io/get-started)
[13](https://pypi.org/project/kagglehub/)
[14](https://www.youtube.com/watch?v=tUSRvV8bTMQ)
[15](https://www.youtube.com/watch?v=F7F31wvyEtY)
[16](https://blog.roboflow.com/how-to-use-kaggle-for-computer-vision/)
[17](https://www.youtube.com/watch?v=krkS9u140tM)
[18](https://www.youtube.com/watch?v=DgGFhQmfxHo)
[19](https://www.reddit.com/r/learnpython/comments/155mler/whats_the_process_for_getting_kaggle_data_into_a/)
[20](https://mmiakashs.github.io/blog/2018-09-20-kaggle-api-google-colab/)