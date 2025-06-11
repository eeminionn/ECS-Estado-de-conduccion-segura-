# from django.shortcuts import render, redirect

# from .arduino_control import enviar_a_arduino

# PUERTO_ARDUINO = 'COM3'  # En Linux o Mac
# # PUERTO_ARDUINO = 'COM3'       # En Windows
# # Create your views here.

# def home(request):
#     return render(request, 'home.html')

# def contacto(request):
#     if request.method == 'POST':
#         boton = request.POST.get('boton')
#         if boton in ['1', '2', '3']:
#             enviar_a_arduino(PUERTO_ARDUINO, boton)
#         return redirect('contacto')  # Redirecciona para evitar reenvío del formulario
#     return render(request, 'contacto.html')

from django.shortcuts import render, redirect


from .arduino_control import enviar_a_arduino, leer_desde_arduino

from django.http import JsonResponse
from django.views.decorators.http import require_GET

PUERTO_ARDUINO = 'COM3'  # En Linux o Mac
# PUERTO_ARDUINO = 'COM3'       # En Windows

@require_GET
def obtener_lecturas(request):
    datos = arduino.obtener_lectura()
    return JsonResponse(datos)

def home(request):
    return render(request, 'home.html')


from .arduino_manager import ArduinoManager

arduino = ArduinoManager('COM3')

def interfaz(request):
    if request.method == 'POST':
        boton = request.POST.get('boton')
        if boton in ['1', '2', '3']:
            arduino.enviar_comando(boton)
        return redirect('contacto')

    lectura = arduino.obtener_lectura()
    return render(request, 'contacto.html', {'lectura': lectura})
