import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

@csrf_exempt
def registrar_usuario(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            
            # Solo pedimos lo básico para la cuenta
            username = datos.get('username')
            password = datos.get('password')
            email = datos.get('email', '')

            if not username or not password:
                return JsonResponse({"error": "Usuario y contraseña son obligatorios"}, status=400)

            # Crear el usuario (contraseña encriptada automáticamente)
            nuevo_usuario = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            return JsonResponse({
                "mensaje": "Usuario creado. Ahora un administrador debe asignarle un rol.",
                "id": nuevo_usuario.id,
                "username": nuevo_usuario.username
            }, status=201)

        except IntegrityError:
            return JsonResponse({"error": "El nombre de usuario ya existe"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)