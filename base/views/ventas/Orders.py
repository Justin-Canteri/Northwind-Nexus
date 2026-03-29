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

class OrderListCreateView(APIView):
    """
    Lista órdenes (con filtro por ID de orden o cliente) y crea nuevas.
    """
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, request):
        
        # Optimizamos la consulta para traer datos del cliente y el empleado de una vez
        queryset = Order.objects.select_related('customer', 'employee', 'ship_via').all()
        
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 2. Creación usando el Serializer
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    """
    Detalle, edición y borrado de una orden específica.
    """
    permission_classes = [IsAuthenticated, IsVentas]

    def get_object(self, id_order):
        try:
            orden_obtenida = Order.objects.select_related('customer', 'employee').get(id=id_order)
            serializer = OrderSerializer(orden_obtenida)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def put(self, request, id_order):

        try:
            orden_obtenida = Order.objects.get(id=id_order)

            serializer = OrderSerializer(orden_obtenida, data = request.data)

            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Order.DoesNotExist:
            return Response({"error": "Noxiste"}, status=404)
           
    def delete(self, request, id_order):
        try:
            productoAeliminar = Order.objects.get(id = id_order)
            productoAeliminar.delete()
            return Response({"mensaje": f"orden {id_order} eliminada"}, status=204)
        except Exception:
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)