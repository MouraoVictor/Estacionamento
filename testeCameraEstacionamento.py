from ultralytics import YOLO
import cv2

# Carrega modelo pré-treinado YOLOv8n
model = YOLO("yolov8n.pt")

# Captura de vídeo da câmera USB (índice 1)
cap = cv2.VideoCapture(1)

total_vagas = 16  # número total de vagas no estacionamento

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao ler vídeo.")
        break

    # Faz a inferência (detecção)
    results = model(frame)

    # Pega apenas os objetos do tipo "car", "truck", "bus", "motorcycle"
    carros = [box for box in results[0].boxes if int(box.cls) in [2, 3, 5, 7]]

    # Desenha os retângulos em volta dos carros
    for box in carros:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = model.names[int(box.cls)]
        conf = float(box.conf[0])

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Calcula vagas livres
    livres = total_vagas - len(carros)
    cv2.putText(frame, f"Vagas livres: {livres}/{total_vagas}",
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Mostra o vídeo em tempo real
    cv2.imshow("Monitoramento do Estacionamento", frame)

    # Pressione ESC para sair
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
