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

class OrderDetailListCreateView(APIView):
    """
    Lista detalles de órdenes (filtrado por orden) y permite agregar productos a órdenes.
    """
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, request):
        # 1. Filtro opcional por ID de orden
        id_orden = request.query_params.get('orden')
        
        # Optimizamos trayendo de una vez los datos del producto y la orden
        queryset = OrderDetail.objects.select_related('product', 'order').all()

        if id_orden:
            queryset = queryset.filter(order_id=id_orden)
        else:
            queryset = queryset[:20] # Límite por defecto
        
        serializer = OrderDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 2. Creación (Agregar producto a orden)
        serializer = OrderDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailDetailView(APIView):
    """
    Maneja un producto específico dentro de una orden específica.
    """
    permission_classes = [IsAuthenticated, IsVentas]

    def get_object(self, id_orden, id_producto):
        try:
            # Buscamos por la combinación única de la tabla intermedia
            return OrderDetail.objects.get(order_id=id_orden, product_id=id_producto)
        except OrderDetail.DoesNotExist:
            return None

    def get(self, request, id_orden, id_producto):
        detalle = self.get_object(id_orden, id_producto)
        if not detalle:
            return Response({"error": "No se encontró el producto en esa orden"}, status=404)
        
        serializer = OrderDetailSerializer(detalle)
        return Response(serializer.data)

    def put(self, request, id_orden, id_producto):
        detalle = self.get_object(id_orden, id_producto)
        if not detalle:
            return Response({"error": "No existe el detalle"}, status=404)

        serializer = OrderDetailSerializer(detalle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id_orden, id_producto):
        detalle = self.get_object(id_orden, id_producto)
        if not detalle:
            return Response({"error": "No existe el detalle"}, status=404)
        
        detalle.delete()
        return Response(
            {"mensaje": f"Producto {id_producto} eliminado de la orden {id_orden}"}, 
            status=status.HTTP_204_NO_CONTENT
        )