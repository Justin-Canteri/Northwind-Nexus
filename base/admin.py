from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.apps import apps

# Obtenemos todos los modelos de tu app 'base'
modelos_base = apps.get_app_config('base').get_models()

for modelo in modelos_base:
    try:
        admin.site.register(modelo)
    except admin.sites.AlreadyRegistered:
        # Si ya está registrado por alguna razón, ignoramos el error y seguimos
        pass 