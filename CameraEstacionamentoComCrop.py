from ultralytics import YOLO
import cv2
import numpy as np # Importe o numpy

# Carrega modelo pré-treinado YOLOv8n
model = YOLO("yolov8n.pt")

# Captura de vídeo da câmera USB (índice 1)
cap = cv2.VideoCapture(1)

total_vagas = 16  # número total de vagas no estacionamento

# --- SUA NOVA LINHA AQUI ---
# Defina a área de corte (x1, y1, x2, y2)
# Você PRECISA ajustar esses valores para a sua câmera
CROP_AREA = (300, 70, 950, 700) # (Exemplo: x_inicio, y_inicio, x_fim, y_fim)
x1_c, y1_c, x2_c, y2_c = CROP_AREA

while True:
    ret, frame_original = cap.read() # Renomeado para frame_original
    if not ret:
        print("Falha ao ler vídeo.")
        break

    # --- SUA SEGUNDA NOVA LINHA AQUI ---
    # Aplica o "crop" ANTES de qualquer processamento
    # IMPORTANTE: O slicing do numpy/OpenCV é [y:y, x:x]
    frame = frame_original[y1_c:y2_c, x1_c:x2_c]
    # ------------------------------------

    # Faz a inferência (detecção) SÓ NO FRAME CORTADO
    results = model(frame)

    # Pega apenas os objetos do tipo "car", "truck", "bus", "motorcycle"
    carros = [box for box in results[0].boxes if int(box.cls) in [2, 3]]

    # --- O RESTO DO SEU CÓDIGO ORIGINAL ---
    
    # Desenha os retângulos em volta dos carros
    for box in carros:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = model.names[int(box.cls)]
        conf = float(box.conf[0])

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Calcula vagas livres (Usando a sua lógica original)
    livres = total_vagas - len(carros)
    cv2.putText(frame, f"Vagas livres: {livres}/{total_vagas}",
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Mostra o vídeo CORTADO em tempo real
    cv2.imshow("Monitoramento (Cropado)", frame)
    
    # (Opcional) Mostra onde está o corte no vídeo original
    cv2.rectangle(frame_original, (x1_c, y1_c), (x2_c, y2_c), (0, 255, 255), 2)
    cv2.imshow("Monitoramento (Original)", frame_original)


    # Pressione ESC para sair
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()