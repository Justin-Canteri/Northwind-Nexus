import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import Employee

def buscar_empleados(request):
    # 1. Filtramos por apellido o ciudad
    apellido = request.GET.get('apellido')
    ciudad = request.GET.get('ciudad')

    if apellido:
        resultados = Employee.objects.filter(last_name__icontains=apellido)
    elif ciudad:
        resultados = Employee.objects.filter(city__icontains=ciudad)
    else:
        # Traemos todos los empleados
        resultados = Employee.objects.all()
        
    # 3. Respuesta en HTML
    respuesta_texto = "<h1>Nómina de Empleados Northwind:</h1><ul>"
    
    for e in resultados:
        # Manejo de la relación recursiva para mostrar quién es el jefe
        jefe = f" (Reporta a: {e.reports_to.first_name})" if e.reports_to else " (Es Gerente)"
        respuesta_texto += f"<li>ID: {e.id} - {e.first_name} {e.last_name} - Cargo: {e.title}{jefe}</li>"
    
    respuesta_texto += "</ul>"

    return HttpResponse(respuesta_texto)

@csrf_exempt
def crear_empleado(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            # Creamos el empleado (el ID es AutoField, no se envía)
            nuevo_empleado = Employee.objects.create(
                first_name=datos.get('first_name'),
                last_name=datos.get('last_name'),
                title=datos.get('title'),
                birth_date=datos.get('birth_date'),
                hire_date=datos.get('hire_date'),
                city=datos.get('city'),
                country=datos.get('country'),
                reports_to_id=datos.get('reports_to_id') # Pasamos el ID del jefe
            )

            return JsonResponse({
                "mensaje": "Empleado registrado con éxito",
                "id_asignado": nuevo_empleado.id,
                "nombre_completo": f"{nuevo_empleado.first_name} {nuevo_empleado.last_name}"
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)

@csrf_exempt
def editar_empleado(request, id_empleado):
    if request.method == 'PUT':
        try:
            e = Employee.objects.get(id=id_empleado)
            datos = json.loads(request.body)

            # Actualizamos campos básicos
            e.first_name = datos.get('first_name', e.first_name)
            e.last_name = datos.get('last_name', e.last_name)
            e.title = datos.get('title', e.title)
            e.city = datos.get('city', e.city)
            e.reports_to_id = datos.get('reports_to_id', e.reports_to_id)

            e.save()

            return JsonResponse({
                "mensaje": f"Empleado {id_empleado} actualizado",
                "datos_actuales": {
                    "nombre": f"{e.first_name} {e.last_name}",
                    "cargo": e.title
                }
            })

        except Employee.DoesNotExist:
            return JsonResponse({"error": "El empleado no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)

@csrf_exempt
def eliminar_empleado(request, id_empleado):
    if request.method == 'DELETE':
        try:
            e = Employee.objects.get(id=id_empleado)
            e.delete()
            return JsonResponse({"mensaje": f"Empleado {id_empleado} eliminado"})
        except Employee.DoesNotExist:
            return JsonResponse({"error": "No existe"}, status=404)
        except Exception as e:
            # Error común: No puedes borrar a un jefe si tiene empleados a cargo
            # o si el empleado ya realizó ventas (Orders).
            return JsonResponse({
                "error": "No se puede eliminar: el empleado tiene subordinados o registros de ventas"
            }, status=400)

    return JsonResponse({"error": "Solo se permite DELETE"}, status=405)