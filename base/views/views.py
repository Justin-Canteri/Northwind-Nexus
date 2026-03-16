import json
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return HttpResponse('Pagina de inicio')
