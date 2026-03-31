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

from ....configuracion.logger_config import setup_logging


class productsListCreateView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request):
        # Log de consulta (Solo consola/archivo general si lo tienes)
        resultado = Producto.objects.select_related('categoria','proveedor').all()
        serializer = ProductoSerializer(resultado, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        
        # Preparamos el log de auditoría
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            producto = serializer.save()
            audit_log.info(f"PRODUCTO CREADO: {producto.nombre} (ID: {producto.id}) - Stock: {producto.units_in_stock}")
            return Response(serializer.data, status=201)
        
        # Si falla, registramos la advertencia en consola
        logger.warning(f"Fallo al crear producto por usuario {request.user.username}: {serializer.errors}")
        return Response(serializer.errors, status=400)

class productsDetailView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request, id_producto):
        try:
            producto_Obtenido = Producto.objects.select_related('categoria', 'proveedor').get(id=id_producto)
            serializer = ProductoSerializer(producto_Obtenido)
            return Response(serializer.data)
        except Producto.DoesNotExist:
            logger.warning(f"Producto no encontrado: ID {id_producto}")
            return Response({"error": "No existe"}, status=404)

    def put(self, request, id_producto):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            producto_Obtenido = Producto.objects.get(id=id_producto)
            serializer = ProductoSerializer(producto_Obtenido, data=request.data)

            if serializer.is_valid():
                serializer.save()
                audit_log.info(f"PRODUCTO ACTUALIZADO: ID {id_producto} - Datos: {request.data.keys()}")
                return Response(serializer.data)
            
            return Response(serializer.errors, status=400)
        except Producto.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def delete(self, request, id_producto):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            productoAeliminar = Producto.objects.get(id=id_producto)
            nombre_prod = getattr(productoAeliminar, 'nombre', 'Desconocido') # Evita errores si el campo varía
            productoAeliminar.delete()
            
            audit_log.info(f"PRODUCTO ELIMINADO: {nombre_prod} (ID: {id_producto})")
            return Response({"mensaje": f"Producto {id_producto} eliminado"}, status=204)
        except Producto.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
        except Exception as e:
            # Esto irá a tu errors.log configurado con backtrace=True
            logger.error(f"Error crítico eliminando producto {id_producto}: {str(e)}")
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)