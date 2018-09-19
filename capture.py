#!/usr/bin/python
# CAPTURAR DADOS DOS STCP PARA PODER VER ONDE É QUE OS HORÁRIOS FALHAM
import os, sys
import importlib
stcp = importlib.import_module("stcp")
import time
import sqlite3
import datetime

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file, isolation_level=None)
        return conn
    except:
        print("ERROR CONNECTING TO DATABASE")
 
    return None

def insert_into_db(conn, linha, paragem, time):
    c = conn.cursor()
    c.execute("""
        INSERT INTO bus VALUES(NULL, '{0}', '{1}', '{2}');
    """.format(linha, paragem, time))

# Shift right to display in MB
def size(file_location):
    return os.path.getsize(file_location) >> 20

linhas = stcp.getLinhas()[0:4]
paragens = []

for linha in linhas:
    for ldir in range(0, 1):
        stops = stcp.getParagens(linha, ldir)
        #print(linha)
        for stop in stops:
            if stop not in paragens:
                paragens.append(stop)

#print(paragens[:-1])
#print(paragens)

conn = create_connection("capture.db")
size_of_db = size("./capture.db") 
print(len(paragens))
tempos = []
tempos_old = []
# size_of_db in MB
###
# TEMPO DE EXECUÇÃO DE UM CICLO: 4m:10s
###
while (size_of_db < 500):
    i = 0
    for stop in paragens:
        print(i)
        tempo = stcp.getTempos(stop)
        tempos.append(tempo)
        if tempo == []:
            pass
        else:
            if tempos_old != []:
                # PROBLEMA: AUTOCARROS PODEM TROCAR DE LUGAR
                if tempo[0][2] > tempos_old[i][0][2] or tempo[0][0] != tempos_old[i][0][0]:
                    # Autocarro passou
                    insert_into_db(conn, tempos_old[i][0][0], tempos_old[i][0][1], str(datetime.datetime.now()))
                    print("WORKS")
        i = i + 1
    tempos_old = tempos
    tempos = []