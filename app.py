from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Retornar dados da tabela em json
@app.route('/')
@app.route("/lista", methods=["GET"])
def listar():
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    connection = sqlite3.connect('banco.db')
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    sql = "SELECT * FROM tb_music_book"
    cursor.execute(sql)
    result = json.dumps(cursor.fetchall())
    return result


app.run(debug=True)

