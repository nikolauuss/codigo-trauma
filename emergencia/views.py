from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Emergencia
from .forms import ClienteSignUpForm
from django.conf import settings
from django.core.mail import send_mail



# Vista para la página principal
@login_required
def principal_view(request):
    user = request.user
    
    # Obtén todas las emergencias (o filtra según sea necesario)
    emergencias = Emergencia.objects.all()  # Puedes aplicar filtros según tus necesidades
    
    if user.groups.filter(name='Doctores').exists():
        # Renderiza la plantilla para doctores con el contexto necesario
        return render(request, 'principal_doctor.html', {'emergencias': emergencias})
    
    elif user.groups.filter(name='Clientes').exists():
        # Renderiza la plantilla para clientes con el contexto necesario
        return render(request, 'principal_cliente.html', {'emergencias': emergencias})

# Vista para iniciar una nueva emergencia
@login_required
def registrar_emergencia(request):
    if request.method == 'POST':
        # Capturamos todos los datos del formulario
        nombre_accidentado = request.POST.get('nombre_accidentado')
        num_victimas = request.POST.get('num_victimas')
        tipo = request.POST.get('tipo')
        ubicacion = request.POST.get('ubicacion')
        descripcion_incidente = request.POST.get('descripcion_incidente')
        gravedad = request.POST.get('gravedad')

        # Verificamos si todos los campos necesarios están completos
        if nombre_accidentado and num_victimas and tipo and ubicacion and descripcion_incidente and gravedad:
            # Creamos la emergencia en la base de datos
            emergencia = Emergencia.objects.create(
                nombre_accidentado=nombre_accidentado,
                num_victimas=num_victimas,
                tipo=tipo,
                ubicacion=ubicacion,
                descripcion_incidente=descripcion_incidente,
                
            )
            messages.success(request, 'Emergencia registrada exitosamente.')

            # Verificamos si la gravedad es grave y mostramos un mensaje adicional
            if gravedad == 'grave':
                messages.warning(request, '¡Atención! Se ha registrado una emergencia grave.')

            return redirect('principal')  # Redirigir a la página principal después del registro
        else:
            messages.error(request, 'Por favor, completa todos los campos.')

    return render(request, 'iniciar_emergencia.html')

# Vista para buscar información de emergencias
@login_required
def buscar_info_view(request):
    emergencias = Emergencia.objects.all()
    return render(request, 'buscar_info.html', {'emergencias': emergencias})

# Vista para evaluar una emergencia
import random


def evaluar_emergencia(request, emergencia_id):
    emergencia = get_object_or_404(Emergencia, id=emergencia_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm':
            # Mensaje de confirmación
            messages.success(request, f"Has evaluado la emergencia: {emergencia.tipo}. La emergencia se eliminará.")
            # Redirigir para confirmar eliminación
            return render(request, 'evaluar_emergencia.html', {
                'emergencia': emergencia,
                'confirmation_message': True,
                'sala_aleatoria': 'Sala 3',  # Aquí puedes usar la lógica para obtener la sala aleatoria
                'messages': messages.get_messages(request)  # Pasar los mensajes
            })
        elif action == 'final_confirm':
            # Eliminar la emergencia
            emergencia.delete()
            messages.success(request, "La emergencia ha sido eliminada exitosamente.")
            return redirect('principal')

    return render(request, 'evaluar_emergencia.html', {
        'emergencia': emergencia,
        'messages': messages.get_messages(request)  # Pasar los mensajes
    })
# Vista para eliminar una emergencia
@login_required
def eliminar_emergencia_view(request, id):
    emergencia = get_object_or_404(Emergencia, id=id)
    emergencia.delete()
    messages.success(request, 'Emergencia eliminada exitosamente.')
    return redirect('buscar_info')

# Vista para iniciar sesión

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión.')
    return redirect('login')

def informacion(request):
    # Obtén todas las emergencias relacionadas
    emergencias = Emergencia.objects.all()  # o usa select_related si necesitas cargar relaciones
    context = {
        'emergencias': emergencias
    }
    return render(request, 'informacion.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('principal')  # Cambia 'principal' por tu URL de la página principal
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'login.html')

def registro_view(request):
    if request.method == 'POST':
        form = ClienteSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario en la base de datos

            # Enviar correo de notificación
            send_mail(
                'Gracias por crear tu cuenta',
                '¡Gracias por registrarte! Tu cuenta ha sido creada exitosamente.',
                settings.EMAIL_HOST_USER,  # Tu correo configurado en settings.py
                [user.email],  # Correo del nuevo usuario
                fail_silently=False,
            )

            messages.success(request, '¡Cuenta creada con éxito! Se ha enviado un correo a tu dirección.')
            return redirect('login')  # Redirigir a la página de inicio de sesión después del registro
        else:
            # Si el formulario no es válido, mostrar mensajes de error específicos
            for field in form:
                for error in field.errors:
                    messages.error(request, f'Error en {field.label}: {error}')
            messages.error(request, 'Por favor, completa todos los campos obligatorios.')

    else:
        form = ClienteSignUpForm()

    return render(request, 'registro.html', {'form': form})
