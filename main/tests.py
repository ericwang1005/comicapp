from unittest.mock import patch

from django.test import Client, TestCase

from main.models import Comic


class ViewSmokeTests(TestCase):
    """基本 smoke test：確認各頁面可正常回應，且首頁已從即時爬蟲抽離為讀 DB。"""

    def test_index_empty_db_returns_200(self):
        """DB 為空時首頁仍正常渲染（不再依賴即時爬蟲開 Chrome）。"""
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_index_shows_comics_from_db(self):
        """首頁顯示資料庫中的漫畫（fetch_comics 寫入後的資料來源）。"""
        Comic.objects.create(
            title='測試漫畫',
            new_update='第1話',
            comic_url='https://example.com/comic/1',
            img_url='https://example.com/1.jpg',
        )
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '測試漫畫')

    def test_static_pages_return_200(self):
        for path in ['/home.html', '/books.html', '/favorite.html', '/login.html']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    @patch('crawl.crawler.search_comic', return_value=[])
    def test_search_get_returns_200(self, mock_search):
        """搜尋維持即時爬（此處 mock 掉爬蟲），GET 應正常回應。"""
        resp = self.client.get('/search.html', {'key': 'test'})
        self.assertEqual(resp.status_code, 200)

    @patch('crawl.crawler.search_comic', return_value=[])
    def test_search_non_get_does_not_crash(self, mock_search):
        """P1 回歸測試：非 GET 請求不應觸發 UnboundLocalError。"""
        resp = self.client.post('/search.html')
        self.assertEqual(resp.status_code, 200)


class ComicModelTests(TestCase):
    def test_str_returns_title(self):
        comic = Comic(title='海賊王', comic_url='https://example.com/op')
        self.assertEqual(str(comic), '海賊王')


class CsrfProxyRegressionTest(TestCase):
    """回歸測試：Render 在邊緣終結 TLS 並以 HTTP 轉發，帶 https Origin 的 admin 登入 POST
    不應被 Django 4.0+ 的 CSRF Origin 檢查誤判為 403。守護 settings 的
    SECURE_PROXY_SSL_HEADER / CSRF_TRUSTED_ORIGINS；若被誤刪此測試會失敗。"""

    def test_admin_login_post_with_https_origin_not_csrf_blocked(self):
        host = 'comicapp-wccw.onrender.com'
        client = Client(enforce_csrf_checks=True)
        # GET 先取得 csrftoken（GET 不觸發 Origin 檢查）
        get_resp = client.get('/admin/login/', SERVER_NAME=host,
                              HTTP_X_FORWARDED_PROTO='https')
        token = get_resp.cookies['csrftoken'].value
        # 模擬 Render：wsgi scheme 是 http，但帶 X-Forwarded-Proto=https 與 https Origin
        resp = client.post(
            '/admin/login/',
            {'username': 'x', 'password': 'y',
             'csrfmiddlewaretoken': token, 'next': '/admin/'},
            SERVER_NAME=host,
            HTTP_ORIGIN='https://comicapp-wccw.onrender.com',
            HTTP_X_FORWARDED_PROTO='https',
        )
        self.assertNotEqual(
            resp.status_code, 403,
            'admin 登入被 CSRF Origin 檢查誤判 403，請確認 settings 的 '
            'SECURE_PROXY_SSL_HEADER 設定仍在')
