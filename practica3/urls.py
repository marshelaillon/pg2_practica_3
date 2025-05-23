from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from gym.views import UsuarioViewSet, EjercicioViewSet

router = routers.DefaultRouter()

router.register(r"usuarios", UsuarioViewSet)
router.register(r"ejercicios", EjercicioViewSet)

urlpatterns = [
  path("admin/", admin.site.urls),
  path("api/", include(router.urls)),
]