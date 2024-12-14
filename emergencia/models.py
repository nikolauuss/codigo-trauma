from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo de Emergencia
class Emergencia(models.Model):
    num_victimas = models.PositiveIntegerField()  # Cambiado a PositiveIntegerField para evitar números negativos
    tipo = models.CharField(max_length=100)  # Tipo de emergencia
    ubicacion = models.CharField(max_length=200)  # Ubicación de la emergencia
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    descripcion_incidente = models.TextField()  # Descripción del incidente
    nombre_accidentado = models.CharField(max_length=100)  # Nombre del accidentado
    

    class Meta:
        verbose_name = 'Emergencia'
        verbose_name_plural = 'Emergencias'
        ordering = ['-fecha']  # Ordenar las emergencias por fecha, las más recientes primero

    def __str__(self):
        return f'Emergencia: {self.tipo} con {self.num_victimas} víctimas en {self.ubicacion} el {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}'

# Modelo para los clientes
class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.usuario.username

# Modelo para la respuesta de los miembros clínicos ante una emergencia
class RespuestaEmergencia(models.Model):
    emergencia = models.ForeignKey(Emergencia, on_delete=models.CASCADE, related_name='respuestas')
    miembro = models.ForeignKey(User, on_delete=models.CASCADE)  # Miembro que responde a la emergencia
    descripcion = models.TextField()
    ha_respondido = models.BooleanField(default=False)
    tiempo_respuesta = models.DateTimeField(null=True, blank=True)

    def registrar_respuesta(self):
        self.ha_respondido = True
        self.tiempo_respuesta = timezone.now()
        self.save()

    def __str__(self):
        return f'Respuesta a {self.emergencia.tipo} por {self.miembro.username}'
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Agrega otros campos que necesites, por ejemplo:
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username
class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    sala = models.CharField(max_length=100)
    hora_visitas = models.TimeField()
    emergencia = models.ForeignKey(Emergencia, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario.username} en sala {self.sala}'
    
    