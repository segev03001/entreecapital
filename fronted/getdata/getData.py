import psycopg2


def insertDataIntoDB(tableName):
    conn = psycopg2.connect(
        database="entreeCapitalHomeAssignment", user='postgres', password='s2512160', host="localhost", port='5433'
    )
    conn.autocommit = True
    curs = conn.cursor()

    try:
         data = curs.execute('''SELECT * FROM "{0}"'''.format(tableName))
    except Exception as e:
        return e

    conn.close()
    return data
