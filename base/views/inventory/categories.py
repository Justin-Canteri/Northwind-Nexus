import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from ...models.inventory import categories  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt #para que postman entre sin seguridad

def buscar(request):
    # 1. Obtenemos el parámetro de la URL: ?nombre=Chai
    nombre_buscado = request.GET.get('nombre')

    # 2. Hacemos el GET a la DB de Northwind
    if nombre_buscado:
        # SELECT * FROM products WHERE product_name ILIKE '%valor%'
        resultados = categories.objects.only('id','nombre', 'descripcion').filter(nombre__icontains=nombre_buscado) # es basicamente el sql de django
    else:
        # Si no hay búsqueda, traemos los primeros 10
        resultados = categories.objects.only('id','nombre', 'descripcion').all()#[:10] #en caso de que quiera limitar la cantidad de elementos que llame
        
    # 3. Construimos la respuesta manual (HttpResponse)
    # Creamos una lista de texto con los datos de la DB
    respuesta_texto = "<h1>Resultados de Northwind:</h1><ul>"
    
    for p in resultados:
        respuesta_texto += f"<li>categoria: id: {p.id} - {p.nombre} - descripcion: {p.descripcion}</li>"
    
    respuesta_texto += "</ul>"

    # 4. Enviamos el paquete al navegador
    return HttpResponse(respuesta_texto)

    
@csrf_exempt
def crear_categoria(request):
    if request.method == 'POST':
        try:
            # 1. "Traducimos" el JSON que viene de Postman a un diccionario
            datos = json.loads(request.body)

            # 2. Extraemos los datos del diccionario 'datos'
            # Usamos .get('campo', valor_por_defecto) para evitar errores si falta algo
            nuevo_prod = categories.objects.create(
                id = datos.get('id'),
                nombre=datos.get('nombre'),
                descripcion =datos.get('descripcion')
            )

            # 3. Respondemos con un JSON (es la mejor práctica)
            return JsonResponse({
                "mensaje": "categoria creada con éxito",
                "id_asignado": nuevo_prod.id,
                "nombre": nuevo_prod.nombre
            }, status=201) # 201 significa "Created"

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite POST"}, status=405)

@csrf_exempt
def delete_categoria(request, id_producto):
    if request.method == 'DELETE':
        categories.objects.filter(id=id_producto).delete()
        return JsonResponse({"mensaje": "Borrado con éxito"})

@csrf_exempt
def editar_categoria(request, id_producto):
    if request.method == 'PUT':
        try:
            # 1. Buscamos el producto que queremos editar
            # Si no existe, Django lanzará una excepción 'DoesNotExist'
            p = categories.objects.get(id=id_producto)

            # 2. Leemos el paquete JSON con los nuevos datos
            datos = json.loads(request.body)

            # 3. Actualizamos los campos
            # Usamos datos.get('campo', p.campo) para que si no envías un campo, se quede el valor que ya tenía
            p.nombre = datos.get('nombre', p.nombre)
            p.descripcion = datos.get('precio', p.descripcion)
            

            # 4. Guardamos los cambios en la DB
            p.save()

            return JsonResponse({
                "mensaje": f"Producto {id_producto} actualizado correctamente",
                "datos_nuevos": {
                    "nombre": p.nombre,
                    "descripcion": p.descripcion
                }
            })

        except categories.DoesNotExist:
            return JsonResponse({"error": "la categoria no existe"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Solo se permite PUT"}, status=405)