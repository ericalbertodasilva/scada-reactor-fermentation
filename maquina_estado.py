# coding: utf-8

import time
import sqlite3
from com_arduino import *
from datetime import datetime

while True:
    try:
        send_all_data()
        conn = sqlite3.connect("registro.db",timeout=10)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM dinamica WHERE id = 1;""")
        reg = cursor.fetchall()
        status = int(reg[0][1])
        conn.close
        if status == 2: # Estador ligar Bomba
            print(zerar_reator_1())
            cursor = conn.cursor()
            cursor.execute("""UPDATE dinamica SET status = 0 WHERE id = 1""")
            conn.commit()
        elif status == 3: # Estador ligar Bomba
            print(zerar_reator_2())
            cursor = conn.cursor()
            cursor.execute("""UPDATE dinamica SET status = 0 WHERE id = 1""")
            conn.commit()
        
    except:
        print("erro porta serial")
    time.sleep(10)