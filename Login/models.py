from django.db import models

class Usuario(models.Model):

    # Campos comunes
    id_usuario = models.AutoField(primary_key=True)
    carnet = models.CharField(max_length=20, unique=True, blank=True)
    contrasena = models.CharField(max_length=128, null=True)  # Contraseña encriptada
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(
        max_length=10,
        choices=[('Masculino','Masculino'),('Femenino','Femenino'),('Otro','Otro')],
        null=True,
        blank=True
    )

    # Rol: estudiante, maestro o administrador
    rol = models.CharField(
        max_length=10,
        choices=[('alumno','Alumno'), ('maestro','Maestro'), ('admin','Administrador')]
    )

    # Campos específicos
    # Solo para estudiantes
    anio_estudio = models.IntegerField(null=True, blank=True)
    estado = models.CharField(
        max_length=10,
        choices=[('Activo','Activo'),('Egresado','Egresado'),('Expulsado','Expulsado')],
        default='Activo',
        blank=True
    )

    # Solo para maestros
    especialidad = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"