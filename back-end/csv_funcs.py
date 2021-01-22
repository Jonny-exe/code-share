# csvFuncs.py
import csv
import os
import sys

filename = "/home/a/Documents/GitHub/tensorflow-text/src/tensorflow/test1.csv"

# csv data
rows = {"status": 1, "type": 1, "color": "blue", "dead": 1}

fieldnames = ["status", "type", "color", "dead"]


def add_row(row: dict):
    with open(filename, "a+", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        if os.stat(filename).st_size == 0:
            writer.writeheader()

        # I make this to ensure the order is right
        newRow = []
        for key in fieldnames:
            if key in row.keys():
                newRow.append(row[key])

        # I check that the new row isnt empty or has fields missing
        if len(newRow) > 0 and len(newRow) == len(fieldnames):
            writer.writerow(newRow)
        file.close()
