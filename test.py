#!/usr/bin/python3
import datetime as dt
import os
import pathlib

path = str(pathlib.Path(__file__).parent.resolve()) + "/log.txt"
print(path)
now = dt.datetime.utcnow()

f = open(path, "w")
f.write(str(now))
f.close()
