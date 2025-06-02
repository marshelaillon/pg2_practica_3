from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailLookupViewSet

router = DefaultRouter()
router.register(r'', EmailLookupViewSet, basename='emails')

urlpatterns = [
    path('', include(router.urls), name="email-lookup"),
]
