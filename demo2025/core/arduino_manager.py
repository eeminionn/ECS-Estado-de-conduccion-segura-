import serial
import threading
import time

class ArduinoManager:
    def __init__(self, puerto):
        self.puerto = puerto
        self.lectura_actual = {"A0": None, "A1": None}
        self.lock = threading.Lock()
        self.serial = serial.Serial(puerto, 9600, timeout=1)
        time.sleep(2)
        self.escuchando = True
        threading.Thread(target=self._leer_loop, daemon=True).start()

    def _leer_loop(self):
        while self.escuchando:
            try:
                if self.serial.in_waiting:
                    linea = self.serial.readline().decode(errors='ignore').strip()
                    if "A0" in linea and "A1" in linea:
                        partes = linea.split(" ")
                        with self.lock:
                            for p in partes:
                                if ":" in p:
                                    k, v = p.split(":")
                                    self.lectura_actual[k] = int(v)
            except Exception as e:
                print("Error leyendo de Arduino:", e)

    def enviar_comando(self, comando):
        try:
            with self.lock:
                self.serial.write(comando.encode())
        except Exception as e:
            print("Error enviando a Arduino:", e)

    def obtener_lectura(self):
        with self.lock:
            return self.lectura_actual.copy()
