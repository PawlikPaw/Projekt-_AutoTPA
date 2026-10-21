import os
import cv2
import numpy as np

# Tworzenie struktury folderów testowych
os.makedirs("dataset/images/train", exist_ok=True)
os.makedirs("dataset/labels/train", exist_ok=True)

# Generowanie kilku sztucznych obrazów testowych
for i in range(5):
    # Tworzenie pustego "zdjęcia RTG" (szary obraz 640x640)
    img = np.ones((640, 640, 3), dtype=np.uint8) * 50
    
    # Symulacja 4 punktów kluczowych w losowych miejscach
    points = []
    for _ in range(4):
        px = np.random.uniform(0.2, 0.8)
        py = np.random.uniform(0.2, 0.8)
        points.extend([px, py, 2.0]) # 2.0 oznacza punkt widoczny i oznaczony
        # Rysujemy kropkę na obrazku podglądowym
        cv2.circle(img, (int(px * 640), int(py * 640)), 8, (0, 255, 0), -1)

    # Zapis obrazu
    img_path = f"dataset/images/train/img_{i}.jpg"
    cv2.imwrite(img_path, img)

    # Zapis pliku etykiety (bounding box wokół całości + 4 punkty)
    # Bounding box obejmujący punkty: x_center, y_center, width, height
    label_line = f"0 0.5 0.5 0.8 0.8 " + " ".join(map(str, points))
    
    label_path = f"dataset/labels/train/img_{i}.txt"
    with open(label_path, "w") as f:
        f.write(label_line)

print("Wygenerowano sztuczne dane testowe!")