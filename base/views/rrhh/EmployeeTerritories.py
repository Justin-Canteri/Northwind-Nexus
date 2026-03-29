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


class EmployeeTerritoriesCreateView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def get(self, request):
        territorios = EmployeeTerritory.objects.select_related(
            'employee', 
            'territory', 
            'territory__region'  # dentro de territory está region 
        ).all()
        serializer = EmployeeTerritorySerializer(territorios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeTerritorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


class EmployeeTerritoriesDetailView(APIView):
    permission_classes = [IsAuthenticated, IsRRHH]

    def get(self, request, id_EmployeeTerritory):
        try:
            et_obtenido = EmployeeTerritory.objects.select_related(
                'employee',
                'territory',
                'territory__region'
            ).get(employee_id=id_EmployeeTerritory)

            serializer = EmployeeTerritorySerializer(et_obtenido)
            return Response(serializer.data)
        except EmployeeTerritory.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def put(self, request, id_EmployeeTerritory):
        try:
            et_obtenido = EmployeeTerritory.objects.get(employee_id=id_EmployeeTerritory)

            serializer = EmployeeTerritorySerializer(et_obtenido, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except EmployeeTerritory.DoesNotExist:
            return Response({"error": "No existe"}, status=404)

    def delete(self, request, id_EmployeeTerritory):
        try:
            et_obtenido = EmployeeTerritory.objects.get(employee_id=id_EmployeeTerritory)
            et_obtenido.delete()
            return Response({"mensaje": f"EmployeeTerritory {id_EmployeeTerritory} eliminado"}, status=204)
        except EmployeeTerritory.DoesNotExist:
            return Response({"error": "No existe"}, status=404)