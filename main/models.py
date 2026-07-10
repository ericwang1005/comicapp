from django.db import models


class Comic(models.Model):
    """首頁推薦漫畫。由 `python manage.py fetch_comics` 爬取後寫入，
    index view 直接讀本表，避免每次請求都同步開 Chrome 爬蟲。"""
    title = models.CharField(max_length=255)
    new_update = models.CharField(max_length=255, blank=True)
    comic_url = models.URLField(max_length=500, unique=True)
    img_url = models.URLField(max_length=500, blank=True)
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fetched_at']

    def __str__(self):
        return self.title
