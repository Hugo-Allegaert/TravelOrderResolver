import os
import re
from numpy import timedelta64
import psycopg2
import sys
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from datetime import datetime
from datetime import timedelta


class Node():
    def __init__(self, x, y, distance):
        self.x = [x[0], y[0]]
        self.y = [x[1], y[1]]
        self.distance = str(distance)


#
# Sql function
#
def get_all_stops():
    sql = "SELECT distinct stop_id FROM stops WHERE stop_id like '%Train%';"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def exec_query(sql):
    try:
        cursor.execute(sql)
    except Exception as err:
        conn.rollback()
        print('Request : "'+str(sql)+'"' + '\nDatabase Sql error : ' + str(err))
        return 1
    conn.commit()


def get_all_linked_stops():
    sql = "SELECT stop_lon, stop_lat, stop_name FROM stops WHERE parent_station = ' ';"


def draw_graph(graphs):
    #graphs = [Node([1, 3], [3, 3], 2), Node([3, 2], [10, 10], 1)]
    for n in graphs:
        print(n.x, n.y)
        plt.plot(n.x, n.y, 'ro-')
        plt.text(n.x[1], n.y[1], n.distance,
                 fontsize=9, fontname="Helvetica", weight="bold")
    plt.show()


def get_next_stop(stop_id):
    FMT = '%H:%M:%S'
    nodes = []
    sql = "select distinct trip_id, departure_time from stop_times st where stop_id = '{stop_id}';".format(
        stop_id=stop_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    ids = []
    for trip in res:
        sql = "select st.stop_id, st.arrival_time, s.stop_name, s.stop_lon, s.stop_lat from stop_times st left join stops s on s.stop_id = st.stop_id where st.trip_id = '" + \
            trip[0]+"' and st.arrival_time > '"+trip[1]+"' limit 1;"
        time_depart = trip[1]
        if time_depart.find('24:') == 0:
            time_depart = time_depart.replace('24:', '00:', 1)
        cursor.execute(sql)
        stop = cursor.fetchall()
        if (stop):
            stop = stop[0]
            if (stop[0] not in ids):
                time_arrival = stop[1]
                if time_arrival.find('24:') == 0:
                    time_arrival = time_arrival.replace('24:', '00:', 1)
                tdelta = datetime.strptime(
                    time_arrival, FMT) - datetime.strptime(time_depart, FMT)
                if tdelta.days < 0:
                    tdelta = timedelta(
                        days=0, seconds=tdelta.seconds, microseconds=tdelta.microseconds)
                tdelta = tdelta.seconds / 60
                sql = "insert into stop_stop (stop_origin, stop_arrival, score) values ('"+str(
                    stop_id)+"', '"+str(stop[0])+"', '"+str(tdelta)+"')"
                exec_query(sql)
            sql = "insert into stop_stop_trip (fk_stop_stop, fk_trip) values ((select rowid from stop_stop ss where ss.stop_origin = '{so}' and ss.stop_arrival = '{sa}'), '{trip_id}')".format(
                so=stop_id, sa=stop[0], trip_id=trip[0])
            exec_query(sql)
            ids.append(stop[0])

    return nodes


def arrival_departure_time():
    sql = "select sst.rowid, sst.fk_trip, ss.stop_origin, ss.stop_arrival from stop_stop_trip sst left join stop_stop ss on ss.rowid = sst.fk_stop_stop;"
    cursor.execute(sql)
    resql = cursor.fetchall()
    for res in resql:
        sql = "UPDATE stop_stop_trip set departure_time = (select st.departure_time from stop_times st where trip_id = '{t}' and stop_id = '{s_o}'), arrival_time = (select st.departure_time from stop_times st where trip_id = '{t}' and stop_id = '{s_a}') where rowid = {id}".format(
            t=res[1], s_o=res[2], s_a=res[3], id=res[0])
        exec_query(sql)


if __name__ == '__main__':
    global conn, cursor

    conn = psycopg2.connect(
        host="localhost",
        database="sncf",
        user="postgres",
        password="postgres",
        port="5432")

    cursor = conn.cursor()
    # arrival_departure_time()
    # exit(0)
    stops = get_all_stops()
    i = 0
    nb = len(stops)
    for id in stops:
        print("{i} / {nb}".format(i=i, nb=nb), end='\r')
        get_next_stop(id[0])
        i += 1
    print('DONE            ')
    exit(0)
