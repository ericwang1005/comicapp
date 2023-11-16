import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from threading import Thread


def get_chrome(url, hide=False):
    try:
        options = webdriver.ChromeOptions()
        if hide:
            options.add_argument('--headless')
        chrome = webdriver.Chrome(options=options)
        chrome.get(url)
        return chrome
    except Exception as e:
        print(e)


def getSoup(url, post_data=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    try:
        if post_data is not None:
            resp = requests.post(url, post_data, headers=headers)
        else:
            resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'lxml')
            return soup
        else:
            print('網頁取得失敗')
    except Exception as e:
        print('網址錯誤', e)


def update_btn(key):
    keys = key
    thread = Thread(target=search_comic, args=(keys,))
    thread.start()


def search_comic(keys):
    datas = []
    try:
        url = 'https://www.manhuaren.com/search/'
        chrome = get_chrome(url, hide=True)
        search_xpath = '/html/body/div[1]/div/input'
        element = chrome.find_element(By.XPATH, search_xpath)
        element.clear()
        time.sleep(1)
        element.send_keys(f'{keys}')
        time.sleep(1)
        element.send_keys(Keys.RETURN)
        confirm_xpath = '/html/body/div[1]/a[2]'
        chrome.find_element(By.XPATH, confirm_xpath).click()
        soup = BeautifulSoup(chrome.page_source, 'lxml')
        comic_list = soup.find('ul', class_="book-list").find_all('li')
        for comic in comic_list:
            link = 'https://www.manhuaren.com' + \
                comic.find('a').get('href')
            title = comic.find('a').get('title')
            info = comic.find('p', class_='book-list-info-desc').text.strip()
            img_url = comic.find('img').get('src')
            datas.append([title, link, info, img_url])
        return datas

    except Exception as e:
        print(e)
    finally:
        chrome.quit()


def quick_pick_comic(url):
    datas = []
    chrome = get_chrome(url, hide=True)
    comic_xpath = '/html/body/ul[1]/li[1]/a'
    chrome.find_element(By.XPATH, comic_xpath).click()
    scroll_window(chrome=chrome)
    soup = BeautifulSoup(chrome.page_source, 'lxml')
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


def scroll_window(chrome, start=0, end=10000, step=500, delay_time=0.5):
    while start <= end:
        chrome.execute_script(f'window.scrollTo({start},{start+step})')
        start += step
        time.sleep(delay_time)
