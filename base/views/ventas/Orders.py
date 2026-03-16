import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.ventas import Order  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt


def buscar(request):
    order_buscado = request.GET.get('nombre')

    if order_buscado:
        resultado = Order.objects.filter(order_buscado = id)
    else:
        resultado = Order.objects.all()

    respuesta_texto = "<h1>Resultados de Northwind:</h1><ul>"

    for p in resultado:
        respuesta_texto += f"Order: = {p.id} -{p.customer}"

    respuesta_texto += "</ul>"

    return HttpResponse (respuesta_texto)


@csrf_exempt
def crear_order(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            # Creamos la orden con los datos que vienen de Postman
            nueva_order = Order.objects.create(
                customer_id=datos.get('customer_id'), # ID del cliente (ej: 'ALFKI')
                employee_id=datos.get('employee_id'),
                order_date=datos.get('order_date'),
                required_date=datos.get('required_date'),
                ship_via_id=datos.get('ship_via_id'), # ID del Shipper
                freight=datos.get('freight', 0),
                ship_name=datos.get('ship_name'),
                ship_address=datos.get('ship_address'),
                ship_city=datos.get('ship_city'),
                ship_country=datos.get('ship_country')
            )

            return JsonResponse({
                "mensaje": "Orden creada con éxito",
                "order_id": nueva_order.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)


@csrf_exempt
def editar_order(request, id_order):
    if request.method == 'PUT':
        try:
            o = Order.objects.get(id=id_order)
            datos = json.loads(request.body)

            # Actualizamos campos (si no vienen en el JSON, dejamos el que estaba)
            o.ship_name = datos.get('ship_name', o.ship_name)
            o.ship_address = datos.get('ship_address', o.ship_address)
            o.freight = datos.get('freight', o.freight)
            o.shipped_date = datos.get('shipped_date', o.shipped_date)

            o.save()

            return JsonResponse({
                "mensaje": f"Orden {id_order} actualizada",
                "datos": {"ship_name": o.ship_name, "flete": float(o.freight)}
            })

        except Order.DoesNotExist:
            return JsonResponse({"error": "La orden no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def eliminar_order(request, id_order):
    if request.method == 'DELETE':
        try:
            # Primero buscamos para confirmar existencia
            orden = Order.objects.get(id=id_order)
            orden.delete()
            return JsonResponse({"mensaje": f"Orden {id_order} eliminada correctamente"})
        except Order.DoesNotExist:
            return JsonResponse({"error": "La orden no existe"}, status=404)