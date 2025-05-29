from datetime import datetime
from dash import no_update as nop
import math

# App specific imports
from consts import DATA_PATH

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
    csv_file = f"{DATA_PATH}/{target}_practice.csv"
    now = datetime.strftime(datetime.now(), "%d/%m/%Y")
    
    new_darts = convert_bull_to_50([d1, d2, d3])

    if target != "bull":
        total = calculate_total(d1, d2, d3)

    with open(csv_file, "a") as f:
        if target != "bull":
            f.write(f"{now},{new_darts[0]},{new_darts[1]},{new_darts[2]},{total}\n")
        else:
            # don't care about total for bullseye practice
            f.write(f"{now},{new_darts[0]},{new_darts[1]},{new_darts[2]}\n")


def read_3_dart_avg(target, avg=True):
    with open(f"{DATA_PATH}/{target}_3_dart_avg.txt", "r") as f:
        lines = f.readlines()
    return float(lines[avg].split("= ")[1])


def update_3_dart_avg_file(n_visits, avg, target):
    with open(f"{DATA_PATH}/{target}_3_dart_avg.txt", "w") as f:
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


def create_3_dart_avg_file(DATA_PATH, target):
    with open(f"{DATA_PATH}/{target}_practice.csv", "w") as f:
        f.write("Timestamp,Dart1,Dart2,Dart3,Total")
    f.close()


def calc_session_3_dart_avg(n_visits, running_total, just_deleted):
    if just_deleted:
        try:
            return int(running_total) / int(n_visits)
        except ZeroDivisionError:
            return 0
    return int(running_total) / (int(n_visits) + 1)


def calc_alltime_3_dart_avg(n_visits, n_visits_all, running_total, alltime_total, just_deleted):
    if just_deleted:
        return (int(alltime_total) + int(running_total)) / (int(n_visits_all) + int(n_visits))
    return (int(alltime_total) + int(running_total)) / (int(n_visits_all) + int(n_visits) + 1)


def delete_last_entry_in_file(target):
    csv_file = f"{DATA_PATH}/{target}_practice"
    with open(f'{csv_file}.csv', "r") as f:
        lines = f.readlines()
    
    f.close()

    open(f'{csv_file}.csv', 'w').close()
    with open(f'{csv_file}.csv', 'a') as g:
        for i, line in enumerate(lines):
            if '/' in line or 'Timestamp' in line: # line not empty
                try:
                    x = lines[i + 1]
                except IndexError:
                    return line.strip("\n").split(",")[-1]
                g.write(line)


def verify_checkout(darts, formatted_darts, score_remaining):
    for i, dart in enumerate(darts):
        if "D" in dart:
            total_thrown_inc_dbl = 2 * int(dart.split("D")[1]) + formatted_darts[i - 1] + formatted_darts[i - 2]
            return total_thrown_inc_dbl == int(score_remaining)


def verify_checkout_numpad(score_thrown, score_remaining):
    bogeys = [169, 168, 166, 165, 163, 162, 159]
    if score_remaining > 170 or score_remaining in bogeys:
        return False
    return score_thrown == score_remaining
    

def calc_remaining_score_numpad(score, score_thrown):
    return str(score - score_thrown) if score_thrown < score - 1 else str(score)
