#!/usr/bin/python
# CAPTURAR DADOS DOS STCP PARA PODER VER ONDE É QUE OS HORÁRIOS FALHAM
import os, sys
import importlib
importlib.import_module("stcp")
import time
import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
    
# Shift right to display in MB
def size(file_location):
    return os.path.getsize(file_location) >> 20

db = create_connection("capture.db")
size_of_db = size("./capture.db") 

linhas = stcp.getLinhas()
for linha in linhas:
        paragens.append 

while (size_of_db < 500):
    
