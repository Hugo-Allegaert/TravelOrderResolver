import os
import re
import psycopg2
import sys
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *

routes_list = []


class Route:
    def __init__(self, id, name):
        self.route_id = id
        self.name = name


#
# Sql function
#
def get_all_stops():
    sql = "SELECT stop_lon, stop_lat FROM stops WHERE 1=1;"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


def get_all_routes():
    sql = "SELECT distinct t.trip_id, r.route_long_name FROM trips t, routes r WHERE t.route_id = r.route_id;"
    cursor.execute(sql)
    resql = cursor.fetchall()
    routes = []
    for res in resql:
        routes.append(Route(res[0], res[1]))
    return routes


def get_routes_by_name(name):
    sql = "SELECT r.route_id, r.route_long_name FROM routes r WHERE r.route_long_name like '%"+name+"%';"
    cursor.execute(sql)
    resql = cursor.fetchall()
    routes = []
    for res in resql:
        routes.append(Route(res[0], res[1]))
    return routes


def get_route_stops(id):
    sql = "SELECT distinct s.stop_lon,  s.stop_lat, s.stop_name FROM trips t LEFT JOIN stop_times st on t.trip_id = st.trip_id LEFT JOIN stops s on st.stop_id = s.stop_id where t.route_id = '" + \
        str(id)+"';"
    cursor.execute(sql)
    resql = cursor.fetchall()
    x = []
    y = []
    label = []
    for res in resql:
        x.append(float(res[0]))
        y.append(float(res[1]))
        label.append(res[2])
    return x, y, label


def get_trip(id):
    sql = "SELECT s.stop_lon, s.stop_lat, s.stop_name from stop_times st, stops s WHERE trip_id = '" + \
        str(id)+"' AND s.stop_id = st.stop_id;"
    cursor.execute(sql)
    resql = cursor.fetchall()
    x = []
    y = []
    label = []
    for res in resql:
        x.append(float(res[0]))
        y.append(float(res[1]))
        label.append(res[2])
    return x, y, label


#
# Tkinter function
#
def draw_trip(plt, trip_id, color):
    x, y, label = get_trip(trip_id)
    for i in range(len(x)):
        plt.plot(x[i], y[i], color+'h')
        plt.text(x[i], y[i], label[i],
                 fontsize=9, fontname="Helvetica", weight="bold")


def draw_route(plt, route_id, color):
    x, y, label = get_route_stops(route_id)
    for i in range(len(x)):
        plt.plot(x[i], y[i], color+'h')
        plt.text(x[i], y[i], label[i],
                 fontsize=9, fontname="Helvetica", weight="bold")


def draw_map(routes_id):
    stops = get_all_stops()
    x = []
    y = []
    for data in stops:
        if float(data[1]) > float(20):
            x.append(float(data[0]))
            y.append(float(data[1]))

    plt.scatter(x, y)

    color = ['m', 'g', 'r', 'y', 'c']
    i = 0
    for route_id in routes_id:
        if i >= len(color):
            i = 0
        draw_route(plt, route_id, color[i])
        i += 1
    plt.show()


def show_route():
    idx = Lb1.curselection()
    routes_id = []
    if len(sys.argv) > 1:
        routes_id = sys.argv[1:]
    else:
        for id in idx:
            routes_id.append(routes_list[id].route_id)
    draw_map(routes_id)


def search_route():
    global routes_list
    Lb1.delete(0, Lb1.size())
    name = entry1.get()
    entry1.delete(0, 'end')
    routes_list = get_routes_by_name(str(name))
    for i in range(len(routes_list)):
        Lb1.insert(i, routes_list[i].name)


def init_tk():
    root = tk.Tk()
    global canvas1, entry1
    canvas1 = tk.Canvas(root, width=600, height=320,  relief='raised')
    canvas1.pack()

    label1 = tk.Label(root, text='Find your trip')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(300, 25, window=label1)

    label2 = tk.Label(root, text='Search your route:')
    label2.config(font=('helvetica', 12))
    canvas1.create_window(200, 120, window=label2)

    canvas1.create_window(400, 80, window=tk.Label(root, text='Route list'))

    entry1 = tk.Entry(root)
    canvas1.create_window(200, 140, window=entry1)

    button1 = tk.Button(text='Search', command=search_route)
    canvas1.create_window(200, 170, window=button1)

    button2 = tk.Button(text='Show', command=show_route)
    canvas1.create_window(400, 280, window=button2)

    # listbox
    global Lb1
    Lb1 = Listbox(root, selectmode=MULTIPLE)
    canvas1.create_window(400, 180, window=Lb1)

    root.mainloop()


if __name__ == '__main__':
    global conn, cursor

    conn = psycopg2.connect(
        host="localhost",
        database="sncf",
        user="postgres",
        password="postgres",
        port="5432")
    cursor = conn.cursor()

    init_tk()

    cursor.close()
    conn.close()
    exit(0)
