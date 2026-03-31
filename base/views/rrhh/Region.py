import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import Region # Importamos desde el nuevo módulo de RRHH

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRRHH  # Asegúrate de que la ruta sea correcta
from ...models.rrhh import Region
from ...serializers import RegionSerializer

from ....configuracion.logger_config import setup_logging

class RegionListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def get(self, request):
        busqueda = request.query_params.get('nombre')
        resultados = Region.objects.filter(description__icontains=busqueda) if busqueda else Region.objects.all()
        serializer = RegionSerializer(resultados, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegionSerializer(data=request.data)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            region = serializer.save()
            audit_log.info(f"REGIÓN CREADA: {region.description} (ID: {region.id})")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def put(self, request, id_region):
        try:
            region = Region.objects.get(id=id_region)
            audit_log = logger.bind(audit=True, user=request.user.username)
            serializer = RegionSerializer(region, data=request.data)
            if serializer.is_valid():
                serializer.save()
                audit_log.info(f"REGIÓN ACTUALIZADA: ID {id_region}")
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Region.DoesNotExist:
            return Response({"error": "La región no existe"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id_region):
        try:
            region = Region.objects.get(id=id_region)
            audit_log = logger.bind(audit=True, user=request.user.username)
            region.delete()
            audit_log.info(f"REGIÓN ELIMINADA: ID {id_region}")
            return Response({"mensaje": f"Región {id_region} eliminada"}, status=status.HTTP_204_NO_CONTENT)
        except Region.DoesNotExist:
            return Response({"error": "No existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error al eliminar región {id_region}: {str(e)}")
            return Response({"error": "No se puede eliminar: existen territorios vinculados"}, status=status.HTTP_400_BAD_REQUEST)