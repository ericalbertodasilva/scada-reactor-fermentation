from flask import render_template, jsonify, url_for
from app import app
from app.models import Medidas, Reator_fermentacao_1, Reator_fermentacao_2, Dinamica
import sqlite3
import time
import io
from datetime import *

@app.route('/')
def index():
    return render_template('monitorar.html')

@app.route('/_get_status', methods=['GET',])
def _get_status():
    conn = sqlite3.connect("registro.db",timeout=10)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM medidas WHERE id=(SELECT MAX(id) FROM medidas);""")
    status = cursor.fetchall()
    conn.close
    print(status)
    t = {}
    t.update({"temperatura":status[0][1]})
    t.update({"UR":status[0][2]})
    t.update({"co21":status[0][3]})
    t.update({"co22":status[0][4]})
    t.update({"data_registro":status[0][5]})
    return jsonify(t)

@app.route('/_get_status_reator1', methods=['GET',])
def _get_status_reator1():
    conn = sqlite3.connect("registro.db",timeout=10)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM reator_fermentacao_1 WHERE id=(SELECT MAX(id) FROM reator_fermentacao_1);""")
    status = cursor.fetchall()
    conn.close
    print(status)
    t = {}
    t.update({"co2":status[0][1]})
    t.update({"data_excel":status[0][2]})
    t.update({"art_estimado":status[0][3]})
    t.update({"etanol_estimado":status[0][4]})
    t.update({"data_registro":status[0][5]})
    return jsonify(t)

@app.route('/_get_status_reator2', methods=['GET',])
def _get_status_reator2():
    conn = sqlite3.connect("registro.db",timeout=10)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM reator_fermentacao_2 WHERE id=(SELECT MAX(id) FROM reator_fermentacao_2);""")
    status = cursor.fetchall()
    conn.close
    print(status)
    t = {}
    t.update({"co2":status[0][1]})
    t.update({"data_excel":status[0][2]})
    t.update({"art_estimado":status[0][3]})
    t.update({"etanol_estimado":status[0][4]})
    t.update({"data_registro":status[0][5]})
    return jsonify(t)

@app.route('/_get_grafico', methods=['GET',])
def _get_grafico():
    data_anterior = datetime.now() + timedelta(hours=-24)
    medidass = Medidas.query.filter(Medidas.data_registro >= data_anterior).all()
    j = ""
    for medi in medidass:
        j = j + str({'data_registro':str(medi.data_registro), 'temperatura':str(medi.temperatura), 'UR':str(medi.UR), 'reator_CO2_1':str(medi.reator_CO2_1), 'reator_CO2_2':str(medi.reator_CO2_2)})
    j = "["+ j.replace("}{","} , {").replace("'","\"") + "]"
    print(j)
    return j

@app.route('/_get_grafico_reator1', methods=['GET',])
def _get_grafico_reator1():
    data_anterior = datetime.now() + timedelta(hours=-24)
    Reator_fermentacao_1s = Reator_fermentacao_1.query.filter(Reator_fermentacao_1.data_registro >= data_anterior).all()
    j = ""
    for medi in Reator_fermentacao_1s:
        j = j + str({'data_registro':str(medi.data_registro), 'co2':str(medi.co2), 'art_estimado':str(medi.art_estimado), 'etanol_estimado':str(medi.etanol_estimado)})
    #print(j)
    return "["+ j.replace("}{","} , {").replace("'","\"") + "]"

@app.route('/_get_grafico_reator2', methods=['GET',])
def _get_grafico_reator2():
    data_anterior = datetime.now() + timedelta(hours=-24)
    Reator_fermentacao_2s = Reator_fermentacao_2.query.filter(Reator_fermentacao_2.data_registro >= data_anterior).all()
    j = ""
    for medi in Reator_fermentacao_2s:
        j = j + str({'data_registro':str(medi.data_registro), 'co2':str(medi.co2), 'art_estimado':str(medi.art_estimado), 'etanol_estimado':str(medi.etanol_estimado)})
    #print(j)
    return "["+ j.replace("}{","} , {").replace("'","\"") + "]"

@app.route('/_zerar_reator1', methods=['POST',])
def _zerar_reator1():
    conn = sqlite3.connect("registro.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("""UPDATE dinamica SET status = 2 WHERE id = 1""")
    conn.commit()
    conn.close()
    print("Reator 1 zerado")
    return jsonify({'Reator1':'zero'})

@app.route('/_zerar_reator2', methods=['POST',])
def _zerar_reator2():
    conn = sqlite3.connect("registro.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute("""UPDATE dinamica SET status = 3 WHERE id = 1""")
    conn.commit()
    conn.close()
    print("Reator 2 zerado")
    return jsonify({'Reator2':'zero'})