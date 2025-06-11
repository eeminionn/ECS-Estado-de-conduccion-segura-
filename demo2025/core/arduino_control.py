import serial
import time

def enviar_a_arduino(puerto: str, comando: str):
    try:
        arduino = serial.Serial(puerto, 9600, timeout=1)
        time.sleep(2)  # Esperar a que Arduino inicie
        arduino.write(comando.encode())
        arduino.close()
    except Exception as e:
        print("Error al comunicar con Arduino:", e)


def leer_desde_arduino(puerto: str):
    try:
        arduino = serial.Serial(puerto, 9600, timeout=2)
        time.sleep(2)
        arduino.flushInput()
        
        linea = arduino.readline().decode().strip()
        arduino.close()

        # Se espera algo como: "A0:123 A1:456"
        datos = {"A0": None, "A1": None}
        partes = linea.split(" ")
        for p in partes:
            if ":" in p:
                k, v = p.split(":")
                datos[k] = int(v)

        return datos
    except Exception as e:
        print("Error al leer de Arduino:", e)
        return {"A0": "Error", "A1": "Error"}