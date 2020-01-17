import cv2
import numpy as np
import math
import time

camera = cv2.VideoCapture(0)

while(True):
    # bez try i except program konczy prace gdy w ramce nie ma obiektu - error
    try:
        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)
        # definiowanie ramki czarno-bialej
        image_BlackAndWhite = frame[50:350, 50:350]
        # wyswietlanie zielonego prostokata, rozmiar
        cv2.rectangle(frame, (50, 50), (350, 350), (0, 255, 0), 2)
        # zmiana koloru na rgb na hsv w framie czarno bialym
        hsv = cv2.cvtColor(image_BlackAndWhite, cv2.COLOR_BGR2HSV)
        # HSV - definiowanie kolorów do detekcji skóry
        lowerSkinColor = np.array([0, 20, 70])
        upperSkinColor = np.array([20, 255, 255])
        # znajdowanie reki zdefiniowane poprzez kolory hsv
        whiteHand = cv2.inRange(hsv, lowerSkinColor, upperSkinColor)
        contours, hierarchy = cv2.findContours(whiteHand, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key=lambda x: cv2.contourArea(x))
        # rysowanie przyblizonego konturu? approx the contour a little
        epsilon = cv2.arcLength(cnt, True) * 0.0005
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        # tworzenie wypuklego obrysu wokol dloni
        hull = cv2.convexHull(cnt)
        # definiowanie obszaru obrysu i obszaru dloni
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
        # szukanie procentowej wartosci obszaru w obrysie nieobejmujacego dloni
        arearatio = ((areahull - areacnt) / areacnt) * 100
        # szukanie defektow (palcow) w wypukłym obrysie w odniesieniu do ręki
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
        # palce liczba "defektow"
        finger = 0

        # fragment kodu szukajacy liczby palcow ("defektow")
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            pt = (100, 180)

            # szukanie dlugosci kazdego boku trojkata
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            s = (a + b + c) / 2
            ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

            # odleglosc miedzy punktem a wypuklym obrysem
            d = (2 * ar) / a

            # uzycie cosinusa
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

            # ignorowanie katow >90 i punktow bardzo blisko obrysu (30) (sa to zwykle zaklocenia)
            if angle <= 90 and d > 40:
                finger += 1
                cv2.circle(image_BlackAndWhite, far, 3, [255, 0, 0], -1)

            # rysowanie lini dookola reki
            cv2.line(image_BlackAndWhite, start, end, [0, 255, 0], 2)

        finger += 1

        # wypisywanie odpowiednich gestow

        if finger == 1:
            if areacnt < 2000:
                cv2.putText(frame, 'Umiesc dlon ramce', (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 51, 0), 3)
            else:
                #bylo 12
                if arearatio < 75:
                    cv2.putText(frame, 'Piesc', (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 51, 0), 3)


        elif finger == 2:
            cv2.putText(frame, 'Pokoj', (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 51, 0), 3)

        elif finger == 5:
            cv2.putText(frame, 'Piatka', (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 51, 0), 3)

        cv2.imshow('Podglad', whiteHand)
        cv2.imshow('Ramka', frame)
    except:
        pass

    #zamykanie okien przyciskiem ESC
    k = cv2.waitKey(5)
    if k == 27:
        break

cv2.destroyAllWindows()
camera.release()