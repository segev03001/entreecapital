import psycopg2
from flask import Flask
from flask import request
from flask import render_template


app = Flask(__name__)



@app.route('/', methods=['GET'])
def index(name=None, tableName='NorsemenTVseries'):
    if request.method == 'GET':
        conn = psycopg2.connect(database="entreeCapitalHomeAssignment", user='postgres', password='s2512160', host="localhost", port='5433')
        conn.autocommit = True
        cursor = conn.cursor()
        sql = '''SELECT * FROM  "NorsemenTVseries";''';

        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
        except Exception as e:
            print(e.args[0])
        conn.close()
        # return result
    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run()
