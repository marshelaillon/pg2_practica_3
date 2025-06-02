from rest_framework import serializers
from .models import ServiceResult

class ServiceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceResult
        fields = '__all__'
