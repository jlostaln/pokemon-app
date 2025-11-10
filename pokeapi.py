import urllib.request
import json
import pokecache

class PokeApi:
    def __init__(self):
        self.cache = pokecache.Cache()


    def get_data(self, url):
        data = self.cache.get(url)
        if not data:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = response.read()
                self.cache.add(url, data)

        return json.loads(data)


    def get_location_areas(self, url):
        locations_data = self.get_data(url)

        areas = locations_data["results"]
        next = locations_data["next"]
        previous = locations_data["previous"]

        return areas, next, previous


    def get_encounters(self, url):
        encounters = self.get_data(url)

        return encounters["pokemon_encounters"]

