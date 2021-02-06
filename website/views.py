from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def index(request):
    return HttpResponse(render(request, 'website/website.html', {}))


@login_required
def profile(request):
    return HttpResponse(render(request, 'website/profile.html', {}))
