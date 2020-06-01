# coding: utf-8

from datetime import datetime
import time
import sqlite3
import serial

porta = serial.Serial("COM3",57600)

#co2 a 20 C 1,84 kg/m3 = 1,84 g/L = 0,00184 g/ml

conficiente_co2 = 0.00184
conficiente_medidor_gas1 = 72
conficiente_medidor_gas2 = 55
converter_co2_art= 2.0454
converter_co2_etanol= 1.0454

def excel_date(date1):
    temp = datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)

def teste_s():
    msg = b'<?>'
    porta.write(msg) # Escrever dados na porta serial
    resposta = porta.readline() # Receber dados na porta serial
    if (str(resposta) == "b'<?>\\r\\n'"):
        print("Serial OK")
    else:
        print("Serial sem resposta")
    return resposta

def send_all_data():
    conn = sqlite3.connect("registro.db",timeout=10)
    porta.write(b'<a>') # Escrever dados na porta serial
    resposta = str(porta.readline()) # Receber dados na porta serial
    resposta = list(resposta.replace("b'<a;","").replace(">\\r\\n'","").split(";"))
    # Conectar ao banco de dados
    cursor = conn.cursor()
    # inserir dados na tabela
    # <a;velocidade;temperatura;UR;reator1;reator2>
    cursor.execute("""INSERT INTO medidas (temperatura, UR, reator_CO2_1, reator_CO2_2, data_registro) VALUES (?, ?, ?, ?, ?)""", \
        (float(resposta[0]), float(resposta[1]), int(resposta[2])*conficiente_medidor_gas1, int(resposta[3])*conficiente_medidor_gas2, str(datetime.today())))
    conn.commit()

    cursor.execute("""SELECT * FROM medidas WHERE id=(SELECT MAX(id) FROM medidas);""")
    status = cursor.fetchall()
    volume_gas_reator1 = int(resposta[2])*conficiente_medidor_gas1
    massa_co2_reator1 = volume_gas_reator1*conficiente_co2
    volume_gas_reator2 = int(resposta[2])*conficiente_medidor_gas2
    massa_co2_reator2 = volume_gas_reator2*conficiente_co2

    if (float(status[0][2])!=volume_gas_reator1):
        cursor.execute("""INSERT INTO reator_fermentacao_1 (reator_CO2_1, art_estimado, etanol_estimado, data_excel, data_registro) VALUES (?, ?, ?, ?, ?)""", \
            (int(volume_gas_reator1), float(massa_co2_reator1*converter_co2_art), float(massa_co2_reator1*converter_co2_etanol), \
                float(excel_date(datetime.today())), str(datetime.today())))
        conn.commit()
    
    if (float(status[0][3])!=volume_gas_reator2):
        cursor.execute("""INSERT INTO reator_fermentacao_2 (reator_CO2_2, art_estimado, etanol_estimado, data_excel, data_registro) VALUES (?, ?, ?, ?, ?)""", \
            (int(volume_gas_reator2), float(massa_co2_reator2*converter_co2_art), float(massa_co2_reator2*converter_co2_etanol), \
                float(excel_date(datetime.today())), str(datetime.today())))
        conn.commit()
    
    conn.close
    print("Parametros gravados no banco de dados " + str(datetime.now()))
    return resposta

def zerar_reator_1():
    msg = b'<b>'
    porta.write(msg) # Escrever dados na porta serial
    resposta = porta.readline() # Receber dados na porta serial
    return resposta

def zerar_reator_2():
    msg = b'<c>'
    porta.write(msg) # Escrever dados na porta serial
    resposta = porta.readline() # Receber dados na porta serial
    return resposta

def teste():
    print(teste_s())
    print(send_all_data())
    #time.sleep(5)