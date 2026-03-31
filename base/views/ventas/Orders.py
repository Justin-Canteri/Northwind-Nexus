import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.ventas import Order  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsVentas
from ...models.ventas import Order
from ...serializers import OrderSerializer

from ....configuracion.logger_config import setup_logging

class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, request):
        queryset = Order.objects.select_related('customer', 'employee', 'ship_via').all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            order = serializer.save()
            audit_log.info(f"ORDEN CREADA: ID {order.id} para Cliente {order.customer_id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated, IsVentas]

    def put(self, request, id_order):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            orden = Order.objects.get(id=id_order)
            serializer = OrderSerializer(orden, data=request.data)
            if serializer.is_valid():
                serializer.save() # Faltaba el .save() en tu código original
                audit_log.info(f"ORDEN MODIFICADA: ID {id_order}")
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Order.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def delete(self, request, id_order):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            orden = Order.objects.get(id=id_order)
            orden.delete()
            audit_log.info(f"ORDEN ELIMINADA: ID {id_order}")
            return Response({"mensaje": f"orden {id_order} eliminada"}, status=204)
        except Exception as e:
            logger.error(f"Fallo crítico al eliminar orden {id_order}: {str(e)}")
            return Response({"error": "No se puede eliminar: tiene detalles asociados"}, status=400)