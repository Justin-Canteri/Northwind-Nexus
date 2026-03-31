import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import Territory, Region # Importamos ambos para validar la región

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRRHH 
from ...models.rrhh import Territory
from ...serializers import TerritorySerializer

from ....configuracion.logger_config import setup_logging


class TerritoryListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def get(self, request):
        descripcion = request.query_params.get('nombre')
        region_id = request.query_params.get('region')
        queryset = Territory.objects.select_related('region').all()

        if descripcion:
            queryset = queryset.filter(description__icontains=descripcion)
        elif region_id:
            queryset = queryset.filter(region_id=region_id)
        else:
            queryset = queryset[:10]

        serializer = TerritorySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TerritorySerializer(data=request.data)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            territorio = serializer.save()
            audit_log.info(f"TERRITORIO CREADO: {territorio.description} (ID: {territorio.id})")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Error al crear territorio por {request.user.username}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TerritoryDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def get_object(self, id_territorio):
        try:
            return Territory.objects.select_related('region').get(id=id_territorio)
        except Territory.DoesNotExist:
            return None

    def get(self, request, id_territorio):
        territorio = self.get_object(id_territorio)
        if not territorio:
            return Response({"error": "El territorio no existe"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TerritorySerializer(territorio)
        return Response(serializer.data)

    def put(self, request, id_territorio):
        territorio = self.get_object(id_territorio)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if not territorio:
            return Response({"error": "El territorio no existe"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TerritorySerializer(territorio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            audit_log.info(f"TERRITORIO ACTUALIZADO: ID {id_territorio}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_territorio):
        territorio = self.get_object(id_territorio)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if not territorio:
            return Response({"error": "No existe"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            territorio.delete()
            audit_log.info(f"TERRITORIO ELIMINADO: ID {id_territorio}")
            return Response({"mensaje": f"Territorio {id_territorio} eliminado"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error al eliminar territorio {id_territorio}: {str(e)}")
            return Response({"error": "No se puede eliminar: tiene empleados asignados"}, status=status.HTTP_400_BAD_REQUEST)