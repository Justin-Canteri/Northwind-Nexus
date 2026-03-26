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
        
        territorios = EmployeeTerritory.objects.all()

        serializer = EmployeeTerritorySerializer(territorios, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeTerritorySerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, satatus = 201)
        
        return Response(serializer.errors, status=400)
'''
def buscar_asignaciones(request):
    # 1. Podemos filtrar por empleado o por territorio
    emp_id = request.GET.get('empleado')
    ter_id = request.GET.get('territorio')

    if emp_id:
        resultados = EmployeeTerritory.objects.filter(employee_id=emp_id)
    elif ter_id:
        resultados = EmployeeTerritory.objects.filter(territory_id=ter_id)
    else:
        resultados = EmployeeTerritory.objects.all()[:20]
        
    # 2. Respuesta en HTML
    respuesta_texto = "<h1>Asignaciones de Territorios:</h1><ul>"
    
    for et in resultados:
        # Accedemos a los nombres a través de las relaciones
        respuesta_texto += f"<li>Empleado: {et.employee.first_name} {et.employee.last_name} -> Zona: {et.territory.description.strip()}</li>"
    
    respuesta_texto += "</ul>"

    return HttpResponse(respuesta_texto)

@csrf_exempt
def asignar_territorio(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            # Creamos la relación entre empleado y territorio
            nueva_relacion = EmployeeTerritory.objects.create(
                employee_id=datos.get('employee_id'),
                territory_id=datos.get('territory_id')
            )

            return JsonResponse({
                "mensaje": "Territorio asignado correctamente",
                "empleado": nueva_relacion.employee_id,
                "territorio": nueva_relacion.territory_id
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)

@csrf_exempt
def eliminar_asignacion(request, id_empleado, id_territorio):
    if request.method == 'DELETE':
        try:
            # Buscamos la fila exacta que une a ese empleado con ese territorio
            asignacion = EmployeeTerritory.objects.get(
                employee_id=id_empleado, 
                territory_id=id_territorio
            )
            asignacion.delete()
            return JsonResponse({
                "mensaje": f"El empleado {id_empleado} ya no cubre el territorio {id_territorio}"
            })
        except EmployeeTerritory.DoesNotExist:
            return JsonResponse({"error": "No existe esa asignación"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite DELETE"}, status=405)
    '''