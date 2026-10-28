import os
import cv2
import numpy as np
import pandas as pd

# Automatyczne pobranie ścieżki do folderu 'Points', w którym leży ten skrypt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_points_from_image(image_path):
    """
    Funkcja wykrywające współrzędne 4 punktów na podstawie zielonych linii/znaczników na zdjęciu RTG.
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"Nie znaleziono obrazu: {image_path}")
        return None, None, None

    height, width, _ = img.shape

    # Konwersja do przestrzeni HSV w celu wyizolowania zielonych linii rysowanych przez lekarza
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Zakres koloru zielonego dla linii i oznaczeń
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Znajdowanie konturów lub punktów charakterystycznych zielonego elementu
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    points = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 5:  # odfiltrowanie szumów
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                points.append((cx, cy))

    # Zabezpieczenie, gdyby znaleziono mniej niż 4 punkty
    while len(points) < 4:
        points.append((0, 0))

    # Bierzemy pierwsze 4 znaczące punkty (P1, P2, P3, P4)
    p1, p2, p3, p4 = points[:4]

    return width, height, [p1, p2, p3, p4]

def update_excel_with_extracted_data(excel_filename, image_folder_name):
    # Tworzenie pełnych ścieżek wewnątrz folderu Points
    excel_path = os.path.join(BASE_DIR, excel_filename)
    image_folder = os.path.join(BASE_DIR, image_folder_name)
    
    if not os.path.exists(excel_path):
        print(f"Błąd: Nie znaleziono pliku Excel pod adresem: {excel_path}")
        return

    df = pd.read_excel(excel_path)
    
    for idx, row in df.iterrows():
        case_name = row['case']
        img_type = row['image']  # preop lub postop
        
        # Konwersja np. case_0010 na 10
        case_num = case_name.split('_')[-1].lstrip('0')
        img_filename = f"{case_num}_{img_type}.jpg"
        img_path = os.path.join(image_folder, img_filename)
        
        if os.path.exists(img_path):
            width, height, pts = extract_points_from_image(img_path)
            if pts:
                df.at[idx, 'P1 X (The center of the talus)'] = pts[0][0]
                df.at[idx, 'P1 Y (The center of the talus)'] = pts[0][1]
                df.at[idx, 'P2 X (The center of the intercondylar eminence)'] = pts[1][0]
                df.at[idx, 'P2 Y (The center of the intercondylar eminence)'] = pts[1][1]
                df.at[idx, 'P3 X (Cranial plateau point) '] = pts[2][0]
                df.at[idx, 'P3 Y (Cranial plateau point) '] = pts[2][1]
                df.at[idx, 'P4 X (Caudal plateau point) '] = pts[3][0]
                df.at[idx, 'P4 Y (Caudal plateau point) '] = pts[3][1]
                df.at[idx, 'Image Width'] = width
                df.at[idx, 'Image Height'] = height
                
                print(f"Zaktualizowano wiersz dla: {img_filename}")
        else:
            print(f"Ostrzeżenie: Brak pliku obrazu w folderze dataset_annotated: {img_filename}")

    # Zapis zaktualizowanego pliku Excel
    df.to_excel(excel_path, index=False)
    print("Arkusz Excel został pomyślnie zaktualizowany!")

if __name__ == "__main__":
    # Wywołanie funkcji dla plików znajdujących się w folderze Points
    update_excel_with_extracted_data("Cases_test.xlsx", "dataset_annotated")