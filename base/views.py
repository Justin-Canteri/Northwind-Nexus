import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt #para que postman entre sin seguridad

# Create your views here.
def inicio(request):
    return HttpResponse('Pagina de inicio')

def buscar(request):
    # 1. Obtenemos el parámetro de la URL: ?nombre=Chai
    nombre_buscado = request.GET.get('nombre')

    # 2. Hacemos el GET a la DB de Northwind
    if nombre_buscado:
        # SELECT * FROM products WHERE product_name ILIKE '%valor%'
        resultados = Producto.objects.only('id','nombre', 'precio').filter(nombre__icontains=nombre_buscado) # es basicamente el sql de django
    else:
        # Si no hay búsqueda, traemos los primeros 10
        resultados = Producto.objects.only('nombre', 'precio').all()#[:10] #en caso de que quiera limitar la cantidad de elementos que llame
        
    # 3. Construimos la respuesta manual (HttpResponse)
    # Creamos una lista de texto con los datos de la DB
    respuesta_texto = "<h1>Resultados de Northwind:</h1><ul>"
    
    for p in resultados:
        respuesta_texto += f"<li>Producto: id: {p.id}- {p.nombre} - Precio: ${p.precio}</li>"
    
    respuesta_texto += "</ul>"

    # 4. Enviamos el paquete al navegador
    return HttpResponse(respuesta_texto)

@csrf_exempt
def crear_producto(request):
    if request.method == 'POST':
        try:
            # 1. "Traducimos" el JSON que viene de Postman a un diccionario
            datos = json.loads(request.body)

            # 2. Extraemos los datos del diccionario 'datos'
            # Usamos .get('campo', valor_por_defecto) para evitar errores si falta algo
            nuevo_prod = Producto.objects.create(
                id = datos.get('id'),
                nombre=datos.get('nombre'),
                precio=datos.get('precio'),
                stock=datos.get('stock'),
                categoria_id=datos.get('categoria_id'),
                proveedor_id=datos.get('proveedor_id'),
                cantidad_por_unidad=datos.get('cantidad_por_unidad'),
                descontinuado=datos.get('descontinuado', 0)
            )

            # 3. Respondemos con un JSON (es la mejor práctica)
            return JsonResponse({
                "mensaje": "Producto creado con éxito",
                "id_asignado": nuevo_prod.id,
                "nombre": nuevo_prod.nombre
            }, status=201) # 201 significa "Created"

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)


@csrf_exempt
def delete_producto(request, id_producto):
    if request.method == 'DELETE':
        Producto.objects.filter(id=id_producto).delete()
        return JsonResponse({"mensaje": "Borrado con éxito"})
 

@csrf_exempt
def editar_producto(request, id_producto):
    if request.method == 'PUT':
        try:
            # 1. Buscamos el producto que queremos editar
            # Si no existe, Django lanzará una excepción 'DoesNotExist'
            p = Producto.objects.get(id=id_producto)

            # 2. Leemos el paquete JSON con los nuevos datos
            datos = json.loads(request.body)

            # 3. Actualizamos los campos
            # Usamos datos.get('campo', p.campo) para que si no envías un campo, se quede el valor que ya tenía
            p.nombre = datos.get('nombre', p.nombre)
            p.precio = datos.get('precio', p.precio)
            p.stock = datos.get('stock', p.stock)
            p.categoria_id = datos.get('categoria_id', p.categoria_id)

            # 4. Guardamos los cambios en la DB
            p.save()

            return JsonResponse({
                "mensaje": f"Producto {id_producto} actualizado correctamente",
                "datos_nuevos": {
                    "nombre": p.nombre,
                    "precio": float(p.precio)
                }
            })

        except Producto.DoesNotExist:
            return JsonResponse({"error": "El producto no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)
