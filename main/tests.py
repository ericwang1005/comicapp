from unittest.mock import patch

from django.test import TestCase

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
