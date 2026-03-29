import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.ventas import Customer  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsVentas  # Importamos tu clase de permiso
from ...models.ventas import Customer
from ...serializers import CustomerSerializer

class CustomerListCreateView(APIView):
    """
    Lista clientes (con filtro por nombre de empresa) y permite crear nuevos.
    """
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, request):        
        resultados = Customer.objects.all()
        
        # 2. Serialización
        serializer = CustomerSerializer(resultados, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 3. Creación: El ID debe ser enviado (5 caracteres)
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    """
    Obtener, actualizar o eliminar un cliente específico por su ID de 5 letras.
    """
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, id_cliente):
        try:
            customer_Obtenido = Customer.objects.get(id=id_cliente)
            serializer = CustomerSerializer(customer_Obtenido)

            return Response(serializer.data)
        
        except Customer.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def put(self, request, id_cliente):

        try:
            Producto_Obtenido = Customer.objects.get(id = id_cliente)

            serializer  = CustomerSerializer(Producto_Obtenido, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response (serializer.errors,status=400)
        except Customer.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

        

    def delete(self, request, id_cliente):
        try:
            ClienteAeliminar = Customer.objects.get(id = id_cliente)
            ClienteAeliminar.delete()
            return Response({"mensaje": f"cliente {id_cliente} eliminado"}, status=204)
        except Exception:
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)