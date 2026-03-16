import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.ventas import Customer  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt


def buscar_clientes(request):
    # 1. Obtenemos el parámetro de búsqueda por nombre de empresa
    nombre_buscado = request.GET.get('nombre')

    # 2. Hacemos el filtro en la DB
    if nombre_buscado:
        # SELECT * FROM customers WHERE company_name ILIKE '%valor%'
        resultados = Customer.objects.filter(company_name__icontains=nombre_buscado)
    else:
        # Si no hay búsqueda, traemos los primeros 10 para no saturar
        resultados = Customer.objects.all()[:10]
        
    # 3. Construimos la respuesta en HTML (siguiendo tu formato de estudio)
    respuesta_texto = "<h1>Resultados de Clientes Northwind:</h1><ul>"
    
    for c in resultados:
        respuesta_texto += f"<li>ID: {c.id} - Empresa: {c.company_name} - Contacto: {c.contact_name}</li>"
    
    respuesta_texto += "</ul>"

    return HttpResponse(respuesta_texto)

@csrf_exempt
def crear_cliente(request):
    if request.method == 'POST':
        try:
            # 1. Traducimos el JSON a diccionario
            datos = json.loads(request.body)

            # 2. Creamos el cliente
            # IMPORTANTE: En Northwind el ID de cliente NO es autoincremental, son 5 letras.
            nuevo_cliente = Customer.objects.create(
                id=datos.get('id'), # Ej: 'ABCDE'
                company_name=datos.get('company_name'),
                contact_name=datos.get('contact_name'),
                contact_title=datos.get('contact_title'),
                address=datos.get('address'),
                city=datos.get('city'),
                country=datos.get('country'),
                phone=datos.get('phone')
            )

            return JsonResponse({
                "mensaje": "Cliente creado con éxito",
                "id_asignado": nuevo_cliente.id,
                "empresa": nuevo_cliente.company_name
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)

@csrf_exempt
def editar_cliente(request, id_cliente):
    if request.method == 'PUT':
        try:
            # 1. Buscamos el cliente por su ID (las 5 letras)
            c = Customer.objects.get(id=id_cliente)

            # 2. Leemos los datos nuevos
            datos = json.loads(request.body)

            # 3. Actualizamos los campos (si no vienen, dejamos el anterior)
            c.company_name = datos.get('company_name', c.company_name)
            c.contact_name = datos.get('contact_name', c.contact_name)
            c.address = datos.get('address', c.address)
            c.city = datos.get('city', c.city)
            c.phone = datos.get('phone', c.phone)

            # 4. Guardamos cambios
            c.save()

            return JsonResponse({
                "mensaje": f"Cliente {id_cliente} actualizado correctamente",
                "datos_actualizados": {
                    "empresa": c.company_name,
                    "ciudad": c.city
                }
            })

        except Customer.DoesNotExist:
            return JsonResponse({"error": "El cliente no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)

@csrf_exempt
def eliminar_cliente(request, id_cliente):
    if request.method == 'DELETE':
        try:
            # Verificamos si existe antes de borrar
            cliente = Customer.objects.get(id=id_cliente)
            cliente.delete()
            return JsonResponse({"mensaje": f"Cliente {id_cliente} eliminado con éxito"})
        except Customer.DoesNotExist:
            return JsonResponse({"error": "El cliente no existe"}, status=404)
        except Exception as e:
            # Northwind no te dejará borrar un cliente que ya tenga Órdenes (llave foránea)
            return JsonResponse({"error": "No se puede eliminar: el cliente tiene pedidos asociados"}, status=400)

    return JsonResponse({"error": "Solo se permite DELETE"}, status=405)