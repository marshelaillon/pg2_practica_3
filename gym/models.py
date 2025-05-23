from django.db import models

class Usuario(models.Model):
  id = models.BigAutoField(primary_key=True)
  altura = models.FloatField()
  contrasenia_hash = models.CharField(max_length=128)
  correo = models.EmailField(max_length=254, unique=True)
  creadoEn = models.DateTimeField(auto_now_add=True)
  edad = models.IntegerField()
  genero = models.CharField(max_length=1)
  nombre_usuario = models.CharField(max_length=50)
  peso = models.FloatField()

  def __str__(self):
    return self.nombre

class Ejercicio(models.Model):
  id = models.BigAutoField(primary_key=True)
  descripcion = models.TextField()
  dificultad = models.CharField(max_length=20)
  equipo_necesario = models.CharField(max_length=50)
  nombre = models.CharField(max_length=50)

  def __str__(self):
    return self.nombre

class ProgresionEjercicio(models.Model):
  id = models.BigAutoField(primary_key=True)
  ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
  nivel_dificultad = models.IntegerField()
  nombre = models.CharField(max_length=50)

class RutinaEntrenamiento(models.Model):
  id = models.BigAutoField(primary_key=True)
  duracion_minutos = models.IntegerField()
  enfoque = models.CharField(max_length=50)
  nombre = models.CharField(max_length=50)

  def __str__(self):
    return self.nombre
  
class EjercicioRutina(models.Model):
  id = models.BigAutoField(primary_key=True)
  ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
  rutina = models.ForeignKey(RutinaEntrenamiento, on_delete=models.CASCADE)
  orden = models.IntegerField()
  repeticiones = models.IntegerField()
  series = models.IntegerField()