import datetime
import json
import asyncio
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# from aiohttp import ClientSession
from django.utils.text import slugify
from urllib.parse import urljoin

from alert.models import Movie, Region, Genre, Date

type_codes = ["MOVIE", "TV", "TV_EPISODE"]


def get_regions(page):
    soup = BeautifulSoup(page, "lxml")
    options = soup.select("select[id='country-selector'] option")
    regions = [{"country": option.get_text(strip=True), "code": option.get("value")} for option in options]
    with open(f"jobs/regions.json", "w") as file:
      json.dump(regions, file, indent=4)
    return "done"


def get_type(page):
    url = "https://www.imdb.com"
    soup = BeautifulSoup(page, "lxml")
    items = soup.select("a.ipc-chip--on-base")
    typs = [
        {"type": item.span.text.strip(), "url": urljoin(url, item.get("href"))}
        for item in items
    ]
    return typs


async def fetch(url, session, type, region):
    async with session.get(url) as resp:
        html_body = await resp.read()
        return {"page": html_body, "type": type, "region": region}


async def get_pages():
    tasks = []

    async with ClientSession() as session:
        regions = Region.objects.all()

        for region in regions:
            types = Movie.TypeChoice.choices
            types = [type[0] for type in types]
            for typ in types:
                url = f"https://www.imdb.com/calendar/?ref_=rlm&region={region.code}&type={typ}"
                # tasks.append(
                #     asyncio.create_task(fetch(url, session))
                # )
                tasks.append(asyncio.create_task(fetch(url, session, typ, region)))
        pages_content = await asyncio.gather(*tasks)
        return pages_content


def parse_page(obj):
    page = obj["page"]
    obj_type = obj["type"]
    region = obj["region"]

    soup = BeautifulSoup(page, "html.parser")
    articles = soup.select("article[data-testid='calendar-section']")

    for article in articles:
        date = article.select_one("div[data-testid='release-date'] h3").text.strip()

        items = article.select("li[data-testid='coming-soon-entry']")
        for item in items:
            title = item.select_one(
                "div.ipc-metadata-list-summary-item__tc a"
            ).text.strip()
            try:
                image = item.select_one("div.ipc-poster__poster-image img").get("src")
            except:
                image = ""
            grs = item.select(
                "div.ipc-metadata-list-summary-item__tc ul.ipc-metadata-list-summary-item__tl li"
            )
            genres = [g.label.text.strip() for g in grs]
            cts = item.select(
                "div.ipc-metadata-list-summary-item__tc ul.ipc-metadata-list-summary-item__stl li"
            )
            casts = [c.label.text.strip() for c in cts]

            save(date, title, image, obj_type, region, casts=casts, genres=genres)
    return


def save(date, title, image, obj_type, region, **kwargs):
    date = datetime.datetime.strptime(date, "%b %d, %Y")
    date_obj = Date.objects.get_or_create(date=date)[0]
    print(date.date)
    genres_obj = []
    for genre in kwargs["genres"]:
        g = Genre.objects.filter(slug=slugify(genre))
        if not g.exists():
            g = Genre.objects.create(name=genre, slug=slugify(genre), is_movie=True)
        else:
            g = g[0]
            g.is_game = True 
            g.save()
        genres_obj.append(g)
    casts = str(kwargs["casts"]).replace("[", "").replace("]", "").replace("'", "")

    if not Movie.objects.filter(slug=slugify(title)).exists():
        movie = Movie.objects.create(
            title=title,
            image=image,
            casts=casts,
            date=date_obj,
            type=Movie.TypeChoice[obj_type],
            region=region,
        )
        for obj in genres_obj:
            movie.genres.add(obj)
        movie.save()
        print(f"Saved {movie.title}")
    return


def main():
    objects = asyncio.run(get_pages())
    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, objects)


if __name__ == "__main__":
    with open("imdb_calender.html", "r") as file:
        context = {
            "page": file.read(),
            "region": Region.objects.get(code="TR"),
            "type": "MOVIE",
        }

        print(parse_page(context))
