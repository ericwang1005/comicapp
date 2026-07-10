from django.core.management.base import BaseCommand

import crawl.crawler as crawling
from main.models import Comic


class Command(BaseCommand):
    help = '爬取首頁推薦漫畫並更新資料庫，供 index 頁讀取（取代每次請求即時爬蟲）'

    URL = 'https://www.manhuaren.com/search/'

    def handle(self, *args, **options):
        datas = crawling.quick_pick_comic(self.URL)
        if not datas:
            self.stdout.write(self.style.WARNING('沒有爬到任何漫畫，資料庫未更新'))
            return

        created, updated = 0, 0
        for data in datas:
            title, new_update, comic_url, img_url = data[0], data[1], data[2], data[-1]
            _, is_created = Comic.objects.update_or_create(
                comic_url=comic_url,
                defaults={
                    'title': title,
                    'new_update': new_update,
                    'img_url': img_url,
                },
            )
            if is_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'完成：新增 {created} 部、更新 {updated} 部漫畫'))
