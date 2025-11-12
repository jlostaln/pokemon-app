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


    def get_pokemon_details(self, name):
        url = self.base_url + "/pokemon/" + name
        pokemon = self.get_data(url)

        return pokemon

    def get_pokemon_additional_info(self, pokemon):
        info = {}
        species_url = pokemon["species"]["url"]
        species = self.get_data(species_url)

        for entry in species["flavor_text_entries"]:
            if entry["language"]["name"] == "en":
                info["flavor_text"] = entry["flavor_text"]
                break

        evolution_chain_url = species["evolution_chain"]["url"]
        evolution_chain = self.get_data(evolution_chain_url)

        def find_next_evolution(chain, name):
            if chain["species"]["name"] == name:
                if chain["evolves_to"]:
                    return chain["evolves_to"][0]["species"]["name"]
                else:
                    return None
            for evolution in chain["evolves_to"]:
                result = find_next_evolution(evolution, name)
                if result:
                    return result
            return None

        name = pokemon["name"]
        next_evolution = find_next_evolution(evolution_chain["chain"], name)
        info["next_evolution"] = next_evolution

        return info


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

