import cv2
import dlib
from scipy.spatial import distance
import pyttsx3
import speech_recognition as sr
import time

# --- Funciones del asistente virtual ---

def hablar(texto):
    print("Asistente:", texto)
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Escuchando...")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("Usuario:", texto)
        return texto.lower()
    except sr.UnknownValueError:
        hablar("No entendí lo que dijiste.")
        return ""
    except sr.RequestError:
        hablar("Hubo un problema con el reconocimiento de voz.")
        return ""

def preguntar_camino():
    hablar("¿Cómo sientes el camino hoy?")
    respuesta_camino = escuchar()

    if any(palabra in respuesta_camino for palabra in ["bien", "tranquilo", "suave", "normal"]):
        hablar("Perfecto, me alegra que todo esté tranquilo.")
    elif any(palabra in respuesta_camino for palabra in ["mal", "pesado", "difícil", "complicado"]):
        hablar("Lo siento, ten mucho cuidado y mantente alerta.")
    else:
        hablar("No entendí tu respuesta, pero sigue conduciendo con precaución.")

def asistente_virtual():
    hablar("Hola, noto que estás cansado. ¿Quieres que tome el control del vehículo?")
    respuesta = escuchar()

    if "sí" in respuesta or "si" in respuesta or "hazlo" in respuesta:
        hablar("De acuerdo. Activando el modo de conducción asistida.")
    elif "no" in respuesta or "yo puedo" in respuesta:
        hablar("Muy bien. Por favor, mantente alerta.")
    else:
        hablar("No entendí tu respuesta. Por favor, responde sí o no.")
    
    time.sleep(3)
    preguntar_camino()

# --- Función para calcular el aspecto del ojo (EAR) ---

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# --- Configuración de dlib y cámara ---

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/Users/palomagonzalez/Documents/paloma_2025/blink_detector/shape_predictor_68_face_landmarks.dat")


LEFT_EYE = list(range(42, 48))
RIGHT_EYE = list(range(36, 42))

EYE_AR_THRESH = 0.25
EYE_AR_CONSEC_FRAMES = 3

blink_counter = 0
frame_counter = 0
alert_triggered = False

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        landmarks = [(shape.part(i).x, shape.part(i).y) for i in range(68)]

        left_eye = [landmarks[i] for i in LEFT_EYE]
        right_eye = [landmarks[i] for i in RIGHT_EYE]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # Dibuja contornos ojos
        for point in left_eye:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)
        for point in right_eye:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)

        # Detectar parpadeo
        if ear < EYE_AR_THRESH:
            frame_counter += 1
        else:
            if frame_counter >= EYE_AR_CONSEC_FRAMES:
                blink_counter += 1
                print(f"Parpadeos: {blink_counter}")

                if blink_counter >= 5 and not alert_triggered:
                    asistente_virtual()
                    alert_triggered = True

            frame_counter = 0

    cv2.putText(frame, f"Parpadeos: {blink_counter}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

    cv2.imshow("Detector de parpadeo", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
