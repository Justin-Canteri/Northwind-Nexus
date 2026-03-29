import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import Employee

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRRHH  # Importamos tu clase nueva

from ...serializers import EmployeeSerializer

class EmployeeListCreateView(APIView):
    # EL ESCUDO: Aplica para TODO lo que esté aquí adentro
    permission_classes = [IsAuthenticated, IsRRHH]

    def get(self, request):
        # 1. Traemos los datos de la DB
        empleados = Employee.objects.all()
        
        seriealizer = EmployeeSerializer(empleados, many=True)

        return Response(seriealizer.data)
    

    def post(self, request):
        # Pasamos el JSON directo de Postman al traductor (Serializer)
        serializer = EmployeeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Si los datos son correctos, guarda en la DB
            serializer.save() 
            # Devolvemos el objeto creado (con su nuevo ID) como respuesta
            return Response(serializer.data, status=201)
        
        # Si el JSON estaba mal (ej: faltó un campo), enviamos el error
        return Response(serializer.errors, status=400)
    

class EmployeeDetailView(APIView):
    # El mismo escudo de seguridad
    permission_classes = [IsAuthenticated, IsRRHH]

    def get(self, request, id_empleado):
        try:
            empleado = Employee.objects.get(id = id_empleado)

            serializer = EmployeeSerializer(empleado)
            return Response (serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
        

    def put(self, request, id_empleado):
        try:
            empleado = Employee.objects.get(id=id_empleado)
            # Pasamos el objeto existente Y los nuevos datos
            serializer = EmployeeSerializer(empleado, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Employee.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def delete(self, request, id_empleado):
        try:
            e = Employee.objects.get(id=id_empleado)
            e.delete()
            return Response({"mensaje": f"Empleado {id_empleado} eliminado"})
        except Exception:
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)