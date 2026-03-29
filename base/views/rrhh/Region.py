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

class RegionListCreateView(APIView):
    """
    Lista todas las regiones (con filtro por nombre) y permite crear nuevas.
    """
    permission_classes = [IsAuthenticated, IsRRHH]

    def get(self, request):
        # 1. Filtro por nombre (query params)
        busqueda = request.query_params.get('nombre')
        if busqueda:
            resultados = Region.objects.filter(description__icontains=busqueda)
        else:
            resultados = Region.objects.all()
        
        # 2. Serialización
        serializer = RegionSerializer(resultados, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 3. Creación con validación de Serializer
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegionDetailView(APIView):
    """
    Obtener, actualizar o eliminar una región específica.
    """
    permission_classes = [IsAuthenticated, IsRRHH]

    def get_object(self, id_region):
        try:
            return Region.objects.get(id=id_region)
        except Region.DoesNotExist:
            return None

    def get(self, request, id_region):
        region = self.get_object(id_region)
        if not region:
            return Response({"error": "La región no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RegionSerializer(region)
        return Response(serializer.data)

    def put(self, request, id_region):
        region = self.get_object(id_region)
        if not region:
            return Response({"error": "La región no existe"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RegionSerializer(region, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_region):
        region = self.get_object(id_region)
        if not region:
            return Response({"error": "La región no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            region.delete()
            return Response({"mensaje": f"Región {id_region} eliminada"}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                {"error": "No se puede eliminar: existen territorios vinculados"}, 
                status=status.HTTP_400_BAD_REQUEST
            )