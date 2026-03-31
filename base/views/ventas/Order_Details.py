import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.ventas import OrderDetail # Importamos el modelo

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsVentas
from ...models.ventas import OrderDetail
from ...serializers import OrderDetailSerializer

from ....configuracion.logger_config import setup_logging

class OrderDetailListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsVentas]

    def post(self, request):
        serializer = OrderDetailSerializer(data=request.data)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            det = serializer.save()
            audit_log.info(f"ITEM AGREGADO: Producto {det.product_id} a Orden {det.order_id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailDetailView(APIView):
    permission_classes = [IsAuthenticated, IsVentas]

    def put(self, request, id_orden, id_producto):
        detalle = self.get_object(id_orden, id_producto)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if not detalle:
            return Response({"error": "No existe"}, status=404)

        serializer = OrderDetailSerializer(detalle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            audit_log.info(f"ITEM ACTUALIZADO: Orden {id_orden}, Producto {id_producto}")
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id_orden, id_producto):
        detalle = self.get_object(id_orden, id_producto)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if not detalle:
            return Response({"error": "No existe"}, status=404)
        
        detalle.delete()
        audit_log.info(f"ITEM ELIMINADO: Producto {id_producto} de Orden {id_orden}")
        return Response(status=status.HTTP_204_NO_CONTENT)