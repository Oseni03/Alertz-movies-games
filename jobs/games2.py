import json
import asyncio
import datetime
from pprint import pprint 
from requests_html import HTMLSession
# from aiohttp import ClientSession
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from alert.models import Games, Date, Genre, PlatForm
from django.utils.text import slugify


async def fetch(url, session, platform):
    async with session.get(url) as resp:
        html_body = await resp.read()
        return html_body


async def get_pages(search_word):
    tasks = []

    async with ClientSession() as session:
        platforms = PlatForm.objects.all()

        for platform in platforms:
            url = f"https://www.ign.com/upcoming/games/{platform.slug}"
            try:
                tasks.append(asyncio.create_task(fetch(url, session, platform)))
            except:
                continue
        pages_content = await asyncio.gather(*tasks)
        return pages_content


def get_platforms(page):
    soup = BeautifulSoup(page, "html.parser")
        
    platforms = []
    
    options = soup.select("select#platformSlug option")[1:]
    platforms = [
        {"name": option.get_text(strip=True), "value": option.get("value")}
        for option in options
    ]
    with open(f"jobs/platforms.json", "w") as file:
        json.dump(platforms, file, indent=4)
    return "done"


def get_genres(page):
    soup = BeautifulSoup(page, "html.parser")
        
    options = soup.select("select#genreSlug option")[1:]
    genres = [
        {"name": option.get_text(strip=True), "slug": option.get("value")}
        for option in options
    ]
    with open(f"jobs/genres.json", "w") as file:
        json.dump(genres, file, indent=4)
    return "done"


def parse_page(page):
    soup = BeautifulSoup(page, "html.parser")
    games = []
    
    items = soup.select("div.card-grid-wrapper a.object-card")
    
    for item in items:
        image = item.select_one("figure.aspect-ratio img").get("src", None)
        title = item.select_one("div.details div.title").text.strip()
        genres = item.select_one("div.details div.attribute-label").text.strip().split(", ")
        pfs = item.select("div.details div.platforms span.platform-icon")
        platforms = [pf.get("data-cy") for pf in pfs]
        date = item.select_one("div.details time.release-date").text.strip()
        
        games.append({
            "title": title,
            "image": image,
            "genres": genres,
            "platforms": platforms,
            "date": date,
        })
        save(title, image, date, genres, platforms)
    return games


def save(title, image, release_date, genres, platforms):
    try:
        date = datetime.datetime.strptime(release_date, "%b %d, %Y")
    except:
        return
    date_obj = Date.objects.get_or_create(date=date)[0]
    date_obj.has_games = True 
    date_obj.save()
    
    genres_obj = []
    for genre in genres:
        g = Genre.objects.filter(slug=slugify(genre))
        if not g.exists():
            g = Genre.objects.create(name=genre, slug=slugify(genre), is_game=True)
        else:
            g = g[0]
            g.is_game = True 
            g.save()
        genres_obj.append(g)
            
    pfs = []
    for platform in platforms:
        print(platform)
        pf = PlatForm.objects.filter(slug=platform)
        if not pf.exists():
            pf = PlatForm.objects.create(name=platform.replace("-", " ").title(), slug=platform)
        else:
            pf = pf.get()
        pfs.append(pf)
        
    if not Games.objects.filter(slug=slugify(title)).exists():
        gen_list = str(genres).replace("[", "").replace("]", "").replace("'", "")
        game = Games.objects.create(title=title, date=date_obj, image=image, genres_list=gen_list)
        for genre in genres_obj:
            game.genres.add(genre)
        for pf in pfs:
            game.platforms.add(pf)
        game.save()
    print("Saved Game:" + title)


def main(search_word):
    pages = asyncio.run(get_pages(search_word))
    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, pages)


if __name__ == "__main__":
    with open("jobs/ign_ps4.html", "r") as file:
        games = parse_page(file.read())
        print(games)
        # with open(f"games.json", "w") as file:
        #     json.dump(games, file, indent=4)
