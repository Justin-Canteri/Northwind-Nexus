import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return render(request, "index.html",{"titulo": "Bienvenido a Northwind API"})


def inventario(request):
    return render(request, "inventario.html",{"titulo": "Bienvenido a inventario de Northwind API"})

def rrhh(request):
    return render(request, "rrhh.html",{"titulo": "Bienvenido a rrhh de Northwind API"})

def ventas(request):
    return render(request, "ventas.html",{"titulo": "Bienvenido a ventas de Northwind API"})