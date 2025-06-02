import httpx
from asgiref.sync import async_to_sync

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from .models import EmailLookup, ServiceResult
from .serializers import ServiceResultSerializer

from holehe.modules.social_media.discord import discord
from holehe.modules.social_media.instagram import instagram
from holehe.modules.social_media.pinterest import pinterest
from holehe.modules.social_media.snapchat import snapchat
from holehe.modules.social_media.twitter import twitter
from holehe.modules.social_media.patreon import patreon
from holehe.modules.social_media.taringa import taringa
from holehe.modules.social_media.tumblr import tumblr

#* Algunos módulos comentados porque no son necesarios en este momento *#
# from holehe.modules.music.spotify import spotify
# from holehe.modules.music.lastfm import lastfm
# from holehe.modules.cms.wordpress import wordpress
# from holehe.modules.software.office365 import office365
# from holehe.modules.programing.github import github
# from holehe.modules.shopping.amazon import amazon
# from holehe.modules.learning.quora import quora
# from holehe.modules.mails.google import google
# from holehe.modules.mails.protonmail import protonmail

SERVICE_FUNCTIONS = {
  "instagram": instagram,
  "discord": discord,
  "pinterest": pinterest,
  "snapchat": snapchat,
  "twitter": twitter,
  "patreon": patreon,
  "taringa": taringa,
  "tumblr": tumblr,
}

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

async def run_holehe_module(email, service):
    out = []
    async with httpx.AsyncClient(headers=DEFAULT_HEADERS) as client:
        func = SERVICE_FUNCTIONS.get(service)
        if func:
            await func(email, client, out)
    return out

class HoleheSocialAllCheck(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        results = {}
        try:
            lookup = EmailLookup.objects.create(email=email)

            for social in SERVICE_FUNCTIONS.keys():
                try:
                    result = async_to_sync(run_holehe_module)(email, social)
                    results[social] = result

                    ServiceResult.objects.create(
                        lookup=lookup,
                        service=social,
                        result_data=result
                    )

                except Exception as e:
                    error_result = {"error": str(e)}
                    results[social] = error_result

                    ServiceResult.objects.create(
                        lookup=lookup,
                        service=social,
                        result_data=error_result
                    )

            return Response({"results": results}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class EmailLookupViewSet(viewsets.ViewSet):
    def list(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            return Response({"error": "Formato de correo electrónico inválido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Buscar en la base de datos
            lookup = EmailLookup.objects.get(email=email)
            results = ServiceResult.objects.filter(lookup=lookup)
            serializer = ServiceResultSerializer(results, many=True)
            return Response(serializer.data)

        except EmailLookup.DoesNotExist:
            # Si no existe, ejecutar Holehe
            lookup = EmailLookup.objects.create(email=email)
            all_results = []

            for social in SERVICE_FUNCTIONS.keys():
                try:
                    result = async_to_sync(run_holehe_module)(email, social)
                    sr = ServiceResult.objects.create(lookup=lookup, service=social, result_data=result)
                    all_results.append(sr)
                except Exception as e:
                    error_result = {"error": str(e)}
                    sr = ServiceResult.objects.create(lookup=lookup, service=social, result_data=error_result)
                    all_results.append(sr)

            serializer = ServiceResultSerializer(all_results, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
