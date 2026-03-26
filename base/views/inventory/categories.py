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

class CategoriesListCreateView(APIView):
    permission_classes = [IsAuthenticated, PremissionInventory]

    def get(self, request):
         resultado = categories.objects.all()

         serializer = categoriesSerializer(resultado, many=True)

         return (serializer.data)

    def post(self, request):
         
         serializer = categoriesSerializer(data = request.data)

         if serializer.is_valid():
              serializer.save()
              return Response(serializer.data, status=201)
         return Response(serializer.error, status=400)
    
class CategoriesDetailsView(APIView):
     permission_classes = [IsAuthenticated, PremissionInventory]

     def get(self, request, id_Categoria):
          try:
               categoria_Obtenido = categories.objects.get(id = id_Categoria)

               serializer = categoriesSerializer(categoria_Obtenido, many = True)

               return Response(serializer.data)
          except categories.DoesNotExist:
               return Response({"error": "No existe"}, status=404)
          
     def put(self, request, id_Categoria):
          
          try:
               categoria_Obtenido = categories.objects.get(id = id_Categoria)
               serializer = categoriesSerializer(categoria_Obtenido, data = request.data)

               if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
               return Response(serializer.errors, status=404)
          except categories.DoesNotExist:
               return Response({"error": "Noxiste"}, status=404)
          
     def delete(self, request, id_Categoria):
          try:
               delete_Cat = categories.objects.get(id = id_Categoria)
               delete_Cat.delete()
               return Response({"mensaje": f"Empleado {id_Categoria} eliminado"})
          except Exception:
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)