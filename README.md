# Kansalaisaloite 2.0
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Kirjautuneet käyttäjät pystyvät luomaan kansalaisaloitteita. Aloitteella on sekä nimi että kuvaus.
  * Lisäämällä kuvaukseen sanan alkuun "#", voidaan aloitteelle luoda vapaita luokitteluja (joita tullaan hyödyntämään ohjelman tulevissa versioissa)
* Kirjautuneet käyttäjät voivat myös äänestää aloitteiden puolesta ja kommentoida niitä.
  * Kommentteja voi muokata ja poistaa.
  * Klikkaamalla kommentin tehnyttä käyttäjää käyttäjäsivuille, josta löytyvät muut käyttäjän kommentit 
* Käyttäjä näkee sovellukseen lisätyt aloitteet etusivulla ja pystyy myös etsimään niitä hakusaalla.


## Testaaminen:
* Sovelluksen testaaminen Windows-käyttöjärjestelmällä edellyttää, että Python, Pythonin Flask kirjasto sekä STQlite ovat asennettuina.
* Sovelluksessa tulee mukana tietokantaskeema, jonka mukaisen kannan saa pystytettyä Powershelissä komennolla  _cat schema.sql | sqlite3 database.db_
* Kun kanta on pystyssä saa ohjelman käyntiin komennolla flask.run
* Ohjelman käyttöliittymään pääsee käsiksi osoitteessa http://127.0.0.1:5000/
