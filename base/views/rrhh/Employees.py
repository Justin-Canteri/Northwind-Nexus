import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import Employee

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRRHH  # Importamos tu clase nueva

from ...serializers import EmployeeSerializer

from ....configuracion.logger_config import setup_logging


class EmployeeListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            empleado = serializer.save()
            audit_log.info(f"EMPLEADO CONTRATADO: {empleado.first_name} {empleado.last_name} (ID: {empleado.id})")
            return Response(serializer.data, status=201)
        
        logger.warning(f"Error al contratar empleado por {request.user.username}: {serializer.errors}")
        return Response(serializer.errors, status=400)

class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def put(self, request, id_empleado):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            empleado = Employee.objects.get(id=id_empleado)
            serializer = EmployeeSerializer(empleado, data=request.data)
            if serializer.is_valid():
                serializer.save()
                audit_log.info(f"EMPLEADO ACTUALIZADO: ID {id_empleado}")
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Employee.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def delete(self, request, id_empleado):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            e = Employee.objects.get(id=id_empleado)
            nombre = f"{e.first_name} {e.last_name}"
            e.delete()
            audit_log.info(f"EMPLEADO ELIMINADO: {nombre} (ID: {id_empleado})")
            return Response({"mensaje": "Eliminado"}, status=204)
        except Exception as e:
            logger.error(f"Error al eliminar empleado {id_empleado}: {str(e)}")
            return Response({"error": "No se puede eliminar: tiene datos asociados"}, status=400)