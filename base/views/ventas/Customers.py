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

from ....configuracion.logger_config import setup_logging

class CustomerListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, request):        
        resultados = Customer.objects.all()
        serializer = CustomerSerializer(resultados, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            customer = serializer.save()
            audit_log.info(f"CLIENTE REGISTRADO: {customer.company_name} (ID: {customer.id})")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, request, id_cliente): # Añadido 'request' que faltaba
        try:
            customer_Obtenido = Customer.objects.get(id=id_cliente)
            serializer = CustomerSerializer(customer_Obtenido)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def put(self, request, id_cliente):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            cliente = Customer.objects.get(id=id_cliente)
            serializer = CustomerSerializer(cliente, data=request.data)
            if serializer.is_valid():
                serializer.save()
                audit_log.info(f"CLIENTE ACTUALIZADO: ID {id_cliente} - {cliente.company_name}")
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Customer.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def delete(self, request, id_cliente):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            cliente = Customer.objects.get(id=id_cliente)
            nombre = cliente.company_name
            cliente.delete()
            audit_log.info(f"CLIENTE ELIMINADO: {nombre} (ID: {id_cliente})")
            return Response({"mensaje": f"cliente {id_cliente} eliminado"}, status=204)
        except Exception as e:
            logger.error(f"Error al eliminar cliente {id_cliente}: {str(e)}")
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)