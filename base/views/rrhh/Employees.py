import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import Employee

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRRHH  # Importamos tu clase nueva

class EmployeeListCreateView(APIView):
    # EL ESCUDO: Aplica para TODO lo que esté aquí adentro
    permission_classes = [IsAuthenticated, IsRRHH]

    def get(self, request):
        # 1. Traemos los datos de la DB
        empleados = Employee.objects.all()
        
        # 2. Creamos una lista para responder (puedes usar un Serializer luego)
        data = []
        for e in empleados:
            data.append({
                "id": e.id,
                "nombre": f"{e.first_name} {e.last_name}",
                "cargo": e.title
            })
        
        # 3. Solo si eres RRHH llegarás a ver este Response
        return Response(data)

    def post(self, request):
        # Aquí pegamos tu lógica de "crear_empleado"
        try:
            datos = request.data # DRF ya te da el JSON listo en 'request.data'
            nuevo_empleado = Employee.objects.create(
                first_name=datos.get('first_name'),
                last_name=datos.get('last_name'),
                title=datos.get('title'),
                city=datos.get('city'),
                country=datos.get('country'),
                reports_to_id=datos.get('reports_to_id')
            )
            return Response({
                "mensaje": "Empleado registrado con éxito",
                "id_asignado": nuevo_empleado.id
            }, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class EmployeeDetailView(APIView):
    # El mismo escudo de seguridad
    permission_classes = [IsAuthenticated, IsRRHH]

    def put(self, request, id_empleado):
        try:
            e = Employee.objects.get(id=id_empleado)
            datos = request.data  # Usamos request.data de DRF
            
            e.first_name = datos.get('first_name', e.first_name)
            e.last_name = datos.get('last_name', e.last_name)
            e.title = datos.get('title', e.title)
            e.save()
            
            return Response({"mensaje": f"Empleado {id_empleado} actualizado"})
        except Employee.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def delete(self, request, id_empleado):
        try:
            e = Employee.objects.get(id=id_empleado)
            e.delete()
            return Response({"mensaje": f"Empleado {id_empleado} eliminado"})
        except Exception:
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)