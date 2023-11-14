from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def books(request):
    return render(request, 'books.html')


def favorite(request):
    return render(request, 'favorite.html')
