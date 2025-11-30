# Pokémon-sovellus

Tämä sovellus käyttää PokeAPI-rajapintaa (https://pokeapi.co/docs/v2) tiedon hakuun.

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. ✅
* Käyttäjä pystyy keräämään, muokkaamaan ja poistamaan pokemoneja. ✅
* Käyttäjä pystyy tutkimaan maailmaa ja etsimään pokemoneja maailmasta. ✅
* Käyttäjä pystyy kehittämään keräämiään pokemoneja.
* Käyttäjä näkee sovelluksen muiden käyttäjien keräämät pokemonit.
* Käyttäjä pystyy etsimään pokemoneja hakusanalla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän keräämät pokemonit. ✅
* Sovelluksessa on leaderboard, joka listaa käyttäjät ja lajittelee käyttäjät kerättyjen pokemonien perusteella.
* Käyttäjä pystyy valitsemaan maksimissaan 6 keräämistään pokemoneista, jotka kulkevat pelaajan mukana.
* Käyttäjä pystyy vaihtamaan pokemoneja toisen käyttäjän kanssa.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

## PokeAPI:n käyttö

Sovellus käyttää PokeAPI:n tarjoamaa rajapintaa Pokémon-maailman tietojen hakemiseen. 
Sovellus hakee maailman tiedot käyttäjän selatessa maailman alueita ja etsiessään "villejä" pokémoneja. Välttääkseen turhia API-kutsuja, sovellukseen on kehitetty välimuistina toimiva tietorakenne, joka tallentaa jokaisen kutsun URL-osoitteen ja raakadatan. Seuraavalla kerralla kutsu haetaan välimuistista API-kutsun sijaan. Välimuisti on toteutettu **pokecache.py** -moduuliin ja sitä käyttää **pokeapi.py** -moduuli. Pokémonit lisätään tietokantaan, kun käyttäjä kerää niitä.

### PokeAPI:n etusivu 

https://pokeapi.co/docs/v2


### Esimerkki alueiden tiedoista:

https://pokeapi.co/api/v2/location-area/

https://pokeapi.co/api/v2/location-area/great-marsh-area-6

### Esimerkki Pikachun tiedoista

https://pokeapi.co/api/v2/pokemon/pikachu

https://pokeapi.co/api/v2/pokemon-species/25/

https://pokeapi.co/api/v2/evolution-chain/10/

