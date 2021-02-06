from django.shortcuts import render
from django.http import HttpResponse
from sticky_link import env


def index(request):
    return HttpResponse(render(request, 'website/index.html', {
        'env': env,
    }))
