import sys
import os
import time
import threading
from queue import Queue
from collections import deque

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
from util.Alfabeto import Alfabeto

voz = pyttsx3.init()
voz.setProperty('volume', 1.0)
voz.setProperty('rate', 120)
fila_fala = Queue()

def thread_fala():
    while True:
        texto = fila_fala.get()
        if texto is None:
            break
        voz.say(texto)
        voz.runAndWait()

threading.Thread(target=thread_fala, daemon=True).start()

def falar(texto):
    fila_fala.put(texto)

alfabeto = Alfabeto()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,max_num_hands=2,min_detection_confidence=0.7,min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

fundo_escuro = np.zeros((480, 640, 3), dtype=np.uint8)
cor_texto = (0, 255, 0) 
cor_limpeza = (0, 0, 255)  

fiap = cv2.imread("images/fiap.png")
fiap = cv2.resize(fiap, (200,200))
mostrar_fiap = False
tempo_fiap = 0
frase_fiap = "FIAP"

eae = cv2.imread("images/eae.png")
eae = cv2.resize(eae, (200,200))
eae_hsv = cv2.cvtColor(eae, cv2.COLOR_BGR2HSV)
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])
mask = cv2.inRange(eae_hsv, lower_white, upper_white)
mask_inv = cv2.bitwise_not(mask)
eae_sem_fundo = cv2.bitwise_and(eae, eae, mask=mask_inv)
mostrar_eae = False
tempo_eae = 0
frase_eae = "EAE"

frase = ""
ultima_letra = ""
ultimo_tempo = time.time()
tempo_entre_letras = 2
mostrar_limpeza = False
tempo_limpeza = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    output = fundo_escuro.copy()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(output, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if len(results.multi_hand_landmarks) == 2:
            ambas_abertas = all(
                all(hand_landmarks.landmark[dedo].y < hand_landmarks.landmark[dedo-2].y 
                    for dedo in [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP])
                for hand_landmarks in results.multi_hand_landmarks)
            
            if ambas_abertas and time.time() - tempo_limpeza > 2:
                frase = ""
                ultima_letra = ""
                mostrar_limpeza = True
                tempo_limpeza = time.time()

        elif len(results.multi_hand_landmarks) == 1:
            hand = results.multi_hand_landmarks[0]
            letra = None
            if alfabeto.letra_A(hand): letra = "A"
            elif alfabeto.letra_B(hand): letra = "B"
            elif alfabeto.letra_C(hand): letra = "C"
            elif alfabeto.letra_D(hand): letra = "D"
            elif alfabeto.letra_E(hand): letra = "E"
            elif alfabeto.letra_F(hand): letra = "F"
            elif alfabeto.letra_G(hand): letra = "G"
            elif alfabeto.letra_I(hand): letra = "I"
            elif alfabeto.letra_L(hand): letra = "L"
            elif alfabeto.letra_O(hand): letra = "O"
            elif alfabeto.letra_M(hand): letra = "M"
            elif alfabeto.letra_N(hand): letra = "N"
            elif alfabeto.letra_P(hand): letra = "P"

            if letra and letra != ultima_letra and time.time() - ultimo_tempo > tempo_entre_letras:
                frase += letra
                ultima_letra = letra
                ultimo_tempo = time.time()
                #falar(letra)

                if frase == frase_fiap and not mostrar_fiap:
                    falar(frase_fiap)
                    mostrar_fiap = True
                    tempo_fiap = time.time()
                
                if frase == frase_eae and not mostrar_eae:
                    falar(frase_eae)
                    mostrar_eae = True
                    tempo_eae = time.time()

    if mostrar_limpeza:
        if time.time() - tempo_limpeza < 1:
            cv2.putText(output, "FRASE LIMPA!", (output.shape[1]//2 - 200, output.shape[0]//2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, cor_limpeza, 3)
        else:
            mostrar_limpeza = False

    cv2.putText(output, f"FRASE: {frase}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, cor_texto, 2)
    cv2.putText(output, f"Proxima em: {max(0, tempo_entre_letras - (time.time() - ultimo_tempo)):.1f}s", 
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    img_pequena = cv2.resize(img, (160, 120))
    output[360:480, 480:640] = img_pequena

    if mostrar_fiap and time.time() - tempo_fiap < 2:
        output[100:300, 220:420] = fiap
    else:
        mostrar_fiap = False

    if mostrar_eae and time.time() - tempo_eae < 2:
        roi = output[100:300, 220:420]
        img_fg = cv2.bitwise_and(eae_sem_fundo, eae_sem_fundo)
        img_bg = cv2.bitwise_and(roi, roi, mask=mask)
        dst = cv2.add(img_bg, img_fg)
        output[100:300, 220:420] = dst
    else:
        mostrar_eae = False

    cv2.imshow("Tradutor de Libras - Modo Analise", output)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

fila_fala.put(None)

cap.release()
cv2.destroyAllWindows()
