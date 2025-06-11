import speech_recognition as sr
import pyttsx3

# Inicializar el motor de voz
engine = pyttsx3.init()

def hablar(texto):
    print("Asistente:", texto)
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language="es-ES")
        print("Usuario:", texto)
        return texto.lower()
    except sr.UnknownValueError:
        hablar("Lo siento, no te entendí.")
        return ""
    except sr.RequestError:
        hablar("Error al conectar con el servicio de voz.")
        return ""

def asistente_virtual():
    hablar("Hola, noto que estás cansado. ¿Quieres que tome el control del vehículo?")
    respuesta = escuchar()

    if "sí" in respuesta or "hazlo" in respuesta:
        hablar("Activando el modo asistido.")
    elif "no" in respuesta or "yo puedo" in respuesta:
        hablar("De acuerdo, conduce con cuidado.")
    else:
        hablar("No entendí tu respuesta. ¿Puedes repetirlo?")

asistente_virtual()
