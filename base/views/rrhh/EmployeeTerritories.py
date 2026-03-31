import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import EmployeeTerritory

#Autenticacion y permisos
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRRHH  # Importamos tu clase nueva

#serializer
from ...serializers import EmployeeTerritorySerializer

from ....configuracion.logger_config import setup_logging



class EmployeeTerritoriesCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def post(self, request):
        serializer = EmployeeTerritorySerializer(data=request.data)
        audit_log = logger.bind(audit=True, user=request.user.username)

        if serializer.is_valid():
            et = serializer.save()
            audit_log.info(f"ASIGNACIÓN DE TERRITORIO: Empleado {et.employee_id} -> Territorio {et.territory_id}")
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class EmployeeTerritoriesDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def delete(self, request, id_EmployeeTerritory):
        audit_log = logger.bind(audit=True, user=request.user.username)
        try:
            et_obtenido = EmployeeTerritory.objects.get(employee_id=id_EmployeeTerritory)
            territorio_id = et_obtenido.territory_id
            et_obtenido.delete()
            audit_log.info(f"DESASIGNACIÓN DE TERRITORIO: Empleado {id_EmployeeTerritory} perdió territorio {territorio_id}")
            return Response(status=204)
        except EmployeeTerritory.DoesNotExist:
            return Response({"error": "No existe"}, status=404)