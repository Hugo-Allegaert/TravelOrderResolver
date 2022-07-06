import os
import re
from numpy import Infinity, empty, timedelta64
import numpy as np
import psycopg2
import sys
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from datetime import datetime
from datetime import timedelta
import math
import time


global conn, cursor

conn = psycopg2.connect(
    host="postgres",
    database="travel",
    user="postgres",
    password="postgres",
    port="5432")
cursor = conn.cursor()


class Node():
    def __init__(self, id, dist, pred, lon='', lat='', name=''):
        self.id = id
        self.dist = dist
        self.pred = pred
        self.lon = lon
        self.lat = lat
        self.name = name

    def set_min_dist(self, dist, pred):
        self.dist = dist
        self.pred = pred


class Trip():
    def __init__(self, start_id, end_id, trips):
        self.start_id = start_id
        self.end_id = end_id
        self.start_name = get_stop_name(start_id)
        self.start_lat, self.start_lon = get_stop_lat_lon(start_id)
        self.end_name = get_stop_name(end_id)
        self.end_lat, self.end_lon = get_stop_lat_lon(end_id)
        err = 1
        while (err == 1):
            err = 0
            for i in range(len(trips)):
                if trips[i]['departure_time'] > trips[i]['arrival_time']:
                    del(trips[i])
                    err = 1
                    break

        self.trips = trips


#
# Output
#


def draw_map(route):
    stops = get_all_stops()
    x = []
    y = []
    for data in stops:
        if float(data[2]) > float(20):
            x.append(float(data[1]))
            y.append(float(data[2]))

    for i in range(len(route)):
        if i + 1 < len(route):
            next_lon = float(route[i+1].lon)
            next_lat = float(route[i+1].lat)
        plt.plot([float(route[i].lon), next_lon], [
                 float(route[i].lat),  next_lat], '-k', lw=2)
        plt.plot(float(route[i].lon), float(route[i].lat), 'hr')
        plt.text(float(route[i].lon), float(route[i].lat), route[i].name,
                 fontsize=9, fontname="Helvetica", weight="bold")
    plt.scatter(x, y)
    plt.show()


def format_date(date):
    return ('{Y}-{M}-{D}'.format(Y=date[:4], M=date[4:6], D=date[6:]))

#
# Sql function
#


def get_all_stops():
    sql = "SELECT distinct stop_id, stop_lon, stop_lat, stop_name FROM stops WHERE stop_id like '%Train%';"
    # with date :
    # sql = "select distinct st.stop_id, s.stop_lon, s.stop_lat, s.stop_name from stop_times st left join trips t on t.trip_id = st.trip_id left join calendar c on t.service_id = c.service_id left join stops s on st.stop_id = s.stop_id where st.stop_id like '%Train%' and c.monday = '1' and c.start_date <= '20200302' and c.end_date >= '20200302';"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def get_stop_name(stop_id):
    sql = "select stop_name from stops where stop_id='{id}'".format(id=stop_id)
    cursor.execute(sql)
    res = cursor.fetchone()
    if res != None:
        return res[0].replace('"', '')
    return ''


def get_linked_stop(stop_id):
    sql = "SELECT stop_arrival, score FROM stop_stop WHERE stop_origin = '{id}'".format(
        id=stop_id)
    # with date :
    # sql = "SELECT stop_arrival, score FROM stop_stop ss left join stop_stop_trip sst on sst.fk_stop_stop = ss.rowid left join trips t on t.trip_id = sst.fk_trip left join calendar c on t.service_id = c.service_id WHERE stop_origin = '{id}' and c.monday = '1' and c.start_date <= '20200302' and c.end_date >= '20200302'".format(
    #    id=stop_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def get_stop_lat_lon(stop_id):
    sql = "select stop_lat, stop_lon from stops where stop_id='{id}'".format(
        id=stop_id)
    cursor.execute(sql)
    res = cursor.fetchone()
    if res != None:
        return res[0], res[1]
    return 0, 0


def get_stop_info(stop_name):
    sql = "select stop_id, stop_name, stop_lat, stop_lon from stops s where LOWER(stop_name) like '%{name}%' and stop_id like '%Train%' limit 1".format(
        name=stop_name)
    cursor.execute(sql)
    res = cursor.fetchone()
    return {'stop_id': res[0], 'stop_name': res[1], 'stop_lat': res[2], 'stop_lon': res[3]}

#
# Djikstra algo
#


def init_graph(stop_start):
    graph = []
    stops = get_all_stops()
    for stop in stops:
        if stop[0] != stop_start:
            graph.append(Node(stop[0], math.inf, None,
                         stop[1], stop[2], stop[3]))
        else:
            graph.append(Node(stop[0], 0, None,
                         stop[1], stop[2], stop[3]))

    return graph


def find_min(graph):
    m = math.inf
    idx = 0
    node = None
    for i in range(len(graph)):
        if graph[i].dist < m:
            m = graph[i].dist
            node = graph[i]
            idx = i
    return idx, node


def maj_distances(graph, node):
    linked_node = get_linked_stop(node.id)

    for stop in linked_node:
        for n in graph:
            if n.id == stop[0] and n.dist > (node.dist + float(stop[1])):
                n.dist = node.dist + float(stop[1])
                n.pred = node.id
    return graph


def find_route(graph, id_start, id_end):
    route = []
    for n in graph:
        if n.id == id_end:
            route.append(n)
            s = n.pred
            print(
                '\nDistance : {d} min / {h} hours'.format(d=n.dist, h=n.dist / 60))
            break
    while 1:
        for n in graph:
            if n.id == s:
                route.append(n)
                s = n.pred
                break
        if n.id == id_start:
            break
    # draw_map(route)
    return route


def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '█' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('Progress: [%s] %s%s Mapped%s\r' %
                     (bar, percents, '%', suffix))
    sys.stdout.flush()


def dijkstra(id_start, id_end):
    graph = init_graph(id_start)
    res = []
    i = 0
    tt = len(graph)
    while len(graph) > 1:
        progress(i, tt)
        i += 1
        idx, next_n = find_min(graph)
        res.append(next_n)
        if next_n == None or next_n.id == id_end:
            break
        del graph[idx]
        graph = maj_distances(graph, next_n)
    if next_n == None:
        return None
    return find_route(res, id_start, id_end)


def find_shorter_trip(route, start_id, end_id):
    trips = []
    while start_id != end_id:
        for stop in route:
            # with date : and c.monday = '1' and c.start_date <= '20200302' and c.end_date >= '20200302'
            sql = "select st.trip_id, st.departure_time, st.arrival_time, c.start_date, c.end_date, c.monday, c.tuesday, c.wednesday, c.thursday, c.friday, c.saturday, c.sunday from stop_times st left join trips t on t.trip_id = st.trip_id left join calendar c on t.service_id = c.service_id where st.stop_id = '{s}' and st.trip_id in (select trip_id from stop_times st where stop_id = '{e}') order by departure_time asc".format(
                s=start_id, e=stop.id)
            cursor.execute(sql)

            def get_departure_time(trip_id):
                sql = "select st.departure_time from stop_times st where trip_id = '{t}' and stop_id = '{s}'".format(
                    t=trip_id, s=stop.id)
                cursor.execute(sql)
                res = cursor.fetchone()
                if res != None:
                    return res[0]
                return ''
            resql = list(map(lambda x: {
                         'trip_id': x[0],
                         'departure_stop': start_id,
                         'arrival_stop': stop.id,
                         'departure_time': x[1],
                         'arrival_time': get_departure_time(x[0]),
                         'start_date': x[3],
                         'end_date': x[4],
                         'monday': x[5],
                         'tuesday': x[6],
                         'wednesday': x[7],
                         'thursday': x[8],
                         'friday': x[9],
                         'saturday': x[10],
                         'sunday': x[11]}, cursor.fetchall()))
            if len(resql) > 0 and stop.id == end_id:
                trips.append(Trip(start_id, end_id, resql))
                start_id = end_id
                break
            elif len(resql) > 0:
                trips.append(Trip(start_id, stop.id, resql))
                start_id = stop.id
                break
    return trips


def format_possible_trip(possible_trip, start_name, end_name):
    date_start = '00000000'
    date_end = '99999999'
    days = {'monday': 0, 'tuesday': 0, 'wednesday': 0,
            'thursday': 0, 'friday': 0, 'saturday': 0, 'sunday': 0}
    for trip in possible_trip:
        if trip['start_date'] > date_start:
            date_start = trip['start_date']
        if trip['end_date'] < date_end:
            date_end = trip['end_date']
        for day in days.keys():
            days[day] += int(trip[day])
    error = True
    for i in days.keys():
        if days[i] == len(possible_trip):
            days[i] = 1
            error = False
        else:
            days[i] = 0
    if date_start > date_end or error == True:
        return None
    return {'start': start_name, 'end': end_name, 'date_start': format_date(date_start), 'date_end': format_date(date_end), 'time_start': possible_trip[0]['departure_time'][:5], 'time_end': possible_trip[len(possible_trip)-1]['arrival_time'][:5], 'days': days, 'trips': possible_trip}


def get_possible_trips(trips, start_name, end_name):
    def find_trip(list_trip, previous_trip):
        res = -1
        for trip in list_trip:
            if trip['start_date'] == None or trip['end_date'] == None:
                continue
            if trip != None and trip['departure_time'] >= previous_trip['arrival_time'] and ((previous_trip['start_date'] >= trip['start_date'] and previous_trip['start_date'] <= trip['end_date']) or (previous_trip['end_date'] >= trip['start_date'] and previous_trip['end_date'] <= trip['end_date'])):
                if res == -1 or res['departure_time'] > trip['departure_time']:
                    if trip['departure_stop'].find('StopPoint') != -1:
                        trip['departure_stop'] = get_stop_name(
                            trip['departure_stop'])
                    if trip['arrival_stop'].find('StopPoint') != -1:
                        trip['arrival_stop'] = get_stop_name(
                            trip['arrival_stop'])
                    res = trip
        return res
    res = []
    for trip in trips[0].trips:
        i = 1
        if trip['departure_stop'].find('StopPoint') != -1:
            trip['departure_stop'] = get_stop_name(trip['departure_stop'])
        if trip['arrival_stop'].find('StopPoint') != -1:
            trip['arrival_stop'] = get_stop_name(trip['arrival_stop'])
        possible_trip = [trip]
        if trip['start_date'] == None or trip['end_date'] == None:
            continue
        while i < len(trips):
            r = find_trip(trips[i].trips, trip)
            if r != -1:
                possible_trip.append(r)
                trip = r
                i += 1
            else:
                break
        if i == len(trips):
            possible_trip = format_possible_trip(
                possible_trip, start_name, end_name)
            if possible_trip != None:
                res.append(possible_trip)
    return res


def get_trip(start_id, end_id):
    route = dijkstra(start_id, end_id)
    trips = [start_id, end_id]
    if route and len(route) > 0:
        trips = find_shorter_trip(route, start_id, end_id)
    return trips, get_possible_trips(trips, get_stop_name(start_id), get_stop_name(end_id))


if __name__ == '__main__':
    # start = 'StopPoint:OCETrain TER-87474007'  # Brest
    start = 'StopPoint:OCETrain TER-87481002'  # Nantes
    # start = 'StopPoint:OCETrain TER-87775007'
    # end = 'StopPoint:OCETrain TER-87471003'

    end = 'StopPoint:OCETrain TER-87751008'  # Marseille
    # end = 'StopPoint:OCETrain TER-87391003'  # Paris
    start_time = time.time()

    # start = 'StopPoint:OCETrain TER-87723197'  # lyon part dieu
    # end = 'StopPoint:OCETrain TER-87686667'  # Paris bercy
    start = 'StopPoint:OCETrain TER-87474007'
    end = 'StopPoint:OCETrain TER-87391003'
    route = dijkstra(start, end)
    trips = find_shorter_trip(route, start, end)
    for trip in trips:
        print("$> trip From\t{s}\tTo\t{e}".format(
            s=trip.start_id, e=trip.end_id))
        print(trip.trips)

    def find_trip(list_trip, previous_trip):
        for trip in list_trip:
            if trip['start_date'] == None or trip['end_date'] == None:
                continue
            if trip != None and trip['departure_time'] >= previous_trip['arrival_time'] and ((previous_trip['start_date'] >= trip['start_date'] and previous_trip['start_date'] <= trip['end_date']) or (previous_trip['end_date'] >= trip['start_date'] and previous_trip['end_date'] <= trip['end_date'])):
                return trip
        return -1
    res = []
    for trip in trips[0].trips:
        i = 1
        possible_trip = [trip]
        if trip['start_date'] == None or trip['end_date'] == None:
            continue
        while i < len(trips):
            r = find_trip(trips[i].trips, trip)
            if r != -1:
                possible_trip.append(r)
                trip = r
                i += 1
            else:
                break
        if i == len(trips):
            res.append(format_possible_trip(possible_trip))
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    for trips in res:
        print('Possible trip :')
        print(trips)
    exit(0)

    sqls = []
    for trip in trips:
        sqls.append("select stop_name from stops s where stop_id = '{id}'".format(
            id=trip.start_id))
        print("$> trip From\t{s}\tTo\t{e}".format(
            s=trip.start_id, e=trip.end_id))
        print(trip.trips)

    sqls.append(
        "select stop_name from stops s where stop_id = '{id}'".format(id=end))
    for sql in sqls:
        cursor.execute(sql)
        print(list(map(lambda x: x[0], cursor.fetchall())))
    # resql = resql.reverse()
    # print(resql)
    # 20200326
    end_time = time.time()
    print("Compute time : ", end_time - start_time, 'sec')
    exit(0)
