# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:60:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:78:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:94:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:111:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:136:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:136:0: R0914: Too many local variables (16/15) (too-many-locals)
app.py:181:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:181:0: R0914: Too many local variables (20/15) (too-many-locals)
app.py:236:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:262:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:289:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:311:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:325:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:333:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:370:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:380:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:390:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:390:0: R0914: Too many local variables (19/15) (too-many-locals)
app.py:433:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:443:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:448:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:470:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:477:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:481:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:499:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:520:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:527:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:531:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module pokeapi
pokeapi.py:1:0: C0114: Missing module docstring (missing-module-docstring)
pokeapi.py:8:0: C0115: Missing class docstring (missing-class-docstring)
pokeapi.py:14:4: C0116: Missing function or method docstring (missing-function-docstring)
pokeapi.py:28:4: C0116: Missing function or method docstring (missing-function-docstring)
pokeapi.py:34:4: C0116: Missing function or method docstring (missing-function-docstring)
pokeapi.py:71:4: C0116: Missing function or method docstring (missing-function-docstring)
pokeapi.py:86:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module pokecache
pokecache.py:1:0: C0114: Missing module docstring (missing-module-docstring)
pokecache.py:3:0: C0115: Missing class docstring (missing-class-docstring)
pokecache.py:3:0: R0903: Too few public methods (0/2) (too-few-public-methods)
pokecache.py:8:0: C0115: Missing class docstring (missing-class-docstring)
pokecache.py:12:4: C0116: Missing function or method docstring (missing-function-docstring)
pokecache.py:15:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module pokemon
pokemon.py:1:0: C0114: Missing module docstring (missing-module-docstring)
pokemon.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:83:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:87:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:91:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:96:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:96:0: R0913: Too many arguments (8/5) (too-many-arguments)
pokemon.py:96:0: R0917: Too many positional arguments (8/5) (too-many-positional-arguments)
pokemon.py:105:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:109:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:113:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:118:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:122:0: C0116: Missing function or method docstring (missing-function-docstring)
pokemon.py:137:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module trades
trades.py:1:0: C0114: Missing module docstring (missing-module-docstring)
trades.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:87:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:99:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:114:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:131:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:135:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:143:0: C0116: Missing function or method docstring (missing-function-docstring)
trades.py:147:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:80:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:102:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:1:0: R0801: Similar lines in 2 files
==pokemon:[47:54]
==users:[27:34]
    if query:
        sql += '''
            AND (pokemon.name LIKE ?
                    OR EXISTS ( SELECT 1
                                FROM pokemon_types
                                WHERE pokemon_types.pokemon_id = pokemon.id
                                AND pokemon_types.type LIKE ?))''' (duplicate-code)

------------------------------------------------------------------
Your code has been rated at 8.70/10 (previous run: 8.70/10, +0.00)
```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan sovelluskehittäjän päätöksiä olla korjaamatta ehdotuksia.

## Muuttujien määrä

Raportista löytyy muutama ilmoitus liittyen muuttujien suureen määrään:

```
app.py:136:0: R0914: Too many local variables (16/15) (too-many-locals)
app.py:181:0: R0914: Too many local variables (20/15) (too-many-locals)
app.py:390:0: R0914: Too many local variables (19/15) (too-many-locals)
pokemon.py:96:0: R0913: Too many arguments (8/5) (too-many-arguments)
pokemon.py:96:0: R0917: Too many positional arguments (8/5) (too-many-positional-arguments)
```

Kyseessä on kahdenlaisia tapauksia, jotka vaativat enemmän muuttujia:
* html-lomake ja haluttu logiikka on monimutkaisempi, jolloin kehityksessä on käytetty apumuuttujia pitämään prosessin askeleet luettavampina.
* html-lomake sisältää useampia kenttiä, mikä lähtökohtaisesti johtaa isompaan muuttujien määrään. Esimerkit alla:

```python
        name = request.form["name"]
        owner_id = session["user_id"]
        height = request.form["height"]
        weight = request.form["weight"]
        base_experience = request.form["base_experience"]
        next_evolution = request.form["next_evolution"]
        flavor_text = request.form["flavor_text"]
        sprite_url = request.form["sprite"]
        with urllib.request.urlopen(sprite_url) as response:
            sprite = response.read()
        stats = json.loads(request.form["stats"])
        is_base_stat = 1
        types = json.loads(request.form["types"])
```

```python
def add_pokemon(name, owner_id, height, weight, base_experience,
                next_evolution, flavor_text, sprite):

    sql = '''INSERT INTO pokemon (name, owner_id, height, weight, base_experience,
                                    next_evolution, flavor_text, sprite)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    db.execute(sql, [name, owner_id, height, weight, base_experience,
                     next_evolution, flavor_text, sprite])
```

Muutaman poikkeuksen takia kehittäjä ei ole nähnyt tarpeelliseksi lähteä muuttamaan tyyliään tai tekemään apufunktioita, jotta näissä tapauksissa muuttujien määrää saataisiin väkisin alas.

## Samanlaiset rivit eri tiedostoissa

Raportissa on seuraava ilmoitus liittyen koodin toistoon eri tiedostoissa:

```
users.py:1:0: R0801: Similar lines in 2 files
==pokemon:[47:54]
==users:[27:34]
    if query:
        sql += '''
            AND (pokemon.name LIKE ?
                    OR EXISTS ( SELECT 1
                                FROM pokemon_types
                                WHERE pokemon_types.pokemon_id = pokemon.id
                                AND pokemon_types.type LIKE ?))''' (duplicate-code)

```

Kyseessä on pieni osa pidempää dynaamista SQL-kyselyä, joka riippuu käyttäjän hakusanasta. Vaikka raportissa mainittu osa on identtinen, on koodi kokonaisuudessaan eri:
* `pokemon`-tiedostossa oleva koodi hakee listattuja pokémoneja kaikilta käyttäjiltä ja käyttää villikortti-syntaksia `hakusana%`
* `users`-tiedostossa oleva koodi hakee käyttäjän omia pokémoneja ja käyttää villikortti-syntaksia `%hakusana%`

Seuraavien syiden takia kehityksessä ei nähty tarvetta tehdä omaa moduulia välttämään näin pientä toisteisuutta:
* toisteisuudessa on kyse pienestä merkkijonon/SQL-kyselyn osasta
* `pokemon` ja `users` -moduulit, joissa tämä toisteisuus esiintyy vastaavat eri toiminnallisuuksista
* tälle logiikalle ei löydy globaalimpaa tarvetta


### Loput raportin sisällön varoituksista vastaavat esimerkkisovelluksen ja lähdemateriaalin mukaisia päätöksiä, joita noudatettiin myös tämän sovelluksen kehityksessä. Siksi sisältöä lainattu esimerkkisovelluksen raportista.

## Docstring-ilmoitukset

Suuri osa raportin ilmoituksista on docstring-kommentteihin liittyviä ilmoituksia:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei käytetä docstring-kommentteja.

## Vakion nimi

Raportissa on seuraava ilmoitus liittyen vakion nimeen:

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Tässä koodin päätasolla määritelty muuttuja tulkitaan vakioksi, jonka nimen tulisi olla kirjoitettu suurilla kirjaimilla. Sovelluksen kehittäjä haluaa tässä olla yhdenmukainen projektin inspiraationa toimivan esimerkkisovelluksen kanssa siinä, että muuttujan nimi on pienillä kirjaimilla. Kyseessä on myös erittäin pieni yksityiskohta, jota kehittäjä ei pidä relevanttina tällä kertaa. Muuttujaa käytetään koodissa näin:

```python
app.secret_key = config.secret_key
```

## Vaarallinen oletusarvo

Raportissa on seuraavat ilmoitukset liittyen vaaralliseen oletusarvoon:

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Esimerkiksi ensimmäinen ilmoitus koskee seuraavaa funktiota:

```python
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```

Tässä parametrin oletusarvo `[]` on tyhjä lista. Tässä ongelmaksi voisi tulla, että sama oletusarvona oleva tyhjä listaolio on jaettu kaikkien funktion kutsujen kesken ja jos jossain kutsussa listan sisältöä muutettaisiin, tämä muutos näkyisi myös muihin kutsuihin. Käytännössä tässä tapauksessa tämä ei kuitenkaan haittaa, koska koodi ei muuta listaoliota.
