# imports
from ultralytics import YOLO
import cv2
import numpy as np
import winsound
import threading
import sys

# CONFIGURAÇÃO DE DESIGN (TEMA "EMPRESARIAL")
# Cores
COR_AZUL_EMPRESA = (210, 100, 0)
COR_AZUL_ESCURO_GRAD = (50, 20, 0)
COR_CINZA_ESCURO = (50, 50, 50)
COR_CINZA_CLARO = (180, 180, 180) 
COR_BRANCO = (255, 255, 255)
COR_VERMELHO_ALERTA = (0, 0, 220)
COR_VERMELHO_BOTAO = (0, 0, 150)
COR_VERMELHO_BOTAO_HOVER = (0, 0, 200)
COR_VERDE_OK = (0, 180, 0)
COR_VERDE_BOTAO = (0, 150, 0)
COR_VERDE_BOTAO_HOVER = (0, 200, 0)

# Transparência dos Painéis
OPACIDADE_PAINEL = 0.6

# Fontes
FONTE_PRINCIPAL = cv2.FONT_HERSHEY_DUPLEX

# BOTÕES E ESTADO DO PROGRAMA
BTN_INICIAR_COORDS = (50, 220, 450, 290) 
BTN_SAIR_COORDS = (100, 310, 400, 380)
BTN_SAIR_MAIN_COORDS = (530, 15, 630, 55) 

program_state = {"action": "wait", "mouse_pos": (0, 0)}

# Funções do Mouse
def handle_start_click(event, x, y, flags, param):
    program_state["mouse_pos"] = (x, y) 
    if event == cv2.EVENT_LBUTTONDOWN:
        if (BTN_INICIAR_COORDS[0] < x < BTN_INICIAR_COORDS[2] and 
            BTN_INICIAR_COORDS[1] < y < BTN_INICIAR_COORDS[3]):
            program_state["action"] = "start"
        if (BTN_SAIR_COORDS[0] < x < BTN_SAIR_COORDS[2] and 
            BTN_SAIR_COORDS[1] < y < BTN_SAIR_COORDS[3]):
            program_state["action"] = "quit"

def handle_main_click(event, x, y, flags, param):
    program_state["mouse_pos"] = (x, y)
    if event == cv2.EVENT_LBUTTONDOWN:
        if (BTN_SAIR_MAIN_COORDS[0] < x < BTN_SAIR_MAIN_COORDS[2] and
            BTN_SAIR_MAIN_COORDS[1] < y < BTN_SAIR_MAIN_COORDS[3]):
            program_state["action"] = "quit"

# FUNÇÕES DE INTERFACE (UI)

# FUNÇÃO AUXILIAR
def create_gradient_background(height, width, color_top_bgr, color_bottom_bgr):
    """Cria um fundo com gradiente vertical usando NumPy."""
    # Cria um array 1D para a interpolação de 'height'
    gradient = np.linspace(0, 1, height).reshape(height, 1, 1)
    
    # Converte cores para float para interpolação
    color_top = np.array(color_top_bgr, dtype=np.float32)
    color_bottom = np.array(color_bottom_bgr, dtype=np.float32)
    
    # Interpola as cores
    gradient_3d = (1 - gradient) * color_top + gradient * color_bottom
    
    # "Estica" o gradiente 1D (Hx1x3) para a largura total (HxWx3)
    background = np.tile(gradient_3d, (1, width, 1)).astype(np.uint8)
    return background

# FUNÇÃO DE BOTÃO ATUALIZADA
def draw_button(img, text, coords, mouse_pos, is_start_button=True):
    """Desenha um botão profissional com borda e efeito hover."""
    x1, y1, x2, y2 = coords
    mx, my = mouse_pos
    is_hovering = (x1 < mx < x2 and y1 < my < y2)

    # Define cores com base no tipo e hover
    if is_start_button:
        cor_fill = COR_VERDE_BOTAO_HOVER if is_hovering else COR_VERDE_BOTAO
        border_color = COR_VERDE_OK
    else:
        cor_fill = COR_VERMELHO_BOTAO_HOVER if is_hovering else COR_VERMELHO_BOTAO
        border_color = COR_VERMELHO_ALERTA

    # Desenha a borda (retângulo maior)
    cv2.rectangle(img, (x1, y1), (x2, y2), border_color, -1)
    # Desenha o preenchimento (um pouco menor para a borda aparecer)
    cv2.rectangle(img, (x1 + 2, y1 + 2), (x2 - 2, y2 - 2), cor_fill, -1)
    
    # Centraliza o texto
    (w, h), _ = cv2.getTextSize(text, FONTE_PRINCIPAL, 0.8, 2)
    text_x = x1 + (x2 - x1 - w) // 2
    text_y = y1 + (y2 - y1 + h) // 2
    cv2.putText(img, text, (text_x, text_y), FONTE_PRINCIPAL, 0.8, COR_BRANCO, 2)

# TELA INICIAL ATUALIZADA
def show_start_screen():
    """Cria e exibe a tela inicial profissional (V2)."""
    
    # Cria o fundo com gradiente
    start_screen_img = create_gradient_background(450, 500, COR_AZUL_EMPRESA, COR_AZUL_ESCURO_GRAD)
    
    window_name = "Sistema de Monitoramento"
    cv2.imshow(window_name, start_screen_img)
    cv2.setMouseCallback(window_name, handle_start_click)

    # "logo (câmera)"
    center_x, center_y = 250, 75
    # Lente externa
    cv2.circle(start_screen_img, (center_x, center_y), 50, COR_CINZA_ESCURO, -1)
    # Borda da lente
    cv2.circle(start_screen_img, (center_x, center_y), 45, COR_CINZA_CLARO, 4)
    # Lente interna
    cv2.circle(start_screen_img, (center_x, center_y), 35, (10, 10, 10), -1) # Preto
    # Reflexo
    cv2.circle(start_screen_img, (center_x + 15, center_y - 15), 5, COR_BRANCO, -1)
    
    # Título e Subtítulo
    cv2.putText(start_screen_img, "Sistema de Monitoramento", (40, 170),
                FONTE_PRINCIPAL, 1, COR_BRANCO, 2)
    cv2.putText(start_screen_img, "Estacionamento Inteligente", (120, 195),
                FONTE_PRINCIPAL, 0.6, COR_CINZA_CLARO, 1)
    
    # Linha divisória e Footer
    cv2.line(start_screen_img, (50, 410), (450, 410), COR_CINZA_CLARO, 1)
    cv2.putText(start_screen_img, "Versao 1.5.1", (390, 430),
                FONTE_PRINCIPAL, 0.4, COR_CINZA_CLARO, 1)

    while True:
        # Copia a tela base para redesenhar os botões (para o hover)
        frame_botoes = start_screen_img.copy()
        
        mx, my = program_state["mouse_pos"]
        
        # Desenha Botões
        draw_button(frame_botoes, "INICIAR MONITORAMENTO (S)", BTN_INICIAR_COORDS, (mx, my), is_start_button=True)
        draw_button(frame_botoes, "SAIR DO SISTEMA (Q)", BTN_SAIR_COORDS, (mx, my), is_start_button=False)

        cv2.imshow(window_name, frame_botoes)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'): program_state["action"] = "start"
        elif key == ord('q'): program_state["action"] = "quit"
        if program_state["action"] != "wait": break
            
    cv2.destroyWindow(window_name) 
    return program_state["action"]

# Alerta sonoro
def tocar_alerta_async():
    winsound.Beep(1000, 500) 

# EXECUÇÃO PRINCIPAL DO PROGRAMA

# MOSTRA A TELA INICIAL e espera a ação
# A linha abaixo agora chama a NOVA show_start_screen()
action = show_start_screen()

# SE O USUÁRIO CLICOU EM "INICIAR", RODA O SEU CÓDIGO
if action == "start":

    print("Iniciando monitoramento...")
    
    model = YOLO("yolov8n.pt")
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a câmera.")
        sys.exit() 

    total_vagas = 8
    CROP_AREA = (300, 70, 950, 600) 
    x1_c, y1_c, x2_c, y2_c = CROP_AREA
    
    FRAME_W = x2_c - x1_c
    FRAME_H = y2_c - y1_c

    alerta_pessoa_ativo = False
    
    main_window_name = "Monitoramento de Estacionamento"
    cv2.namedWindow(main_window_name)
    cv2.setMouseCallback(main_window_name, handle_main_click)
    program_state["action"] = "run" 

    while True:
        ret, frame_original = cap.read() 
        if not ret: break

        frame = frame_original[y1_c:y2_c, x1_c:x2_c]
        results = model(frame)

        classes_carros = [2, 3, 7] 
        classe_pessoa = 0
        carros = []
        pessoas_detectadas = []

        for box in results[0].boxes:
            cls_id = int(box.cls)
            if cls_id in classes_carros:
                carros.append(box)
            elif cls_id == classe_pessoa:
                pessoas_detectadas.append(box)
        
        livres = total_vagas - len(carros)

        if len(pessoas_detectadas) > 0:
            if not alerta_pessoa_ativo:
                print("ALERTA: Pessoa detectada dentro da área!")
                threading.Thread(target=tocar_alerta_async).start()
                alerta_pessoa_ativo = True  
            status_cor = COR_VERMELHO_ALERTA
            status_texto = "ALERTA: PESSOA"
        else:
            if alerta_pessoa_ativo:
                print("Área livre de pessoas.")
                alerta_pessoa_ativo = False
            status_cor = COR_VERDE_OK
            status_texto = "STATUS: SEGURO"

        for box in carros:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), COR_AZUL_EMPRESA, 2) 
        
        for box in pessoas_detectadas:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), COR_VERMELHO_ALERTA, 2)
            cv2.putText(frame, "PESSOA", (x1, y1 - 10), FONTE_PRINCIPAL, 0.6, COR_BRANCO, 2)

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (FRAME_W, 70), COR_CINZA_ESCURO, -1)
        cv2.rectangle(overlay, (0, FRAME_H - 70), (FRAME_W, FRAME_H), COR_CINZA_ESCURO, -1)
        frame_com_ui = cv2.addWeighted(overlay, OPACIDADE_PAINEL, frame, 1 - OPACIDADE_PAINEL, 0)
        
        cv2.putText(frame_com_ui, "SISTEMA DE MONITORAMENTO", (20, 45), 
                    FONTE_PRINCIPAL, 0.9, COR_BRANCO, 2)
        cv2.putText(frame_com_ui, f"VAGAS LIVRES: {livres}/{total_vagas}", (20, FRAME_H - 25), 
                    FONTE_PRINCIPAL, 1, COR_BRANCO, 2)
        
        cv2.rectangle(frame_com_ui, (FRAME_W - 270, FRAME_H - 70), (FRAME_W, FRAME_H), status_cor, -1)
        cv2.putText(frame_com_ui, status_texto, (FRAME_W - 255, FRAME_H - 25), 
                    FONTE_PRINCIPAL, 0.9, COR_BRANCO, 2)
        
        draw_button(frame_com_ui, "SAIR", BTN_SAIR_MAIN_COORDS, 
                    program_state["mouse_pos"], is_start_button=False)

        # Fim do Desenho da UI Principal

        cv2.imshow(main_window_name, frame_com_ui) 

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or program_state["action"] == "quit":
            print("Encerrando monitoramento...")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Monitoramento encerrado.")

else:
    print("Programa encerrado pelo usuário na tela inicial.")
    sys.exit()