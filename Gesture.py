import cv2
import numpy as np
import math


camera = cv2.VideoCapture(0)

while(True):
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    #kernel = np.ones((3, 3), np.uint8)

    # definiowanie frame czarno bialego
    image_BlackAndWhite = frame[50:300, 50:300]

    #wyswietlanie zielonego prostokata, rozmiar
    cv2.rectangle(frame, (50, 50), (300, 300), (0, 255, 0), 0)
    #zmiana koloru na rgb na hsv w framie czarno bialym
    hsv = cv2.cvtColor(image_BlackAndWhite, cv2.COLOR_BGR2HSV)

    #HSV - definiowanie kolorów do detekcji skóry
    lowerSkinColor = np.array([0, 48, 80])
    upperSkinColor = np.array([20, 255, 255])

    #znajdywanie koloru skóry
    mask = cv2.inRange(hsv, lowerSkinColor, upperSkinColor)

    cv2.imshow('mask', mask)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(5)
    if k == 27:
        break

cv2.destroyAllWindows()
camera.release()