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

from ....configuracion.logger_config import setup_logging

class suppliersListCreateView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request):
        resultado = Supplier.objects.all()
        serializer = SupplierSerializer(resultado, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        
        # Auditoría para creación
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            supplier = serializer.save()
            # Registramos el nombre de la empresa proveedora
            company = getattr(supplier, 'company_name', 'S/N')
            audit_log.info(f"PROVEEDOR CREADO: {company} (ID: {supplier.id})")
            return Response(serializer.data, status=201)
        
        logger.warning(f"Fallo al crear proveedor por {request.user.username}: {serializer.errors}")
        return Response(serializer.errors, status=400)

class suppliersDetailView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request, id_supplier):
        try:
            supplier_Obtenido = Supplier.objects.get(id=id_supplier)
            # Corregido: many=True eliminado para un solo objeto
            serializer = SupplierSerializer(supplier_Obtenido) 
            return Response(serializer.data)
        except Supplier.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def put(self, request, id_supplier):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            supplier_Obtenido = Supplier.objects.get(id=id_supplier)
            serializer = SupplierSerializer(supplier_Obtenido, data=request.data)

            if serializer.is_valid():
                serializer.save()
                audit_log.info(f"PROVEEDOR ACTUALIZADO: ID {id_supplier}")
                return Response(serializer.data)
            
            return Response(serializer.errors, status=400)
        except Supplier.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def delete(self, request, id_supplier):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            supplier_a_eliminar = Supplier.objects.get(id=id_supplier)
            company = getattr(supplier_a_eliminar, 'company_name', 'ID ' + str(id_supplier))
            supplier_a_eliminar.delete()
            
            audit_log.info(f"PROVEEDOR ELIMINADO: {company}")
            return Response({"mensaje": f"Proveedor {id_supplier} eliminado"}, status=204)
            
        except Supplier.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
        except Exception as e:
            # Captura errores de integridad (si tiene productos asociados)
            logger.error(f"Error al eliminar proveedor {id_supplier}: {str(e)}")
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)