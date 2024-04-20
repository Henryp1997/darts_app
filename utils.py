from datetime import datetime
import os
from dash import no_update as nop
import math

data_path = f"{os.path.dirname(os.path.realpath(__file__))}/data_store"

def calculate_total(d1, d2, d3):
    darts = [d1, d2, d3]
    if 'Bull' in darts:
        darts[darts.index('Bull')] = '50'
    darts = [convert_score(i) for i in darts]
    return sum([int(i) for i in darts])

def convert_bull_to_50(darts):
    new_darts = []
    for i in darts:
        if i == "Bull":
            new_darts.append(50)
        else:
            new_darts.append(i)
    return new_darts

def write_darts_to_file(d1, d2, d3, target):
    csv_file = f"{data_path}/{target}_practice.csv"
    now = datetime.strftime(datetime.now(), "%d/%m/%Y")
    
    new_darts = convert_bull_to_50([d1, d2, d3])

    if target != "bull":
        total = calculate_total(d1, d2, d3)

    with open(csv_file, "a") as f:
        if target != "bull":
            f.write(f"\n{now},{new_darts[0]},{new_darts[1]},{new_darts[2]},{total}")
        else:
            # don't care about total for bullseye practice
            f.write(f"\n{now},{new_darts[0]},{new_darts[1]},{new_darts[2]}")

def read_3_dart_avg(target, avg=True):
    with open(f"{data_path}/{target}_3_dart_avg.txt", "r") as f:
        lines = f.readlines()
    return float(lines[avg].split("= ")[1])

def update_3_dart_avg_file(n_visits, avg, target):
    with open(f"{data_path}/{target}_3_dart_avg.txt", "w") as f:
        f.write(f"number of visits = {n_visits}\n3 dart average = {avg}")

def record_dart_in_correct_place(value, btn_names, d1, d2):
    if value in ['miss', 'bull', '25']:
        val_dict = {"miss": "0", "bull": "Bull", "25": "25"}
        value = val_dict[value]
    else:
        value = btn_names[int(value) - 1]
    if d1 == "_____":
        return value, nop, nop
    if d2 == "_____":
        return nop, value, nop
    return nop, nop, value

def convert_score(value):
    if 'D' in value:
        return int(value.split("D")[1]) * 2
    if 'T' in value:
        return int(value.split("T")[1]) * 3
    if value == "Bull":
        return 50
    return int(value)

def convert_all_btns_to_dbl_tbl(btn_1_text, d_or_t):
    if d_or_t.upper() in btn_1_text:
        return [f"{i}" for i in range(1, 21)]
    return [f"{d_or_t}{i}" for i in range(1, 21)]

def initialise_3_dart_avg(df):
    n_visits = len(df)
    avg = float("%.2f" % df['Total'].mean())
    total = int(df['Total'].sum())
    if math.isnan(avg):
        avg = "0"
        total = "0"
    # update_3_dart_avg_file(n_visits, avg, target)
    return str(avg), str(total), str(n_visits)

def create_3_dart_avg_file(data_path, target):
    with open(f"{data_path}/{target}_practice.csv", "w") as f:
        f.write("Timestamp,Dart1,Dart2,Dart3,Total")
    f.close()

def calc_session_3_dart_avg(n_visits, running_total):
    return int(running_total) / (int(n_visits) + 1)

def calc_alltime_3_dart_avg(n_visits, n_visits_all, running_total, alltime_total):
    return (int(alltime_total) + int(running_total)) / (int(n_visits_all) + int(n_visits) + 1)
