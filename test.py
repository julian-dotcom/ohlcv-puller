#!/usr/bin/python3
import datetime as dt
import os
import pathlib

path = pathlib.Path().resolve() + "/"
now = dt.datetime.utcnow()

f = open(f"{path}log.txt", "w")
f.write(str(now))
f.close()
