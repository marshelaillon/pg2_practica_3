from datetime import timedelta
from rest_framework import viewsets
from django.utils import timezone as tz
from gym.serializers import *
from gym.models import *

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer