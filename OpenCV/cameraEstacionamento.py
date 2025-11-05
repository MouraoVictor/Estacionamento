import cv2
import numpy as np

carregaAlgoritmo = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")

imagem  = cv2.imread("C:/Users/tinho/OneDrive/Imagens/WallPapers/imagemteste1.jpg")

imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

faces = carregaAlgoritmo.detectMultiScale(imagemCinza)

print(faces)

cv2.imshow("Imagem", imagem)
cv2.imshow("Imagem", faces)

cv2.waitKey(0)
cv2.destroyAllWindows()