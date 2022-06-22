import requests
import bs4
import urllib
import os
import psycopg2


def makeBeautifulSoup(link):
    site = requests.get(link)
    return bs4.BeautifulSoup(site.text, 'html.parser')


def downSaveImg(imgLink, localLink):
    resource = urllib.request.urlopen(imgLink)
    output = open(localLink, "wb")
    output.write(resource.read())
    output.close()


def insertDataIntoDB(curs, tableName, dataList):
    try:
        curs.execute('''DELETE FROM "{0}"'''.format(tableName))
    except Exception:
        return ("We can't delete old date of {0}".format(tableName))

    for data in dataList[1:]:
        insertData = "{0}".format(data)
        try:
            curs.execute('''insert into "{0}" values({1});'''.format(tableName, insertData[1:-1]))
        except:
            pass
    return "We upload the data of {0}".format(tableName)

if __name__ == '__main__':
    ActorListVikings = [["name", "actor name", "description", "image"]]
    ActorListNorsemen = [["name", "actor name", "description", "image"]]
    ActorListNFL = [["name", "description", "image"]]

    ######################################################
    ######################################################
    # Scrape the Vikings site, and collect the description about every character, including the
    # actor playing them, including their photo.
    print("We are handling vikings cast...")
    vikingsSiteSoup = makeBeautifulSoup("https://www.history.com/shows/vikings/cast")
    castUl = vikingsSiteSoup.find_all("div", {"class": "tile-list tile-boxed"})
    castIl = castUl[0].find_all("li")

    for actor in castIl:
        # get name of character
        name = actor.find("strong").text

        # get name of actor
        actorName = actor.find("small").text[10:]

        # get description of actor
        descriptionActorSiteSoup = makeBeautifulSoup(
            "https://www.history.com/shows/vikings/cast/" + name.lower().replace(" ", "-"))
        descriptionActorSiteSoupMainArticle = descriptionActorSiteSoup.find_all('article')
        description = descriptionActorSiteSoupMainArticle[0].get_text()
        description = os.linesep.join([s for s in description.splitlines() if s])

        # get and save image of actor
        imageLink = actor.find("img")['src']
        imageLocalLink = "img\Vikings TV series\{0}.jpg".format(name.lower())
        downSaveImg(imageLink, imageLocalLink)

        ActorListVikings.append([name, actorName, description, imageLocalLink])
    print("done\n")

    ######################################################
    ######################################################
    # Scrape the Norsemen Wikipedia and/or IMDB sites, and collect the description about
    # as many characters as possible, including the actor playing them, including their photo.
    print("We are handling norsemen cast...")
    norsemenSiteSoup = makeBeautifulSoup("https://www.imdb.com/title/tt5905354/fullcredits/?ref_=tt_ql_cl")
    norsemenSiteSoupTable = norsemenSiteSoup.find_all("table")[2].find_all("tr")

    for tr in norsemenSiteSoupTable:
        try:
            tds = tr.find_all("td")
            name = tds[3].find_all("a")[0].text
            actorName = tds[1].text.split('\n', 1)[1].split('\n', 1)[0]
            description = tds[3].find_all("a")[1].text
            imageLink = tds[0].find("img")['src']
            imageLocalLink = "img\\Norsemen TV series\\{0}.jpg".format(actorName.lower())
            downSaveImg(imageLink, imageLocalLink)
            ActorListNorsemen.append([name, actorName, description, imageLocalLink])
        except:
            pass
    print("done\n")

    #######################################################
    #######################################################
    # Scrape the Vikings NFL team roster for information about every player, especially their
    # 2021 season overall statistics and biographies, and their photos.
    print("We are handling vikings NFL team...")
    NFLSiteSoup = makeBeautifulSoup("https://www.vikings.com/team/players-roster/")
    NFLSiteSoupTHTable = NFLSiteSoup.find_all("th")
    description = ""
    for i in range(1, len(NFLSiteSoupTHTable)):
        description += NFLSiteSoupTHTable[i].text + ":{" + str(i - 1) + "} "

    NFLSiteSoupTHTable = NFLSiteSoup.find_all("tbody")[0].find_all("tr")

    for tr in NFLSiteSoupTHTable:
        tds = tr.find_all("td")
        name = tds[0].text
        descriptionText = []
        for td in tds[1:]:
            descriptionText.append(td.text)
        description = description.format(*descriptionText)

        imageLink = tds[0].find("img")['src']
        imageLocalLink = "img\\Vikings NFL team\\{0}.jpg".format(name.lower())
        downSaveImg(imageLink, imageLocalLink)

        ActorListNFL.append([name, description, imageLocalLink])
    print("done\n")

    ######################################################
    ######################################################
    # indert data into DB
    print("We are saving the data to PostgreSQL DB...")

    user = input("Enter user name of PostgreSQL DB (default:'postgres'): ") or 'postgres'
    password = input("Enter password of PostgreSQL DB (default:'1234'): ") or '1234'
    port = input("Port (default:'5432'): ") or '5432'

    conn = psycopg2.connect(
        database="entreeCapitalHomeAssignment", user=user, password=password, host="localhost", port=port
    )

    conn.autocommit = True
    cursor = conn.cursor()
    print(insertDataIntoDB(cursor, "NorsemenTVseries", ActorListNorsemen))
    print(insertDataIntoDB(cursor, "VikingsTVseries", ActorListVikings))
    print(insertDataIntoDB(cursor, "VikingsNFLteam", ActorListNFL))
    conn.close()

    print("done\n")
    input("press Enter to exit")
