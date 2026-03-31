import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.inventory import categories  # Tu "mapa"

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import PremissionInventory  # Importamos tu clase nueva

from ...serializers import categoriesSerializer

from ....configuracion.logger_config import setup_logging

class CategoriesListCreateView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request):
        resultado = categories.objects.all()
        serializer = categoriesSerializer(resultado, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = categoriesSerializer(data=request.data)
        
        # Preparamos el logger con los campos que pide tu filtro: "audit" y "user"
        audit_logger = logger.bind(audit=True, user=request.user.username)
        
        if serializer.is_valid():
            category = serializer.save()
            # Esto irá a audit.log y a la consola
            audit_logger.info(f"CREAR: Categoría '{category.category_name}' (ID: {category.id})")
            return Response(serializer.data, status=201)
        
        # Esto irá a la consola (pero no a audit.log ni errors.log porque es nivel WARNING)
        logger.warning(f"Intento de creación fallido por el usuario {request.user.username}")
        return Response(serializer.errors, status=400)

class CategoriesDetailsView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request, id_Categoria):
        try:
            categoria_Obtenido = categories.objects.get(id=id_Categoria)
            serializer = categoriesSerializer(categoria_Obtenido)
            return Response(serializer.data)
        except categories.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
          
    def put(self, request, id_Categoria):
        audit_logger = logger.bind(audit=True, user=request.user.username)
        try:
            categoria_Obtenido = categories.objects.get(id=id_Categoria)
            serializer = categoriesSerializer(categoria_Obtenido, data=request.data)

            if serializer.is_valid():
                serializer.save()
                audit_logger.info(f"ACTUALIZAR: Categoría ID {id_Categoria}")
                return Response(serializer.data)
            
            return Response(serializer.errors, status=400)
        except categories.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
          
    def delete(self, request, id_Categoria):
        audit_logger = logger.bind(audit=True, user=request.user.username)
        try:
            delete_Cat = categories.objects.get(id=id_Categoria)
            nombre_cat = delete_Cat.category_name
            delete_Cat.delete()
            
            audit_logger.info(f"ELIMINAR: Categoría {nombre_cat} (ID: {id_Categoria})")
            return Response({"mensaje": f"Categoría {id_Categoria} eliminada"})
        except Exception as e:
            # Esto se enviará automáticamente a errors.log gracias a tu nivel="ERROR"
            logger.error(f"Error crítico al eliminar categoría {id_Categoria}: {str(e)}")
            return Response({"error": "Error interno al eliminar"}, status=400)