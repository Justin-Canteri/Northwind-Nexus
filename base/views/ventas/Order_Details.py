import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ...models.ventas import OrderDetail # Importamos el modelo

def buscar_detalles(request):
    # Buscamos todos los productos de una orden específica
    id_orden = request.GET.get('orden')

    if id_orden:
        resultados = OrderDetail.objects.filter(order_id=id_orden)
    else:
        # Si no hay orden, traemos los últimos 20 detalles registrados
        resultados = OrderDetail.objects.all()[:20]
        
    respuesta_texto = f"<h1>Detalles de Órdenes Northwind:</h1><ul>"
    
    for d in resultados:
        # d.product.nombre viene de la relación con la tabla Products
        respuesta_texto += f"<li>Orden: {d.order_id} - Producto: {d.product.nombre} - Cantidad: {d.quantity} - Precio: ${d.unit_price}</li>"
    
    respuesta_texto += "</ul>"

    return HttpResponse(respuesta_texto)

@csrf_exempt
def crear_detalle(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            nuevo_detalle = OrderDetail.objects.create(
                order_id=datos.get('order_id'),
                product_id=datos.get('product_id'),
                unit_price=datos.get('unit_price'),
                quantity=datos.get('quantity'),
                discount=datos.get('discount', 0)
            )

            return JsonResponse({
                "mensaje": "Producto agregado a la orden",
                "orden": nuevo_detalle.order_id,
                "producto": nuevo_detalle.product_id
            }, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)

@csrf_exempt
def editar_detalle(request, id_orden, id_producto):
    if request.method == 'PUT':
        try:
            # Buscamos la fila exacta usando los dos IDs
            d = OrderDetail.objects.get(order_id=id_orden, product_id=id_producto)
            datos = json.loads(request.body)

            d.unit_price = datos.get('unit_price', d.unit_price)
            d.quantity = datos.get('quantity', d.quantity)
            d.discount = datos.get('discount', d.discount)

            d.save()

            return JsonResponse({
                "mensaje": "Detalle actualizado",
                "datos": {
                    "precio_venta": float(d.unit_price),
                    "cantidad": d.quantity
                }
            })

        except OrderDetail.DoesNotExist:
            return JsonResponse({"error": "No se encontró ese producto en esa orden"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)

@csrf_exempt
def eliminar_detalle(request, id_orden, id_producto):
    if request.method == 'DELETE':
        try:
            # Borramos la relación específica
            detalle = OrderDetail.objects.get(order_id=id_orden, product_id=id_producto)
            detalle.delete()
            return JsonResponse({"mensaje": f"Producto {id_producto} quitado de la orden {id_orden}"})
        except OrderDetail.DoesNotExist:
            return JsonResponse({"error": "No existe ese detalle"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite DELETE"}, status=405)