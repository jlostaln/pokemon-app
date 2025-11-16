# Pokémon-sovellus

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen. ✅
* Käyttäjä pystyy keräämään, muokkaamaan ja poistamaan pokemoneja. ✅
* Käyttäjä pystyy tutkimaan maailmaa ja etsimään pokemoneja maailmasta. ✅
* Käyttäjä pystyy kehittämään keräämiään pokemoneja.
* Käyttäjä näkee sovelluksen muiden käyttäjien keräämät pokemonit.
* Käyttäjä pystyy etsimään pokemoneja hakusanalla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän keräämät pokemonit.
* Sovelluksessa on leaderboard, joka listaa käyttäjät ja lajittelee käyttäjät kerättyjen pokemonien perusteella.
* Käyttäjä pystyy valitsemaan maksimissaan 6 keräämistään pokemoneista, jotka kulkevat pelaajan mukana.
* Käyttäjä pystyy vaihtamaan pokemoneja toisen käyttäjän kanssa.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut:

```
$ sqlite3 database.db < schema.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```
