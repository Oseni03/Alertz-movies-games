import json
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from alert.models import Region, Movie, Genre, PlatForm
from jobs import movies, games2


def load_regions() -> None:
    with open(f"jobs/regions.json", "r") as file:
        regions = json.load(file)
    for region in regions:
        country = region["country"]
        code = region["code"]
        if region["country"] is not None:
            if not Region.objects.filter(code=code).exists():
                Region.objects.create(country=country, code=code)
                print(f"Saved region: {country}")
    return


def load_genres():
    with open(f"jobs/genres.json", "r") as file:
        genres = json.load(file)
    for genre in genres:
        name = genre["name"]
        slug = genre["slug"]
        if not Genre.objects.filter(slug=slug).exists():
            Genre.objects.create(name=name, slug=slug, is_game=True)
            print(f"Saved genre: {name}")
    return


def load_platforms():
    with open(f"jobs/platforms.json", "r") as file:
        platforms = json.load(file)
    for pf in platforms:
        name = pf["name"]
        slug = pf["value"]
        if not PlatForm.objects.filter(slug=slug).exists():
            PlatForm.objects.create(name=name, slug=slug)
            print(f"Saved Platform: {name}")
    return


def load_movies():
    with open("jobs/files/imdb_calender.html", "r") as file:
        context = {
            "page": file.read(),
            "region": Region.objects.get(code="TR"),
            "type": "MOVIE"
        }
        
        movies.parse_page(context)


# def load_games():
#     with open("jobs/files/switch_games.html", "r") as file:
#         games.parse_page({"page": file.read(), "platform": "switch"})
#     with open("jobs/files/pc_games.html", "r") as file:
#         games.parse_page({"page": file.read(), "platform": "pc"})
#     with open("jobs/files/ps4_games.html", "r") as file:
#         games.parse_page({"page": file.read(), "platform": "ps4"})
#     with open("jobs/files/ps5_games.html", "r") as file:
#         games.parse_page({"page": file.read(), "platform": "ps5"})
#     with open("jobs/files/x_box_series_games.html", "r") as file:
#         games.parse_page({"page": file.read(), "platform": "xbox-series-x"})
#     with open("jobs/files/xboxone_games.html", "r") as file:
#         games.parse_page({"page": file.read(), "platform": "xboxone"})

def load_games():
    with open("jobs/files/ign_ps4.html", "r") as file:
        games2.parse_page(file.read())
    with open("jobs/files/ign_switch.html", "r") as file:
        games2.parse_page(file.read())
