from django.db import models

class Alumno(models.Model):

    id_alumno = models.AutoField(primary_key=True)  # ID único de cada alumno, se genera automáticamente
    nombre_alumno = models.CharField(max_length=100)  # Nombre del alumno
    apellido_alumno = models.CharField(max_length=100)  # Apellido del alumno
    fecha_nacimiento_alumno = models.DateField()  # Fecha de nacimiento del alumno (Anio - Mes - Dia)
    anio_estudio_alumno = models.IntegerField()  # Año de estudio (1ro a 11vo)

    genero_alumno = models.CharField(
        max_length=10,
        choices=[('Masculino','Masculino'),('Femenino','Femenino'),('Otro','Otro')] # Primero valor guardado en BBDD, segundo mostrado en front
    )

    def __str__(self):
        return f"{self.nombre_alumno} {self.apellido_alumno}"  # Representación legible del alumno
    
# ------------------------------------------------------------------------------------------------------------------ #
    
class Maestro(models.Model):

    id_maestro = models.AutoField(primary_key=True)
    nombre_maestro = models.CharField(max_length=100)
    apellido_maestro = models.CharField(max_length=100)
    fecha_nacimiento_maestro = models.DateField(null=True, blank=True)

    genero_maestro = models.CharField(
        max_length=10,
        choices=[('Masculino','Masculino'),('Femenino','Femenino'),('Otro','Otro')],
        null=True,
        blank=True
    )

    especialidad_maestro = models.CharField(max_length=100)  # Especialidad del maestro (ej: Matemáticas, Literatura)

    def __str__(self):
        return f"{self.nombre_maestro} {self.apellido_maestro}"
    
# ------------------------------------------------------------------------------------------------------------------ #

class Clase(models.Model):
    id_clase = models.AutoField(primary_key=True)
    nombre_clase = models.CharField(max_length=100)  # Nombre de la clase
    anio_inicio_clase = models.IntegerField()  # Año desde el que se imparte la clase
    anio_fin_clase = models.IntegerField()     # Año hasta el que se imparte la clase

    maestro_clase = models.ForeignKey(
        Maestro,
        on_delete=models.SET_NULL,
        null=True,
        related_name='clases'
    )  # Cada clase tiene un maestro, un maestro puede tener varias clases

    def __str__(self):
        return self.nombre_clase

# ------------------------------------------------------------------------------------------------------------------ #

class Inscripcion(models.Model):

    id_inscripcion = models.AutoField(primary_key=True)
    alumno_inscripcion = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')  # Alumno inscrito en la clase
    clase_inscripcion = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='inscripciones')    # Clase en la que está inscrito el alumno
    fecha_inscripcion = models.DateField(auto_now_add=True)  # Fecha en que se registró la inscripción automáticamente

    def __str__(self):
        return f"{self.alumno_inscripcion} en {self.clase_inscripcion}"

# ------------------------------------------------------------------------------------------------------------------ #

class Nota(models.Model):

    id_nota = models.AutoField(primary_key=True)
    inscripcion_nota = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='notas')  # Nota asociada a una inscripción específica
    valor_nota = models.DecimalField(max_digits=5, decimal_places=2)  # Calificación numérica del alumno en esa clase

    def __str__(self):
        return f"{self.inscripcion_nota.alumno_inscripcion} - {self.inscripcion_nota.clase_inscripcion}: {self.valor_nota}"


