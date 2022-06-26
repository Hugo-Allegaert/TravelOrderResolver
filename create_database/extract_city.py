
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


def get_all_stops():
    sql = "SELECT distinct stop_name FROM stops WHERE stop_id like '%Train%';"
    cursor.execute(sql)
    res = cursor.fetchall()
    return res


if __name__ == '__main__':
    global conn, cursor

    conn = psycopg2.connect(
        host="localhost",
        database="sncf",
        user="postgres",
        password="postgres",
        port="5432")

    cursor = conn.cursor()

    stops = get_all_stops()
    f = open("city_name.csv", "a")
    for stop in stops:
        stop_name = stop[0][9:len(stop[0]) - 1]
        f.write(stop_name+'\n')
    f.close()
    exit(0)
