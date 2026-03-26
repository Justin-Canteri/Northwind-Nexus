import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.inventory import Supplier  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt #para que postman entre sin seguridad

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import PremissionInventory  # Importamos tu clase nueva

from ...serializers import SupplierSerializer

class suppliersListCreateView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request):

        resultado = Supplier.objects.all()

        serializer = SupplierSerializer(resultado, many = True)

        return Response( serializer.data)

    def post(self, request):

        serializer = SupplierSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status= 201)
        return Response(serializer.errors, status=400)
    
class suppliersDetailView(APIView):
    permission_classes =[IsAuthenticated, PremissionInventory]

    def get(self, request, id_supplier):
        try:
            supplier_Obtenido = Supplier.objects.get(id = id_supplier)

            serializer = SupplierSerializer(supplier_Obtenido, many = True)

            return Response(serializer.data)
        
        except Supplier.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
        

    def put(self, request, id_supplier):

        try:
            supplier_Obtenido = Supplier.objects.get(id = id_supplier)

            serializer  = SupplierSerializer(supplier_Obtenido, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response (serializer.errors,status=400)
        except Supplier.DoesNotExist:
            return Response({"error": "Noxiste"}, status=404)
    
    def delete(self, request, id_supplier):
        try:
            e = Supplier.objects.get(id = id_supplier)
            e.delete()
            return Response({"mensaje": f"Empleado {id_supplier} eliminado"})
        except Exception:
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)