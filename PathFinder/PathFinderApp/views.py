from django.shortcuts import render
from django.http import HttpResponse


def index(req):
    return HttpResponse("Hello, world. You're at the pathfinderapp index.")
# Create your views here.
