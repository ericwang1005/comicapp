from django.shortcuts import render
from django.http import HttpResponse
import crawl.crawler as crawling
from selenium.webdriver.common.by import By
# Create your views here.
url = 'https://www.manhuaren.com/search/'


def index(request):
    global url
    datas = crawling.quick_pick_comic(url)
    comics = []
    for data in datas:
        context = {}
        context['title'] = data[0]
        context['new_update'] = data[1]
        context['comic_url'] = data[2]
        context['img_url'] = data[-1]
        comics.append(context)
    return render(request, 'index.html', {'comics': comics})


def home(request):
    return render(request, 'home.html')


def books(request):
    return render(request, 'books.html')


def favorite(request):
    return render(request, 'favorite.html')
