# ------------------------------------------------------------------------------------------------------------------ #

from django.db import models
from Login.models import Usuario  # tu nuevo modelo unificado

# ------------------------------------------------------------------------------------------------------------------ #

class Clase(models.Model):
    id_clase = models.AutoField(primary_key=True)
    nombre_clase = models.CharField(max_length=100)
    anio_inicio_clase = models.IntegerField()  # Año desde el que se imparte la clase
    anio_fin_clase = models.IntegerField()     # Año hasta el que se imparte la clase

    maestro_clase = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'rol': 'maestro'},  # Solo usuarios con rol maestro
        related_name='clases'
    )

    def __str__(self):
        return self.nombre_clase

# ------------------------------------------------------------------------------------------------------------------ #

class Inscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    alumno_inscripcion = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'alumno'},  # Solo usuarios con rol alumno
        related_name='inscripciones'
    )
    clase_inscripcion = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )
    fecha_inscripcion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno_inscripcion} en {self.clase_inscripcion}"

# ------------------------------------------------------------------------------------------------------------------ #

class Nota(models.Model):
    id_nota = models.AutoField(primary_key=True)
    inscripcion_nota = models.ForeignKey(
        Inscripcion,
        on_delete=models.CASCADE,
        related_name='notas'
    )
    valor_nota = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.inscripcion_nota.alumno_inscripcion} - {self.inscripcion_nota.clase_inscripcion}: {self.valor_nota}"


# Crear archivo de migraciones: python manage.py makemigrations

# Migrar: python manage.py migrate

# Ver Migraciones aplicadas o pendientes: python manage.py showmigrations