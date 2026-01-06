# Pokémon-sovellus

Tämä sovellus käyttää PokeAPI-rajapintaa (https://pokeapi.co/docs/v2) tiedon hakuun.

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. ✅
* Käyttäjä pystyy keräämään, muokkaamaan ja poistamaan pokemoneja. ✅
* Käyttäjä pystyy tutkimaan maailmaa ja etsimään pokemoneja maailmasta. ✅
* Käyttäjä pystyy etsimään omistamiaan pokemoneja hakusanalla. ✅
* Käyttäjä pystyy listaamaan omistamiaan pokemoneja vaihdettavaksi. ✅
* Käyttäjä näkee sovelluksen muiden käyttäjien listaamat pokemonit. ✅
* Käyttäjä pystyy etsimään listattuja pokemoneja hakusanalla. ✅
* Käyttäjä pystyy vaihtamaan pokemoneja toisen käyttäjän kanssa. ✅
* Käyttäjä pystyy selaamaan omia vaihtokauppojaan. ✅
* Käyttäjä pystyy suodattamaan omia vaihtokauppojaan hakusanalla. ✅
* Käyttäjä pystyy perumaan, hylkäämään ja hyväksymään vaihtokauppoja, joissa hän on osallisena. ✅
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja käyttäjän keräämistä pokemoneista ja vireillä olevista vaihtokaupoista. ✅

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

(**Valinnainen**) Jos haluat luoda pohjalle ison määrän dataa (käyttäjiä, pokemoneja, vaihtokauppoja) ja valmiin testikäyttäjän:

```
$ python3 seed.py
```
* Huom. Tämä vaihe **tyhjentään** tietokannan taulut ja alustaa tietokannan isolla määrällä dataa. Tietokantaan luodaan:
  * iso määrä pikachu-pokemoneja satunnaisilla statistiikoilla. Kaikki näistä ovat listattuja vaihtokaupan kohteeksi.
  * iso määrä vaihtokauppoja eri statuksilla
  * valmiin testikäyttäjän (username=test, password=test), jonka tilillä on valmiiksi iso määrä pokemoneja ja vaihtokauppatapahtumia eri statuksilla.


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
