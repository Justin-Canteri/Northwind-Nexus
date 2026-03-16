import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.ventas import Shipper # Importación desde tu módulo de ventas

def buscar_shippers(request):
    # 1. Obtenemos el parámetro de búsqueda por nombre
    nombre_buscado = request.GET.get('nombre')

    # 2. Filtramos en la DB
    if nombre_buscado:
        resultados = Shipper.objects.filter(company_name__icontains=nombre_buscado)
    else:
        # Son pocos transportistas, así que podemos traer todos
        resultados = Shipper.objects.all()
        
    # 3. Respuesta en HTML
    respuesta_texto = "<h1>Transportistas Northwind:</h1><ul>"
    
    for s in resultados:
        respuesta_texto += f"<li>ID: {s.id} - Empresa: {s.company_name} - Teléfono: {s.phone}</li>"
    
    respuesta_texto += "</ul>"

    return HttpResponse(respuesta_texto)

@csrf_exempt
def crear_shipper(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            # En esta tabla el ID es AutoField, así que no hace falta enviarlo
            nuevo_shipper = Shipper.objects.create(
                company_name=datos.get('company_name'),
                phone=datos.get('phone')
            )

            return JsonResponse({
                "mensaje": "Transportista creado con éxito",
                "id_asignado": nuevo_shipper.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)

@csrf_exempt
def editar_shipper(request, id_shipper):
    if request.method == 'PUT':
        try:
            s = Shipper.objects.get(id=id_shipper)
            datos = json.loads(request.body)

            s.company_name = datos.get('company_name', s.company_name)
            s.phone = datos.get('phone', s.phone)

            s.save()

            return JsonResponse({
                "mensaje": f"Transportista {id_shipper} actualizado",
                "datos": {
                    "empresa": s.company_name,
                    "telefono": s.phone
                }
            })

        except Shipper.DoesNotExist:
            return JsonResponse({"error": "No existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)

@csrf_exempt
def eliminar_shipper(request, id_shipper):
    if request.method == 'DELETE':
        try:
            s = Shipper.objects.get(id=id_shipper)
            s.delete()
            return JsonResponse({"mensaje": f"Transportista {id_shipper} eliminado"})
        except Shipper.DoesNotExist:
            return JsonResponse({"error": "No existe"}, status=404)
        except Exception as e:
            # Igual que con Clientes, si ya se usó en una Orden, dará error de integridad
            return JsonResponse({"error": "No se puede eliminar: tiene pedidos asociados"}, status=400)

    return JsonResponse({"error": "Solo se permite DELETE"}, status=405)