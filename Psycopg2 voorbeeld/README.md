# Van Python naar PostgreSQL met Psycopg2, een stap-voor-stap tutorial!

## Inhoudsopgave

1. [Introductie](#introductie)
2. [Stap 1: Psycopg2 installeren](#stap-1-psycopg2-installeren)
3. [Stap 2: Verbinden met de database](#stap-2-verbinden-met-de-database)
4. [Stap 3: Query uitvoeren](#stap-3-query-uitvoeren)
5. [Stap 4: Resultaten ophalen](#stap-4-resultaten-ophalen)
6. [Stap 5: Verbinding sluiten](#stap-5-verbinding-sluiten)
7. [Best practices](#best-practices)
8. [Voorbeeld](#voorbeeld)
9. [Resources](#resources)


## Introductie
In deze tutorial gaan we aan de slag met de Psycopg2 library in Python. Psycopg2 is een library die het mogelijk maakt om te communiceren met een PostgreSQL database. We gaan een Python script schrijven dat een connectie maakt met een PostgreSQL database en een query uitvoert.


## Stap 1: Psycopg2 installeren

Om Psycopg2 te installeren kan je de volgende commando uitvoeren in je terminal:

```commandline
pip install psycopg2
```

Of door in PyCharm naar Python Packages te gaan (onder de console) en daar psycopg2 te zoeken en te installeren.

Als je Psycopg2 al geïnstalleerd hebt, dan kan je deze stap gewoon overslaan.

## Stap 2: Verbinden met de database

Om te verbinden met een PostgreSQL database kan je de volgende code gebruiken: 

```python
import psycopg2 as pg
connection = pg.connect("host=Vamos user=a password=la dbname=playa") # Vervang hier "Vamos a la playa met jouw eigen connection string"
```
We hebben nu verbinding gemaakt met de database! De connection string is een string die de informatie bevat die nodig is om te verbinden met de database. Deze string bevat de naam van de database, de gebruikersnaam en het wachtwoord.

## Stap 3: Query uitvoeren
Voor een query heb je een cursor nodig, die je kan aanmaken met de volgende code:
```python
cursor = connection.cursor()
```

Nu hebben we een cursor, met de cursor kunnen we queries uitvoeren. Bijvoorbeeld:
```python
cursor.execute("SELECT lyrics FROM songs WHERE songname = 'L\'amour Toujours'") # I still believe in your eyes... 
```

Hiermee voer je de query uit die je tussen de aanhalingstekens hebt gezet. In dit geval is dat een simpele `SELECT` query die de lyrics van het liedje "L'amour Toujours" ophaalt.

Als je een query hebt die parameters nodig heeft, kan je deze ook meegeven in de `execute` functie. Bijvoorbeeld:
```python
cursor.execute("INSERT into songs (artist, songname, lyrics) VALUES (%s, %s, %s)", ("Mary Hopkin", "Those Were The Days", "Once upon a time there was a tavern...")) # Insert een nieuw liedje in de database
```

Hiermee voer je een `INSERT` query uit die een nieuw liedje toevoegt aan de database. De `%s` in de query zijn placeholders voor de waarden die je meegeeft in de tweede parameter van de `execute` functie.

Als je iets toevoegt aan jouw database, is het nodig om de verbinding te committen met de volgende code, zodat de veranderingen ook echt worden doorgevoerd in de database:

```python 
connection.commit()
```

## Stap 4: Resultaten ophalen
Als je een select query hebt uitgevoerd, dan kan je de resultaten ophalen met fetchall, fetchone of fetchmany.

- Fetchall: Haalt alle resultaten op
- Fetchone: Haalt één resultaat op
- Fetchmany: Haalt een bepaald aantal resultaten op (dit aantal geef je mee als parameter)
Nu heb je de resultaten van de query in de variabele `result`.
```python
result = cursor.fetchall()
```
Gebruik fetchone als je maar één resultaat verwacht:
```python
result = cursor.fetchone()
```

Gebruik fetchmany als je een bepaald aantal resultaten wilt ophalen:
```python
result = cursor.fetchmany(5) # Haal 5 resultaten op
```

Als ik nu bijvoorbeeld alle liedjes van The Beatles op wil halen, dan doe ik het volgende:
```python
cursor.execute("SELECT song FROM songs WHERE artist = 'The Beatles'")
result = cursor.fetchall()
for song in result:
    print(song[0]) # Print alleen de songname
```
## Stap 5: Verbinding sluiten
Als je klaar bent met de database kan je de verbinding sluiten door de close functie te gebruiken op jouw connection en cursor objecten:

```python
cursor.close()
connection.close()
```
Hiermee sluit je de verbinding met jouw database, en dan ben je klaar!

## Best practices
Voor dit project is het nog niet erg als je de connection string in je code zet, maar in een productieomgeving is dit onveilig, zeker als je een publieke repository hebt.

Het is beter om de connection string in een apart bestand (zoals een .env bestand, let op om deze **niet** te committen naar GitHub!) te zetten en deze in te laden in je code.

Om deze environment variabelen in te laden kan je gebruikmaken van de os en de dotenv libraries in Python.

Dat ziet er dan ongeveer zo uit:
```python
import psycopg2 as pg
import os
import dotenv

dotenv.load_dotenv()

connection_string = os.getenv("CONNECTION_STRING") # Dit is een voorbeeld van hoe je de connection string kan ophalen uit een .env bestand, je kan de string zo noemen als je wilt.

connection = pg.connect(connection_string)
```
Hierna kan je de eerdere stappen zoals hierboven beschreven uitvoeren. 


Daarnaast is het ook handig om een try-except block te gebruiken om fouten op te vangen, zodat je code niet meteen crasht!

```python
try: 
    connection = pg.connect(connection_string)
    cursor = connection.cursor()
except Exception as e:
    print("Er is iets fout gegaan bij het verbinden met de database!")
    print("De volledige error is: ")
    print(e)
    exit()
```

Als je een klein voorbeeldje van zo'n .env bestand wil zien, kijk naar het .env example in deze folder (lekker hypocriet, maar dit is een voorbeeldje, dus het is niet erg).

Je kan in een .env bijvoorbeeld ook API keys of andere gevoelige informatie opslaan, zodat je deze niet in je code hoeft te zetten.

In dit geval heb je een CONNECTION_STRING, met de variabelen host, user, password en dbname. Deze kan je dan inladen in je code zoals hierboven beschreven, wel is het handig om **je eigen** variabelen in te vullen voor deze variabelen.


## Voorbeeld

In de folder van deze tutorial staat een voorbeeld van hoe je Psycopg2 kan gebruiken om te verbinden met een database en een aantal queries uit te voeren, en (indien je iets opzoekt) de resultaten op te halen en te printen.

Dit met een database voor een muziekcollectie, waarin je liedjes kan toevoegen, verwijderen en opvragen.

Als je wil verbinden met je eigen database, verander dan de connection string in het .env bestand naar jouw eigen wachtwoord, gebruikersnaam, database en host (in mijn geval is dit localhost, maar dit kan ook het IP adres van jouw Azure server zijn!).

Ik raad aan om een nieuwe database aan te maken voor dit voorbeeld (in het voorbeeld heet deze songs, maar je kan deze noemen wat je wil, zolang deze maar bestaat!).


## Resources: 

- [Psycopg2 documentatie](https://www.psycopg.org/docs/)
- [GeeksforGeeks tutorial .env bestanden](https://www.geeksforgeeks.org/python-environment-variables/)
- [Python documentation os library](https://docs.python.org/3/library/os.html)
- [Python documentation dotenv library](https://pypi.org/project/python-dotenv/)
