import os
import re
import psycopg2
import sys
import time
import _tkinter
import tkinter as tk
from tkinter import *
from tkinter import Menu
from tkinter import ttk
from tkinter.messagebox import showinfo


#
# Tkinter function
#
def init_tk():
    # root window
    global root
    root = tk.Tk()
    root.geometry('350x100')
    root.title('Init SNCF database')
    style = ttk.Style(root)
    style.theme_use('alt')

    root.grid()

    # action label
    global action_label
    action_label = ttk.Label(root, text='')
    action_label.grid(column=0, row=0, columnspan=2)

    # progressbar
    global pb
    pb = ttk.Progressbar(
        root,
        orient='horizontal',
        mode='determinate',
        length=300
    )
    # place the progressbar
    pb.grid(column=0, row=1, columnspan=2, padx=10, pady=20)

    # label
    global value_label
    value_label = ttk.Label(root, text=update_progress_label())
    value_label.grid(column=0, row=2, columnspan=2)
    root.update()


def update_progress_label():
    return f"{pb['value']}%"


def progress(val):
    pb['value'] = round(val, 0)
    value_label['text'] = update_progress_label()
    root.update()


def stop():
    pb.stop()
    value_label['text'] = update_progress_label()


#
# Database init funciton
#
def escape_db(string):
    string = "'" + re.sub(r'[\']', "''", string) + "'"
    return string


def db_query(sql, conn, cur):
    try:
        cur.execute(sql)
    except Exception as err:
        conn.rollback()
        print('Request : "'+str(sql)+'"' + '\nDatabase Sql error : ' + str(err))
        return 1
    conn.commit()


def create_tables(conn, cursor):
    action_label['text'] = f"Creating tables ..."
    root.update()
    sqls = []
    entries = os.listdir('./data_sncf/')
    for entry in entries:
        table = entry.split('.')[0]
        f = open('./data_sncf/'+entry, 'r')
        line = f.readline()
        line = re.sub(r'[\n]', ' ', line)
        columns = line.split(',')
        sql = 'CREATE TABLE ' + table + ' (rowid SERIAL PRIMARY KEY'
        for column in columns:
            sql += ', ' + column + ' VARCHAR(255)'
        sql += ");"
        sqls.append(sql)
        f.close()
    for sql in sqls:
        db_query(sql, conn, cursor)


def insert_data(conn, cursor):
    sqls = []
    entries = os.listdir('./data_sncf/')
    prog = re.compile('\"([^,\"]+,[^,\"]+)+\"')
    for entry in entries:
        table = entry.split('.')[0]
        f = open('./data_sncf/'+entry, 'r')
        lines = f.readlines()
        for i in range(len(lines)):
            line = re.sub(r'[\n]', ' ', lines[i])
            clean = prog.search(line)
            if clean:
                sub = re.sub(r'[,]', ' ', clean.group(0))
                line = re.sub(prog, sub, line)
            line = line.split(',')
            if i == 0:
                columns = ', '.join(line)
            else:
                sql = 'INSERT INTO ' + table + \
                    '(' + columns + ') VALUES (' + \
                      ', '.join(list(map(escape_db, list(line)))) + ');'
                sqls.append(sql)
        f.close()
    nb_insert = len(sqls)
    for i in range(nb_insert):
        val = (i / nb_insert) * 100
        progress(val)
        action_label['text'] = f"Inserted data: {i} / {nb_insert}"
        db_query(sqls[i], conn, cursor)
    action_label['text'] = str(nb_insert) + " successfully inserted lines"


def create_timetables(conn, cursor):
    action_label['text'] = f"Creating tables ..."
    root.update()
    sqls = []
    file = './data_sncf/timetables.csv'
    table = 'timetables'
    f = open(file, 'r')
    line = f.readline()
    line = re.sub(r'[\n]', ' ', line)
    columns = line.split('\t')
    sql = 'CREATE TABLE ' + table + ' (rowid SERIAL PRIMARY KEY'
    for column in columns:
        sql += ', ' + column + ' VARCHAR(255)'
    sql += ");"
    sqls.append(sql)
    f.close()
    for sql in sqls:
        db_query(sql, conn, cursor)


def insert_timetables(conn, cursor):
    sqls = []
    file = './data_sncf/timetables.csv'
    prog = re.compile('\"([^,\"]+,[^,\"]+)+\"')
    table = 'timetables'
    f = open(file, 'r')
    lines = f.readlines()
    for i in range(len(lines)):
        line = re.sub(r'[\n]', ' ', lines[i])
        clean = prog.search(line)
        if clean:
            sub = re.sub(r'[,]', ' ', clean.group(0))
            line = re.sub(prog, sub, line)
        line = line.split('\t')
        if i == 0:
            columns = ', '.join(line)
        else:
            sql = 'INSERT INTO ' + table + \
                '(' + columns + ') VALUES (' + \
                  ', '.join(list(map(escape_db, list(line)))) + ');'
            sqls.append(sql)
    f.close()
    nb_insert = len(sqls)
    for i in range(nb_insert):
        val = (i / nb_insert) * 100
        progress(val)
        action_label['text'] = f"Inserted data: {i} / {nb_insert}"
        db_query(sqls[i], conn, cursor)
    action_label['text'] = str(nb_insert) + " successfully inserted lines"


def create_stop_stop(conn, cursor):
    sql = 'CREATE TABLE stop_stop (rowid SERIAL PRIMARY KEY, stop_origin VARCHAR(255), stop_arrival VARCHAR(255), score VARCHAR(255))'
    cursor.execute(sql)
    sql = 'CREATE TABLE stop_stop_trip (rowid SERIAL PRIMARY KEY, fk_stop_stop INT, fk_trip VARCHAR(255))'
    cursor.execute(sql)
    conn.commit()
    sql = 'ALTER TABLE stop_stop_trip ADD COLUMN departure_time varchar(255), ADD COLUMN arrival_time varchar(255);'
    cursor.execute(sql)
    conn.commit()


if __name__ == '__main__':
    init_tk()
    errors = open('.log_error', 'w')
    sys.stdout = errors  # Change the standard output to the file we created.
    print('-*- Error Log File -*-')
    print(' ')

    conn = psycopg2.connect(
        host="localhost",
        database="sncf",
        user="postgres",
        password="postgres",
        port="5432")

    cursor = conn.cursor()

    create_tables(conn, cursor)
    insert_data(conn, cursor)
    create_timetables(conn, cursor)
    insert_timetables(conn, cursor)
    create_stop_stop(conn, cursor)

    cursor.close()
    conn.close()
    print("Success database initialization, connection close.")
    errors.close()
    exit(0)
