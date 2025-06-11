from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.home, name='home'),  # Ruta vacía para la página principal
    path('contacto/', views.interfaz, name='contacto'),
    path('lecturas/', views.obtener_lecturas, name='lecturas'),  # Nueva ruta para AJAX

  



]