import urllib.request
import json
import pokecache
import config

class PokeApi:
    def __init__(self):
        self.cache = pokecache.Cache()
        self.base_url = config.BASE_URL


    def get_data(self, url):
        data = self.cache.get(url)
        if not data:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = response.read()
                self.cache.add(url, data)

        return json.loads(data)


    def get_location_areas(self, page_url=None):
        url = self.base_url + "/location-area/"
        if page_url:
            url = page_url

        locations_data = self.get_data(url)

        areas = locations_data["results"]
        next_url = locations_data["next"]
        previous_url = locations_data["previous"]

        return areas, next_url, previous_url, url


    def get_encounters(self, area_name):
        url = self.base_url + "/location-area/" + area_name
        encounters = self.get_data(url)

        return encounters["pokemon_encounters"]

