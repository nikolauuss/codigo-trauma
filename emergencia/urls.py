from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # Página de login
    path('principal/', views.principal_view, name='principal'),  # Página principal
    path('iniciar-emergencia/', views.registrar_emergencia, name='iniciar_emergencia'),  # Iniciar emergencia
    path('buscar-info/', views.buscar_info_view, name='buscar_info'),  # Buscar emergencias
    path('evaluar-emergencia/<int:emergencia_id>/', views.evaluar_emergencia, name='evaluar_emergencia'),
    path('eliminar-emergencia/<int:id>/', views.eliminar_emergencia_view, name='eliminar_emergencia'),  # Eliminar emergencia
    path('logout/', views.logout_view, name='logout'),  # Cerrar sesión
    path('registro/', views.registro_view, name='registro'),
    path('informacion/', views.informacion, name='informacion'),

]
