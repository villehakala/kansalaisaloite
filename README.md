# Kansalaisaloite 2.0
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Kirjautuneet käyttäjät pystyvät luomaan kansalaisaloitteita. Aloitteella on sekä nimi että kuvaus.
  * Aloitteelle voi valita luokittelun valmiista luokista tai lisätä vapaavalintaisen luokittelun laittamalla minkä vaan kuvauksen sanan alkuun "#".
* Kirjautuneet käyttäjät voivat myös antaa äänensä aloitteelle ja kommentoida niitä.
  * Kommentteja voi muokata ja poistaa.
  * Klikkaamalla kommentin tehnyttä käyttäjää käyttäjäsivuille, josta löytyvät käyttäjän aloitteet ja kommentit
* Käyttäjä näkee sovellukseen lisätyt aloitteet etusivulla ja pystyy myös etsimään niitä hakusanalla.


## Testaaminen:

Asenna flask-kirjasto, jos tätä ei ole jo asennettu

$ pip install flask

Luo tietokannan taulut

$ sqlite3 database.db < schema.sql

Käynnistä sovellus

$ flask run.
