import asyncio
import datetime
from requests_html import HTMLSession
# from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from alert.models import Games, Date
from django.utils.text import slugify


async def fetch(url, session, platform):
    async with session.get(url) as resp:
        html_body = await resp.read()
        return {"page": html_body, "platform": platform}


async def get_pages(search_word):
    tasks = []

    async with ClientSession() as session:
        num = 0
        platforms = [pf[0] for pf in Games.PlatFormChoice.choices]

        for platform in platforms:
            while True:
                url = f"https://www.metacritic.com/browse/games/release-date/coming-soon/{platform}/date?page={num}"
                try:
                    tasks.append(asyncio.create_task(fetch(url, session, platform)))
                except:
                    break
                num += 1
        pages_content = await asyncio.gather(*tasks)
        return pages_content


def parse_page(obj):
    page = obj["page"]
    pf = obj["platform"]
    soup = BeautifulSoup(page, "html.parser")
    items = soup.select("div.products div.item")

    # products = []

    for item in items:
        image = item.select_one("div.img-wrap img").get("src")
        title = item.select_one("div.mid div.title").text.strip()
        # url = item.select_one("a").get("href")
        platform = item.select_one("div.platform span.data").text.strip()
        release_date = item.select_one("div.release_date").text.strip()
        summary = item.select_one("div.product_summary").text.strip().replace("\n", "")
        
        save(title, image, release_date, summary, pf)
        
        # products.append(
        #     {
        #         "title": title,
        #         "image": image,
        #         "release_date": release_date,
        #         "summary": summary,
        #         "platform": platform,
        #     }
        # )
    return


def save(title, image, release_date, summary, platform):
    date = datetime.datetime.strptime(release_date, "%b %d, %Y")
    date_obj = Date.objects.get_or_create(date=date)[0]
    if not Games.objects.filter(slug=slugify(title)).exists():
        Games.objects.create(title=title, date=date_obj, summary=summary, platform=platform, image=image)
    return


def main(search_word):
    pages = asyncio.run(get_pages(search_word))
    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, pages)


if __name__ == "__main__":
    with open("jobs/pc_games.html", "r") as file:
        print(parse_page(file.read()))
