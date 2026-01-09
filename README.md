# Pokémon-sovellus

Tämä sovellus käyttää PokeAPI-rajapintaa (https://pokeapi.co/docs/v2) tiedon hakuun.

## Sisällysluettelo
- [Sovelluksen toiminnot](#sovelluksen-toiminnot)
- [Sovelluksen asennus](#sovelluksen-asennus)
- [Sovelluksen toiminta isolla tietomäärällä](#sovelluksen-toiminta-isolla-tietomäärällä)
- [PokeAPI:n käyttö](#pokeapin-käyttö)

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
## Sovelluksen toiminta isolla tietomäärällä
Sovellukseen voi pohjaksi luoda ison tietokannan `seed.py`-tiedoston avulla. Tiedoston alussa on lista vakioita, joita muuttamalla on helppo säädellä minkälaisen tietokannan itselleen haluaa alustaa.
### Indeksien käyttö
`schema.sql`-tiedostosta näkee, että sovelluksen tietokannassa käytetään paljon indeksejä. Vaikka iso indeksien määrä hidastaa tiedon lisäämistä tauluihin, on tämä tietoinen valinta tehty optimoimaan lukunopeutta. Tämä valinta oli myös helppo tehdä ottaen huomioon kuinka applikaatio toimii: tiedon lisääminen/muokkaaminen tapahtuu käyttäjän toimesta yksi pokémon (pokemon ID) kerrallaan, kun taas tiedon hakeminen tapahtuu isommissa erissä ja mahdollisesti vaihtuvilla kriteereillä.

Esimerkiksi miljoonan pokémonin ja vaihtokauppatapahtuman tietokannassa ensimmäinen sisäänkirjautuminen testikäyttäjällä kesti useamman sekunnin (~3-9 sek). Vaikka jälkimmäiset uudelleenkirjautumiset olivat nopeampia (0,9 - 1,5 sek), [commit feaf0042ce26eaff6b733dd9cfb499a033a62dac](https://github.com/jlostaln/pokemon-app/commit/feaf0042ce26eaff6b733dd9cfb499a033a62dac) paransi huomattavasti käyttökokemusta ja teki sisäänkirjautumisesta nopeaa. Ensimmäinen kirjautuminen oli kuitenkin vielä hitaampaa (1 - 2 sek), mutta [commit f5c45ecd949e7ae047d1dbfd57fd02f1bd1a58f5](https://github.com/jlostaln/pokemon-app/commit/f5c45ecd949e7ae047d1dbfd57fd02f1bd1a58f5) teki sovelluksesta johdonmukaisesti nopean.
Sovellusta testattiin myös `10**7` (10 miljoonaa pokémonia ja kauppatapahtumaa) konfiguraatioilla ja sivut latautivat todella nopeasti. `seed.py`-tiedostoa ajaessa toki huomaa indeksien ja tietueiden määrän, sillä `10**7` alustaminen kesti tovin.
### Listatut pokémonit
Isoimmaksi haasteeksi nopeuden säilyttämiseksi isolla tietomäärällä osoittautui listattujen pokémonien näyttäminen joustavan suodatuksen kanssa (Trade Pokémon -sivu), sillä kaikki `seed.py`:n luomat pokémonit ovat listattuja vaihtokaupan kohteeksi.
Iso tietomäärä ja joustava haku eivät ole tehokas yhdistelmä. Ongelmaksi muodostui haku, joka ei hyödynnä indeksejä parhaalla tavalla (jos lainkaan):
```
    if query:
        sql += '''
            AND (pokemon.name LIKE ?
                    OR EXISTS ( SELECT 1
                                FROM pokemon_types
                                WHERE pokemon_types.pokemon_id = pokemon.id
                                AND pokemon_types.type LIKE ?))'''
        like = "%" + query + "%"
```

Käyttökokemus tuntui huomattavasti hidastuvan, kun käyttäjä meni etsimään vaihdettavia pokémoneja. Hitaimmaksi kohdaksi osoittautui sivumäärän (page_count) laskeminen.
[Commit e9b330e5b44f4ef56531394ca0b5eb936b2ccdf6](https://github.com/jlostaln/pokemon-app/commit/e9b330e5b44f4ef56531394ca0b5eb936b2ccdf6) ratkaisi ongelman. Merkittävin muutos oli jättää sivujen määrän laskeminen pois, ja ainoastaan tarkistaa onko olemassa vielä seuraava sivu, johon käyttäjä voisi siirtyä. Myös aputaulu `listed_pokemon` tehosti suuren määrän kyselyä. Parannuksen jälkeen sivullinen pokémoneja hakusanasta riippumatta latautuu 0,01 sek ajassa, edellä kuvatusta kyselystä huolimatta.

Tässä vaiheessa testauksessa ilmeni kuitenkin vielä ongelma tehokkuuden kanssa, kun:
* tietokannassa miljoonia listattuja pokémoneja, mutta
* esimerkiksi vain yksi pokémon, jonka tyyppi = "ice" tai vain yksi "golbat"-niminen.

Käyttäjän hakiessa hakusanalla, jonka tulos on tyhjä, yksi tai vain muutama pokémon, haku kesti 40-60 sek.
Muuttamalla haun joustavuutta
* tästä `LIKE '%hakusana%'`
* tähän `LIKE 'hakusana%'`

tyhjien tai harvinaisten tulosten hakeminen kesti 1,20 - 2 sek, kun taas useamman sivun haut pysyivät nopeana 0,01 sek. [Commit 2271b962adf1df938a8a8eba0bd425a089db9788](https://github.com/jlostaln/pokemon-app/commit/2271b962adf1df938a8a8eba0bd425a089db9788) muutti listattujen pokémonien kyselyn pullonkaulan seuraavaan muotoon ja teki hausta siedettävän myös hitaimmillaan:
```
    if query:
        sql += '''
            AND (pokemon.name LIKE ?
                    OR EXISTS ( SELECT 1
                                FROM pokemon_types
                                WHERE pokemon_types.pokemon_id = pokemon.id
                                AND pokemon_types.type LIKE ?))'''
        like = query + "%"
```

Sovelluksen luonne huomioon ottaen, vastaavaa muutosta ei tarvitse tehdä muihin osiin sovellusta.
Pääsyy tähän on se, että on epärealistista odottaa että käyttäjä itse keräisi pokémoneja sellaisen määrän, että haut hänen keräämien pokémonien joukosta vaatisi vastaavaa muutosta.

On käyttökokemuksen kannalta parempi, että käyttäjällä on joustavampi haku etsiessään omistamiaan pokémoneja kuin että hänellä olisi optimoitu haku siltä varalta, että hän olisi kerännyt 100 000 tai miljoona pokémonia itse yksi kerrallaan.
Listattujen pokémonien kohdalla tilanne on toinen, koska sivulle tulee myös muiden käyttäjien listaamat pokémonit.


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
