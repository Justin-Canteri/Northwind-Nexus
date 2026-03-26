import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.inventory import Producto  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt #para que postman entre sin seguridad

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import PremissionInventory  # Importamos tu clase nueva

from ...serializers import ProductoSerializer
# Create your views here.

class productsListCreateView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request):

        resultado = Producto.objects.select_related('categoria','proveedor').all()  # ← un solo query
        serializer = ProductoSerializer(resultado, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = ProductoSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status= 201)
        return Response(serializer.errors, status=400)
    

class productsDetailView(APIView):
    permission_classes =[IsAuthenticated, PremissionInventory]

    def get(self, request, id_producto):
        try:
            producto_Obtenido = Producto.objects.select_related('categoria', 'proveedor').get(id=id_producto)

            serializer = ProductoSerializer(producto_Obtenido)  # ← sin many=True

            return Response(serializer.data)
        
        except Producto.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
        

    def put(self, request, id_producto):

        try:
            Producto_Obtenido = Producto.objects.get(id = id_producto)

            serializer  = ProductoSerializer(Producto_Obtenido, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response (serializer.errors,status=400)
        except Producto.DoesNotExist:
            return Response({"error": "Noxiste"}, status=404)
    
    def delete(self, request, id_producto):
        try:
            productoAeliminar = Producto.objects.get(id = id_producto)
            productoAeliminar.delete()
            return Response({"mensaje": f"Empleado {id_producto} eliminado"}, status=204)
        except Exception:
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)