import cv2

# carregaAlgoritmo = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
carregaAlgoritmo = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

imagem = cv2.imread('C:/Users/tinho/OneDrive/Imagens/WallPapers/imagemteste1.jpg')
#pastaFotos/image4.jpg

imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

faces = carregaAlgoritmo.detectMultiScale(imagemCinza)

print(faces)

for (x, y, w, h) in faces:
    cv2.rectangle(imagem, (x, y), (x + w, y + h), (255, 0, 0), 2)


cv2.imshow('Faces', imagem)
cv2.waitKey()