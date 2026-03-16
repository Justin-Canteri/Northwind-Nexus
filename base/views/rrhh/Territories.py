import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.rrhh import Territory, Region # Importamos ambos para validar la región

def buscar_territorios(request):
    # 1. Filtramos por descripción o por ID de región
    descripcion = request.GET.get('nombre')
    region_id = request.GET.get('region')

    if descripcion:
        resultados = Territory.objects.filter(description__icontains=descripcion)
    elif region_id:
        resultados = Territory.objects.filter(region_id=region_id)
    else:
        # Traemos los primeros 10 si no hay filtros
        resultados = Territory.objects.all()[:10]
        
    # 3. Respuesta en HTML
    respuesta_texto = "<h1>Territorios Northwind:</h1><ul>"
    
    for t in resultados:
        # t.region.description accede a la tabla Region gracias al ForeignKey
        respuesta_texto += f"<li>ID: {t.id} - Territorio: {t.description.strip()} - Región: {t.region.description.strip()}</li>"
    
    respuesta_texto += "</ul>"

    return HttpResponse(respuesta_texto)

@csrf_exempt
def crear_territorio(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            # Creamos el territorio
            # Nota: id es CharField, hay que mandarlo (ej: "02139")
            nuevo_territorio = Territory.objects.create(
                id=datos.get('id'),
                description=datos.get('description'),
                region_id=datos.get('region_id') # Solo pasamos el ID de la región
            )

            return JsonResponse({
                "mensaje": "Territorio creado con éxito",
                "id": nuevo_territorio.id,
                "region": nuevo_territorio.region.description.strip()
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)

@csrf_exempt
def editar_territorio(request, id_territorio):
    if request.method == 'PUT':
        try:
            t = Territory.objects.get(id=id_territorio)
            datos = json.loads(request.body)

            t.description = datos.get('description', t.description)
            t.region_id = datos.get('region_id', t.region_id)

            t.save()

            return JsonResponse({
                "mensaje": f"Territorio {id_territorio} actualizado",
                "datos": {
                    "descripcion": t.description.strip(),
                    "region": t.region.description.strip()
                }
            })

        except Territory.DoesNotExist:
            return JsonResponse({"error": "No existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)

@csrf_exempt
def eliminar_territorio(request, id_territorio):
    if request.method == 'DELETE':
        try:
            t = Territory.objects.get(id=id_territorio)
            t.delete()
            return JsonResponse({"mensaje": f"Territorio {id_territorio} eliminado"})
        except Territory.DoesNotExist:
            return JsonResponse({"error": "No existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "No se puede eliminar: tiene empleados asignados"}, status=400)

    return JsonResponse({"error": "Solo se permite DELETE"}, status=405)