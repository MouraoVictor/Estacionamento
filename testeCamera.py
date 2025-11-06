import cv2
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Não conseguiu acessar a câmera.")
        break

    cv2.imshow("Câmera USB do celular", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()