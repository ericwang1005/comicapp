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
