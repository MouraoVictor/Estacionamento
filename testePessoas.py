from ultralytics import YOLO
import cv2
import numpy as np
import winsound  # Sons
import threading

# Modelo pré-treinado para detecção
model = YOLO("yolov8n.pt")

# Conecta à câmera USB (índice 1) (Celular)
cap = cv2.VideoCapture(1)

total_vagas = 16  # número total de vagas no estacionamento

# Define a área de Crop da imagem
CROP_AREA = (300, 70, 950, 700) # (x_inicio, y_inicio, x_fim, y_fim)
x1_c, y1_c, x2_c, y2_c = CROP_AREA

# Para o alarme não disparar ao iniciar
alerta_pessoa_ativo = False

# Alerta sonoro
def tocar_alerta_async():
    """Toca o som de alerta em uma thread separada."""
    winsound.Beep(1000, 500) 

while True:
    ret, frame_original = cap.read() 
    if not ret:
        print("Falha ao ler vídeo.")
        break

    # Aplica o Crop
    frame = frame_original[y1_c:y2_c, x1_c:x2_c]
    
    # Faz a inferência
    results = model(frame)

    # Encontra os carros
    classes_carros = [2, 3, 7]
    carros = [box for box in results[0].boxes if int(box.cls) in classes_carros]

    # Desenha retângulo nos carros
    for box in carros:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) 

    # Calcula vagas livres
    livres = total_vagas - len(carros)
    cv2.putText(frame, f"Vagas livres: {livres}/{total_vagas}",
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
    # Detecção de Pessoas 
    classe_pessoa = 0
    pessoas_detectadas = [box for box in results[0].boxes if int(box.cls) == classe_pessoa]

    if len(pessoas_detectadas) > 0:
        if not alerta_pessoa_ativo:
            print("ALERTA: Pessoa detectada dentro da área!")
            
            threading.Thread(target=tocar_alerta_async).start()
            
            alerta_pessoa_ativo = True  

        # Desenha retângulo nas pessoas
        for box in pessoas_detectadas:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, "PESSOA", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    else:
        # Caso não haja pessoas
        if alerta_pessoa_ativo:
            print("Área livre de pessoas.")
            alerta_pessoa_ativo = False

    # Mostra os vídeos
    cv2.imshow("Monitoramento (Cropado)", frame)
    
    # para mostrar a imagem original com o retângulo do crop:
    # cv2.imshow("Monitoramento (Original)", frame_original)

    # ESC para sair
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()