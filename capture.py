#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # CAPTURAR DADOS DOS STCP PARA PODER VER ONDE É QUE OS HORÁRIOS FALHAM
import os, sys
import importlib
stcp = importlib.import_module("stcp")
import time
import sqlite3
import datetime
from multiprocessing import Process

def printf(string, file):
    f = open("log.txt", "a")
    f.write(string)

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
    conn.commit()
# Shift right to display in MB
def size(file_location):
    return os.path.getsize(file_location) >> 20

conn = create_connection("capture.db")
size_of_db = size("./capture.db") 

###
# TEMPO DE EXECUÇÃO DE UM CICLO: 4m:10s
###
linhas = stcp.getLinhas()
paragens = []
for linha in linhas:
    for ldir in range(0, 1):
        stops = stcp.getParagens(linha, ldir)
        #print(linha)
        for stop in stops:
            if stop not in paragens:
                paragens.append(stop)

def autocarro_passou(stops1):
    tempos = []
    tempos_old = []
    while (size_of_db < 500):
        i = 0
        for stop in stops1:
            tempo = None
            while tempo is None:
                try:
                    tempo = stcp.getTempos(stop)
                except:
                    pass

            tempos.append(tempo)
            #print(tempo)
            #print(stop)
            if tempos_old != []:
                tempo_old = tempos_old[i]
                linhas = []
                for j in range(0, len(tempo)):
                    linhas.append(tempo[j][0])
                for j in range(0, len(tempo_old)):
                    flag = 1
                    if tempo_old[j][2] >= 7:
                        continue
                    for k in range(0, len(tempo)):
                        if tempo_old[j][0] == tempo[k][0] and tempo_old[j][2] >= tempo[k][2]-2:
                            flag = 0
                    if flag != 0:
                        insert_into_db(conn, tempo_old[j][0], stop[0], str(datetime.datetime.now().replace(microsecond=0)))

            i = i + 1
        tempos_old = tempos
        tempos = []

if __name__ == '__main__':
    array1 = paragens[0:int(len(paragens)/4)]
    array2 = paragens[int(len(paragens)/4):int(len(paragens)/2)]
    array3 = paragens[int(len(paragens)/2):int(len(paragens)/4+len(paragens)/2)]
    array4 = paragens[int(len(paragens)/4+len(paragens)/2):len(paragens)]
    p1 = Process(target=autocarro_passou, args=(array1, ))
    p2 = Process(target=autocarro_passou, args=(array2,))
    p3 = Process(target=autocarro_passou, args=(array3,))
    p4 = Process(target=autocarro_passou, args=(array4,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()