from django.shortcuts import render
from django.http import HttpResponse
import crawl.crawler as crawling
from selenium.webdriver.common.by import By
# Create your views here.
url = 'https://www.manhuaren.com/search/'


def index(request):
    global url
    datas = quick_pick_comic(url)
    context = {}
    for data in datas:
        context['title'] = data[0]
        context['new_update'] = data[1]
        context['comic_url'] = data[2]
        context['img_url'] = data[-1]
        return render(request, 'index.html', locals())


def quick_pick_comic(url):
    datas = []
    chrome = crawling.get_chrome(url, hide=True)
    comic_xpath = '/html/body/ul[1]/li[1]/a'
    chrome.find_element(By.XPATH, comic_xpath).click()
    soup = crawling.BeautifulSoup(chrome.page_source, 'lxml')
    if soup != None:
        content = soup.find('ul', class_="manga-list-2").findAll('li')
    try:
        for comic in content:
            title = [title.text.strip() for title in comic][3]
            new_update = [title.text.strip() for title in comic][-2]
            comic_url = 'https://www.manhuaren.com'+comic.find('a').get('href')
            img_url = comic.find('img').get('src')
            datas.append([title, new_update, comic_url, img_url])
    except Exception as e:
        print(e)
    finally:
        if chrome != None:
            chrome.close()
    return datas


def home(request):
    return render(request, 'home.html')


def books(request):
    return render(request, 'books.html')


def favorite(request):
    return render(request, 'favorite.html')
