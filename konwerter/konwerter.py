import os
import pydicom
import numpy as np
from PIL import Image

#LOGIKA KONWERSJI
def konwertuj_plik(sciezka_dcm, sciezka_png):

    # 1. Wczytanie pliku DICOM
    dane_dicom = pydicom.dcmread(sciezka_dcm)
    
    # 2. Wyciągnięcie samych pikseli jako liczb z przecinkiem (float)
    piksele = dane_dicom.pixel_array.astype(float)
    
    # 3. Przeskalowanie jasności do przedziału 0 - 255
    minimum = np.min(piksele)
    maksimum = np.max(piksele)
    piksele = (piksele - minimum) / (maksimum - minimum) * 255.0
    
    # 4. Zaokrąglenie do liczb całkowitych (format 8-bitowy)
    piksele = piksele.astype(np.uint8)
    
    # 5. Zapisanie jako zwykły obraz PNG
    obraz = Image.fromarray(piksele)
    obraz.save(sciezka_png)


#PRZESZUKIWANIE I KONWERTOWANIA KATALOGU
folder_wejsciowy = "surowe_dicom"
folder_wyjsciowy = "gotowe_png"

# Tworzy folder na gotowe zdjęcia (jeśli jeszcze go nie ma)
os.makedirs(folder_wyjsciowy, exist_ok=True)

# Pętla przechodząca przez wszystkie pliki w folderze wejściowym
for nazwa_pliku in os.listdir(folder_wejsciowy):
    if nazwa_pliku.endswith(".dcm"):
        sciezka_wejsciowa = folder_wejsciowy + "/" + nazwa_pliku
        
        nowa_nazwa = nazwa_pliku.replace(".dcm", ".png")
        sciezka_wyjsciowa = folder_wyjsciowy + "/" + nowa_nazwa
        
        konwertuj_plik(sciezka_wejsciowa, sciezka_wyjsciowa)
        print("Przekonwertowano:", nazwa_pliku)