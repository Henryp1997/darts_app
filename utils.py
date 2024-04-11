from datetime import datetime
import os
from dash import no_update as nop

data_path = f"{os.path.dirname(os.path.realpath(__file__))}/data_store"

def calculate_total(d1, d2, d3):
    darts = [d1, d2, d3]
    if 'Bull' in darts:
        darts[darts.index('Bull')] = 50
    d1, d2, d3 = convert_score(d1), convert_score(d2), convert_score(d3)
    return d1, d2, d3, sum([int(i) for i in [d1, d2, d3]])

def write_darts_to_file(d1, d2, d3, target):
    csv_file = f"{data_path}/{target}_practice.csv"
    now = datetime.strftime(datetime.now(), "%d/%m/%Y")
    if target != "bull":
        d1, d2, d3, total = calculate_total(d1, d2, d3) 

    with open(csv_file, "a") as f:
        if target != "bull":
            f.write(f"\n{now},{d1},{d2},{d3},{total}")
        else:
            # don't care about total for bullseye practice
            f.write(f"\n{now},{d1},{d2},{d3}")

def read_3_dart_avg(target, avg=True):
    with open(f"{data_path}/{target}_3_dart_avg.txt", "r") as f:
        lines = f.readlines()
    return float(lines[avg].split("= ")[1])

def update_3_dart_avg_file(n_visits, avg, target):
    with open(f"{data_path}/{target}_3_dart_avg.txt", "w") as f:
        f.write(f"number of visits = {n_visits}\n3 dart average = {avg}")

def record_miss_bull_25(name, d1, d2):
    # what value to show in the top score bar
    val_dict = {"miss": "0", "bull": "Bull", "25": "25"}
    if d1 == "_____":
        return val_dict[name], nop, nop
    if d2 == "_____":
        return nop, val_dict[name], nop
    return nop, nop, val_dict[name]

def convert_score(value):
    if 'D' in value:
        return int(value.split("D")[1]) * 2
    if 'T' in value:
        return int(value.split("T")[1]) * 3
    if value == "Bull":
        return 50
    return int(value)