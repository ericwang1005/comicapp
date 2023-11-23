from django.shortcuts import render
from django.http import HttpResponse
import crawl.crawler as crawling
from selenium.webdriver.common.by import By
import time
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


def scroll_window(chrome, start=0, end=10000, step=500, delay_time=0.5):
    while start <= end:
        chrome.execute_script(f'window.scrollTo({start},{start+step})')
        start += step
        time.sleep(delay_time)
