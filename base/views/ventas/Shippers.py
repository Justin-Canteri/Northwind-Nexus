import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.ventas import Shipper # Importación desde tu módulo de ventas

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsVentas
from ...models.ventas import Shipper
from ...serializers import ShipperSerializer

from ....configuracion.logger_config import setup_logging

class ShipperListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsVentas]

    def post(self, request):
        serializer = ShipperSerializer(data=request.data)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            shipper = serializer.save()
            audit_log.info(f"TRANSPORTISTA CREADO: {shipper.company_name} (ID: {shipper.id})")
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ShipperDetailView(APIView):
    permission_classes = [IsAuthenticated, IsVentas]

    def delete(self, request, id_shipper):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            shipper = Shipper.objects.get(id=id_shipper)
            nombre = shipper.company_name
            shipper.delete()
            audit_log.info(f"TRANSPORTISTA ELIMINADO: {nombre} (ID: {id_shipper})")
            return Response(status=204)
        except Exception as e:
            logger.error(f"Error al eliminar shipper {id_shipper}: {str(e)}")
            return Response({"error": "No se puede eliminar: está vinculado a órdenes"}, status=400)