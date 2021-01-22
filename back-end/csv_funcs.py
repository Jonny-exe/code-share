# csvFuncs.py
import csv
import os
from os.path import dirname
import sys
from dotenv import load_dotenv

env_path = dirname(os.getenv("CODE_SHARE_ENV"))
load_dotenv(env_path)
filename = os.getenv("CSV_FILE_PATH")
print("Filename: ", filename)

# csv data
rows = {"status": 1, "type": 1, "color": "blue", "dead": 1}

fieldnames = ["group", "message_length", "likes"]


def add_row(row: dict):
    with open(filename, "a+", encoding="UTF8", newline="") as file:
        writer = csv.writer(file)
        if os.stat(filename).st_size == 0:
            writer.writerow(fieldnames)

        # I make this to ensure the order is right
        new_row = []
        for key in fieldnames:
            if key in row.keys():
                new_row.append(row[key])
        print("New_row: ", new_row)

        # I check that the new row isnt empty or has fields missing
        if len(new_row) > 0 and len(new_row) == len(fieldnames):
            print("Writting")
            writer.writerow(new_row)
        file.close()
