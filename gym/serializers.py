from gym.models import *
from rest_framework import serializers

class UsuarioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Usuario
    fields = [
      "id",
      "altura",
      "contrasenia_hash",
      "correo",
      "creadoEn",
      "edad",
      "genero",
      "nombre_usuario",
      "peso",
    ]


class EjercicioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ejercicio
    fields = "__all__"