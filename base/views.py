from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto  # Tu "mapa"
from django.views.decorators.csrf import csrf_exempt #para que postman entre sin seguridad

# Create your views here.


def hola(request):
    return HttpResponse ("hola")

def buscar(request):
    # 1. Obtenemos el parámetro de la URL: ?nombre=Chai
    nombre_buscado = request.GET.get('nombre')

    # 2. Hacemos el GET a la DB de Northwind
    if nombre_buscado:
        # SELECT * FROM products WHERE product_name ILIKE '%valor%'
        resultados = Producto.objects.only('nombre', 'precio').filter(nombre__icontains=nombre_buscado) # es basicamente el sql de django
    else:
        # Si no hay búsqueda, traemos los primeros 10
        resultados = Producto.objects.only('nombre', 'precio').all()#[:10] #en caso de que quiera limitar la cantidad de elementos que llame
        
    # 3. Construimos la respuesta manual (HttpResponse)
    # Creamos una lista de texto con los datos de la DB
    respuesta_texto = "<h1>Resultados de Northwind:</h1><ul>"
    
    for p in resultados:
        respuesta_texto += f"<li>Producto: {p.nombre} - Precio: ${p.precio}</li>"
    
    respuesta_texto += "</ul>"

    # 4. Enviamos el paquete al navegador
    return HttpResponse(respuesta_texto)

@csrf_exempt # Esto es para que Postman pueda entrar sin el token de seguridad de Django
def crear_producto(request):
    if request.method == 'POST':
        # Extraemos cada dato que enviaremos desde Postman
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        cat_id = request.POST.get('categoria_id')
        prov_id = request.POST.get('proveedor_id')
        cant_unid = request.POST.get('cantidad_por_unidad')
        desc = request.POST.get('descontinuado', 0) # Valor por defecto 0

        # Guardamos en la base de datos Northwind usando el "Mapa" (Model)
        nuevo = Producto.objects.create(
            nombre=nombre,
            precio=precio,
            stock=stock,
            categoria_id=cat_id,
            proveedor_id=prov_id,
            cantidad_por_unidad=cant_unid,
            descontinuado=desc
        )

        return HttpResponse(f"Éxito: Producto '{nuevo.nombre}' creado con ID {nuevo.id}")
    
    return HttpResponse("Esta ruta solo acepta POST", status=405)