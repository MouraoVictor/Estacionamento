from ultralytics import YOLO
import cv2
import numpy as np
import winsound  # <- NOVO: Para tocar o som (substitui beepy)
import threading # <- NOVO: Para não travar o vídeo

# Carrega modelo pré-treinado YOLOv8n
model = YOLO("yolov8n.pt")

# Captura de vídeo da câmera USB (índice 1)
cap = cv2.VideoCapture(1)

total_vagas = 16  # número total de vagas no estacionamento

# Defina a área de corte (x1, y1, x2, y2)
CROP_AREA = (150, 200, 800, 500) # (Exemplo: x_inicio, y_inicio, x_fim, y_fim)
x1_c, y1_c, x2_c, y2_c = CROP_AREA

# Flag para controlar o alarme
alerta_pessoa_ativo = False

# --- NOVA FUNÇÃO DE ALERTA ---
def tocar_alerta_async():
    """Toca o som de alerta em uma thread separada."""
    # Frequência em Hz, Duração em milissegundos
    winsound.Beep(1000, 500) 
# ------------------------------

while True:
    ret, frame_original = cap.read() 
    if not ret:
        print("Falha ao ler vídeo.")
        break

    # Aplica o "crop"
    frame = frame_original[y1_c:y2_c, x1_c:x2_c]
    
    # Faz a inferência
    results = model(frame)

    # --- LÓGICA DE CARROS ---
    classes_carros = [2, 3, 5, 7]
    carros = [box for box in results[0].boxes if int(box.cls) in classes_carros]
    # ... (desenho dos carros) ...
    for box in carros:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2) 

    # Calcula vagas livres
    livres = total_vagas - len(carros)
    cv2.putText(frame, f"Vagas livres: {livres}/{total_vagas}",
                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
    # --- LÓGICA DE DETECÇÃO DE PESSOAS ---
    classe_pessoa = 0  # A classe 'person' é a 0
    pessoas_detectadas = [box for box in results[0].boxes if int(box.cls) == classe_pessoa]

    if len(pessoas_detectadas) > 0:
        if not alerta_pessoa_ativo:
            print("ALERTA: Pessoa detectada dentro da área!")
            
            # --- MODIFICADO ---
            # Inicia o som em uma thread para não travar o loop principal
            threading.Thread(target=tocar_alerta_async).start()
            # ------------------
            
            alerta_pessoa_ativo = True  

        # Desenha caixas nas pessoas
        for box in pessoas_detectadas:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2) # Amarelo
            cv2.putText(frame, "PESSOA", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    else:
        # Se não há pessoas, reseta o "trava" do alarme
        if alerta_pessoa_ativo:
            print("Área livre de pessoas.")
            alerta_pessoa_ativo = False

    # Mostra os vídeos
    cv2.imshow("Monitoramento (Cropado)", frame)
    cv2.imshow("Monitoramento (Original)", frame_original)

    # Pressione ESC para sair
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()