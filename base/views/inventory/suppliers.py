import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.inventory import Supplier  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt #para que postman entre sin seguridad


@csrf_exempt
def buscar(request):
    nombre_buscado = request.GET.get('nombre')

    if nombre_buscado:
        resultados = Supplier.objects.only('id','company_name', 'phone').filter(nombre__icontains=nombre_buscado)
    else:
        resultados = Supplier.objects.all()

    respuesta_texto = "<h1>Resultados de Northwind:</h1><ul>"
    
    for p in resultados:
        respuesta_texto += f"<li>categoria: id: {p.id} - {p.company_name} - phone: {p.phone}</li>"
    
    respuesta_texto += "</ul>"

    # 4. Enviamos el paquete al navegador
    return HttpResponse(respuesta_texto)

@csrf_exempt
def crear_supplier(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            nuevo_supp = Supplier.objects.create(
                id = datos.get('id') ,
                company_name = datos.get('company_name'),
                contact_name = datos.get('contact_name'),
                contact_title = datos.get('contact_title'),
                address = datos.get('address'),
                city = datos.get('city'),
                region = datos.get('region'),
                postal_code = datos.get('postal_code'),
                country = datos.get('country'),
                phone = datos.get('phone'),
                fax = datos.get('fax'),
                homepage = datos.get('homepage')
            )

            return JsonResponse({
                "mensaje": "Producto creado con éxito",
                "id_asignado": nuevo_supp.id,
                "nombre": nuevo_supp.company_name
            }, status=201)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)
    

@csrf_exempt
def delete_supplier(request, id_suppler):
    if request.method == 'DELETE':
        Supplier.objects.filter(id = id_suppler).delete()
        return JsonResponse({'mensaje': 'borrado con éxito'})    
    
@csrf_exempt
def editar_supplier(request, id_supplier):
    if request.method == 'PUT':
        try:

            p = Supplier.objects.get(id = id_supplier)

            datos = json.load(request.body)

            p.company_name = datos.get('company_name'),
            p.contact_name = datos.get('contact_name'),
            p.contact_title = datos.get('contact_title'),
            p.address = datos.get('address'),
            p.city = datos.get('city'),
            p.region = datos.get('region'),
            p.postal_code = datos.get('postal_code'),
            p.country = datos.get('country'),
            p.phone = datos.get('phone'),
            p.fax = datos.get('fax')
            p.homepage = datos.get('homepage')

            p.save()

            return JsonResponse({
                "mensaje": f"Producto {id_supplier} actualizado correctamente",
                "datos_nuevos": {
                    "nombre": p.company_name
                }
            })
        except Supplier.DoesNotExist:
            return JsonResponse({"error": "el supplier no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)