import cv2
import os

# --- Recommended Fix for Cascade Path ---
cascade_file = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
carregaAlgoritmo = cv2.CascadeClassifier(cascade_file)
# ----------------------------------------

# --- Check if the Cascade Classifier loaded successfully ---
if carregaAlgoritmo.empty():
    print("ERROR: Cascade Classifier failed to load. Check the file path.")
    exit()
# -----------------------------------------------------------

imagem = cv2.imread("C:/Users/tinho/OneDrive/Imagens/WallPapers/imagemteste1.jpg")

# --- Check for Image Loading Error ---
if imagem is None:
    print("ERROR: Could not load image. Check the image file path.")
    exit()
# -------------------------------------

imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

faces = carregaAlgoritmo.detectMultiScale(imagemCinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

print(faces)

# Draw rectangles around detected faces
for (x, y, w, h) in faces:
    cv2.rectangle(imagem, (x, y), (x+w, y+h), (0, 255, 0), 2)

# Show the image with detected faces
cv2.imshow("Imagem", imagem)

cv2.waitKey(0)
cv2.destroyAllWindows()