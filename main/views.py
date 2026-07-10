from django.shortcuts import render
from django.http import HttpResponse
import crawl.crawler as crawling
from main.models import Comic
import time
# Create your views here.


def index(request):
    comics = Comic.objects.all()
    return render(request, 'index.html', {'comics': comics})


def home(request):
    return render(request, 'home.html')


def books(request):
    return render(request, 'books.html')


def favorite(request):
    return render(request, 'favorite.html')


def search(request):
    result = []
    if request.method == 'GET':
        key = request.GET.get('key')
        datas = crawling.search_comic(keys=key)
        for data in datas:
            context = {}
            context['title'] = data[0]
            context['comic_url'] = data[1]
            context['info'] = data[2]
            context['img_url'] = data[-1]
            result.append(context)
    return render(request, 'search.html', {'comic_result': result})


def login(request):
    return render(request, 'login.html')


def scroll_window(chrome, start=0, end=10000, step=500, delay_time=0.5):
    while start <= end:
        chrome.execute_script(f'window.scrollTo({start},{start+step})')
        start += step
        time.sleep(delay_time)
