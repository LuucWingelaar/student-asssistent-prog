import psycopg2 as pg
import dotenv
import os

from requests import delete

# Laad de variabelen uit het .env bestand
dotenv.load_dotenv()

# Haal de connection string uit de .env file
connectionString = os.getenv("CONNECTION_STRING")


def createTable():
    """!
    @brief: Maak een tabel aan in de database als deze nog niet bestaat
    @return: None
    """
    cursor.execute("CREATE TABLE IF NOT EXISTS songs (song VARCHAR(255), artist VARCHAR(255), lyrics TEXT, releaseYear INT)")
    connection.commit()

def deleteSong(song):
    """!
    @brief: Verwijder een liedje uit de database op basis van de gegeven parameters in het hoofdmenu
    @param song: De naam van het liedje dat verwijderd moet worden
    @return: bool, True als het liedje succesvol is verwijderd, anders False
    """
    try:
        cursor.execute("DELETE FROM songs WHERE song = %s", (song,))
        connection.commit()
        print(f"Het liedje {song} is succesvol verwijderd!")
        return True
    except:
        print(f"Het liedje {song} kon niet verwijderd worden, verifieer of het liedje in de database staat!")
        return False


def getAllSongs():
    """!
    @brief: Verkrijg alle nummers in de database
    @return: None
    """
    cursor.execute("SELECT song FROM songs")
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Er zijn geen nummers gevonden!")
        return # Als er geen nummers gevonden zijn, stop de functie
    else:
        print(f"{'-' * 50}")
        print("Alle nummers in de database:")
        for row in rows:
            print(f"{row[0]}") # print de namen van de nummers in de database
        print(f"{'-' * 50}")
        return

def getSongs(artist):
    """!
    @brief: Verkrijg alle nummers van een gegeven artiest
    @param artist: De naam van de artiest waarvan je de nummers wilt verkrijgen
    @return: None
    """
    cursor.execute("SELECT song FROM songs WHERE artist = %s", (artist,))
    rows = cursor.fetchall()
    print(f"{'-' * 50}")
    if len(rows) == 0:
        print("Er zijn geen nummers gevonden van deze artiest!")
        return
    else:
        print(f"Alle nummers van {artist}:")
        for row in rows:
            print(f"{row[0]}") # print de namen van de nummers van de gegeven artiest
    print(f"{'-' * 50}")


def getReleaseYear():
    """!
    @brief: Verkrijg het jaar van uitgave van een gegeven liedje
    @param: None
    @return: releaseYear, het jaar van uitgave van het liedje. Als er geen jaar van uitgave is, return 0
    @note: Deze functie is ervoor om te voorkomen dat er ValueErrors optreden als de gebruiker geen cijfer invoert en om te voorkomen dat we nummers hebben van meer dan 2000 jaar geleden in de database
    """
    while True:
        user_input = input("Wat is het release jaar van het liedje?, druk op enter als je het niet weet: ")
        if user_input == "":
            return 0 # Om een leeg veld in de database te voorkomen, return 0 als er geen release jaar is
        try:
            releaseYear = int(user_input)
            if releaseYear < 0:
                print("Dat is knap, een liedje dat voor Christus is uitgebracht!")
                continue
            return releaseYear
        except ValueError:
            print("Het jaar van uitgave moet een getal zijn!")
            continue


def getSongInformation(song):
    """!
    @brief: Verkrijg informatie over een gegeven liedje
    @param song: De naam van het liedje waarvan je informatie wilt verkrijgen
    @return: None
    """
    cursor.execute("SELECT * FROM songs WHERE song = %s", (song,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        return False # Als er geen nummers gevonden zijn, return False
    else:
        # Print alle informatie over het liedje
        for row in rows:
            print(f"{'-' * 50}")
            print(f"Naam: {row[0]}")
            print(f"Artiest: {row[1]}")
            print(f"Lyrics: {row[2]}")
            print(f"Jaar van uitgave: {row[3]}")
            print(f"{'-' * 50}")
        return True

def newSong(song, artist, lyrics = "", releaseYear = 0):
    """!
    @brief: Voeg een nieuw liedje toe aan de database op basis van de gegeven parameters in het hoofdmenu
    @param song: De naam van het liedje, mag niet leeg zijn
    @param artist: De naam van de artiest, mag niet leeg zijn
    @param lyrics: De lyrics van het liedje, optioneel default is een string om een leeg veld in de database te voorkomen
    @param releaseYear: Het jaar waarin het liedje is uitgebracht, optioneel, default is 0 om een leeg veld in de database te voorkomen
    @return: bool, True als het liedje succesvol is toegevoegd, anders False
    """
    # Voeg het nummer toe aan de database, %s is een placeholder voor de waarde die we willen invoegen
    if song == "" or artist == "":
        print("Het liedje of de artiest mag niet leeg zijn!")
        return False
    cursor.execute("INSERT INTO songs (song, artist, lyrics, releaseYear) VALUES (%s, %s, %s, %s)", (song, artist, lyrics, releaseYear))
    connection.commit()
    return True


def main_menu():
    """!
    @brief: Hoofdmenu van de applicatie
    @return: None
    """
    print(f"{'-' * 50}\nWelkom bij de muziek database! \nMaak een keuze uit de volgende opties:")
    while True:
        keuze = input(f"1. Zoek nummers van een artiest\n2. Voeg een nieuw liedje toe\n3. Zoek informatie over een liedje\n4. Bekijk alle nummers\n5. Verwijder een liedje uit de database\n6. Stop\nJouw keuze: ")
        if keuze == "1":
            artiest = input("Wat is de naam van de artiest? ")
            getSongs(artiest)
        elif keuze == "2":
            song = input("Wat is de naam van het liedje? ")
            artist = input("Wat is de naam van de artiest? ")
            lyrics = input("Wat zijn de lyrics van het liedje? (optioneel) ")
            releaseYear = getReleaseYear()
            if newSong(song, artist, lyrics, releaseYear):
                print("Het liedje is succesvol toegevoegd!")
            else:
                print("Het liedje kon niet toegevoegd worden aan de database!")
        elif keuze == "3":
            song = input("Wat is de naam van het liedje? ")
            if not getSongInformation(song):
                print("Het liedje kon niet gevonden worden in de database!")
        elif keuze == "4":
            getAllSongs()
        elif keuze == "5":
            song = input("Wat is de naam van het liedje dat je wilt verwijderen? ")
            deleteSong(song)
        elif keuze == "6":
            break
        else:
            print("Ongeldige keuze, probeer het opnieuw!")


try:
    connection = pg.connect(connectionString)
    cursor = connection.cursor()
    createTable()
except Exception as e:
    print("Kon niet verbinden met de database!")
    print(e)
    exit()

main_menu()
