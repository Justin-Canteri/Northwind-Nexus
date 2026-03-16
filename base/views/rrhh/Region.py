import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import Region # Importamos desde el nuevo módulo de RRHH

def buscar_regiones(request):
    # 1. Obtenemos el parámetro de búsqueda por descripción
    busqueda = request.GET.get('nombre')

    # 2. Hacemos el filtro en la DB
    if busqueda:
        # SELECT * FROM region WHERE region_description ILIKE '%valor%'
        resultados = Region.objects.filter(description__icontains=busqueda)
    else:
        resultados = Region.objects.all()
        
    # 3. Respuesta en HTML
    respuesta_texto = "<h1>Regiones de Operación Northwind:</h1><ul>"
    
    for r in resultados:
        # Usamos .strip() porque en la DB a veces vienen con espacios en blanco al final
        respuesta_texto += f"<li>ID: {r.id} - Descripción: {r.description.strip()}</li>"
    
    respuesta_texto += "</ul>"

    return HttpResponse(respuesta_texto)

@csrf_exempt
def crear_region(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            # Creamos la región (usando ID manual según el modelo IntegerField)
            nueva_region = Region.objects.create(
                id=datos.get('id'),
                description=datos.get('description')
            )

            return JsonResponse({
                "mensaje": "Región creada correctamente",
                "id": nueva_region.id,
                "descripcion": nueva_region.description.strip()
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)

@csrf_exempt
def editar_region(request, id_region):
    if request.method == 'PUT':
        try:
            r = Region.objects.get(id=id_region)
            datos = json.loads(request.body)

            # Actualizamos la descripción
            r.description = datos.get('description', r.description)
            r.save()

            return JsonResponse({
                "mensaje": f"Región {id_region} actualizada",
                "nueva_descripcion": r.description.strip()
            })

        except Region.DoesNotExist:
            return JsonResponse({"error": "La región no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)

@csrf_exempt
def eliminar_region(request, id_region):
    if request.method == 'DELETE':
        try:
            r = Region.objects.get(id=id_region)
            r.delete()
            return JsonResponse({"mensaje": f"Región {id_region} eliminada con éxito"})
        except Region.DoesNotExist:
            return JsonResponse({"error": "No existe"}, status=404)
        except Exception as e:
            # Nota: No podrás borrar una región si tiene Territorios asociados
            return JsonResponse({
                "error": "No se puede eliminar: existen territorios vinculados a esta región"
            }, status=400)

    return JsonResponse({"error": "Solo se permite DELETE"}, status=405)