import psycopg2


def createDB(curs):
    # Preparing query to create a database
    sql = '''CREATE DATABASE "entreeCapitalHomeAssignment"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Hebrew_Israel.1255'
    LC_CTYPE = 'Hebrew_Israel.1255'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;''';

    # Creating a database
    try:
        curs.execute(sql)
        return "Database created successfully"
    except Exception as e:
        return e.args[0]


def createTables(curs):
    # Doping tables if already exists.
    curs.execute('''DROP TABLE IF EXISTS "NorsemenTVseries"''')
    curs.execute('''DROP TABLE IF EXISTS "VikingsNFLteam"''')
    curs.execute('''DROP TABLE IF EXISTS "VikingsTVseries"''')

    # Creating table as per requirement
    NorsemenTVseriesTable = '''CREATE TABLE public."NorsemenTVseries"
    (
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    "actorName" character varying(30) COLLATE pg_catalog."default",
    description character varying(5000) COLLATE pg_catalog."default",
    "imagePath" character varying(150) COLLATE pg_catalog."default"
    )

    TABLESPACE pg_default;

    ALTER TABLE public."NorsemenTVseries"
    OWNER to postgres;'''

    VikingsNFLteamTable = '''CREATE TABLE public."VikingsNFLteam"
    (
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    description character varying(5000) COLLATE pg_catalog."default",
    "imagePath" character varying(150) COLLATE pg_catalog."default"
    )

    TABLESPACE pg_default;

    ALTER TABLE public."VikingsNFLteam"
    OWNER to postgres;'''

    VikingsTVseriesTable = '''CREATE TABLE public."VikingsTVseries"
    (
    name character varying(30) COLLATE pg_catalog."default" NOT NULL,
    "actorName" character varying(30) COLLATE pg_catalog."default",
    description character varying(5000) COLLATE pg_catalog."default",
    "imagePath" character varying(150) COLLATE pg_catalog."default"
    )

    TABLESPACE pg_default;

    ALTER TABLE public."VikingsTVseries"
    OWNER to postgres;'''

    try:
        curs.execute(NorsemenTVseriesTable)
        print("NorsemenTVseriesTable created successfully")
    except Exception as e:
        print(e.args[0])

    try:
        curs.execute(VikingsNFLteamTable)
        print("VikingsNFLteamTable created successfully")
    except Exception as e:
        print
        print(e.args[0])

    try:
        curs.execute(VikingsTVseriesTable)
        print("VikingsTVseriesTable created successfully")
    except Exception as e:
        print
        print(e.args[0])


if __name__ == '__main__':
    print("Script for creating PostgreSQL DB and tables.")
    user = input("Enter user name of PostgreSQL DB (default:'postgres'): ") or 'postgres'
    password = input("Enter password of PostgreSQL DB (default:'1234'): ") or '1234'
    port = input("Port (default:'5432'): ") or '5432'

    conn = psycopg2.connect(
        database="postgres", user=user, password=password, host="localhost", port=port
    )
    # conn = psycopg2.connect(
    #     database="postgres", user='postgres', password='s2512160', host="localhost", port='5433'
    # )
    conn.autocommit = True
    cursor = conn.cursor()
    print(createDB(cursor))
    conn.close()

    conn = psycopg2.connect(
        database="entreeCapitalHomeAssignment", user='postgres', password='s2512160', host="localhost", port='5433'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    createTables(cursor)
    conn.close()

    file = open("postgres.txt", "r+")
    contents = file.read().split("\n")
    file.seek(0)  # <- This is the missing piece
    file.truncate()
    file.write("{user=" + user + ", password=" + password + ", port=" + port + "}")
    file.close()
    input("press Enter to exit")
