import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.ventas import Shipper # Importación desde tu módulo de ventas

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsVentas
from ...models.ventas import Shipper
from ...serializers import ShipperSerializer

class ShipperListCreateView(APIView):
    """
    Lista transportistas y permite crear nuevos.
    """
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, request):

        resultado = Shipper.objects.all() 
        serializer = ShipperSerializer(resultado, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = ShipperSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status= 201)
        return Response(serializer.errors, status=400)


class ShipperDetailView(APIView):
    """
    Detalle, actualización y borrado de un transportista específico.
    """
    permission_classes = [IsAuthenticated, IsVentas]

    def get(self, request, id_shipper):
        try:
            shipper_Obtenido = Shipper.objects.get(id=id_shipper)

            serializer = ShipperSerializer(shipper_Obtenido)  # ← sin many=True

            return Response(serializer.data)
        
        except Shipper.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
        

    def put(self, request, id_shipper):

        try:
            shipper_Obtenido = Shipper.objects.get(id = id_shipper)

            serializer  = ShipperSerializer(shipper_Obtenido, data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response (serializer.errors,status=400)
        except Shipper.DoesNotExist:
            return Response({"error": "Noxiste"}, status=404)
    
    def delete(self, request, id_shipper):
        try:
            shipperAeliminar = Shipper.objects.get(id = id_shipper)
            shipperAeliminar.delete()
            return Response({"mensaje": f"shipper {id_shipper} eliminado"}, status=204)
        except Exception:
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)