from ultralytics import YOLO

def train_model():
    # Załadowanie wstępnie trenowanego modelu YOLO bazującego na zadaniu pose
    model = YOLO("yolov8n-pose.pt")  

    # Uruchomienie treningu
    results = model.train(
        data="data.yaml",
        epochs=10,          # Liczba powtórzeń
        imgsz=640,          # Rozmiar obrazu
        batch=4,            # Rozmiar batcha dopasowany do możliwości karty graficznej
        device="cpu"        
    )

    print("Trening zakończony pomyślnie!")

if __name__ == "__main__":
    # train_model()
    pass