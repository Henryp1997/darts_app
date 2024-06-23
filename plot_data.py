import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import collections
import os

plt.rcParams['axes.facecolor'] = '#FFFFFF'
plt.rcParams['figure.dpi'] = 300
plt.rcParams["figure.figsize"] = (11,5)

def plot_score_freq(target, linearised_score, dart="all", sngl_dbl_tbl="all"):
    df = pd.read_csv(f"{os.path.dirname(os.path.realpath(__file__))}/data_store/{target}_practice.csv")

    # order list how scores appear on dart board
    sngl_scores = linearised_score

    # get thrown darts
    all_sngl, all_dbl, all_tbl = get_all_darts_from_df(df)
    
    # get filename of plot given sngl_dbl_tbl string
    file_name_ext, i_to_skip = get_filename_ext(sngl_dbl_tbl)

    # now plot extracted data
    colours = ['blue', 'red', 'green']
    names = ['Singles', 'Doubles', 'Trebles']
    fig, ax = plt.subplots()
    for i, scores in enumerate([all_sngl, all_dbl, all_tbl]):
        if i in i_to_skip:
            continue
        
        freq = dict(collections.Counter(scores))

        for score in sngl_scores:
            if score not in scores:
                freq[score] = 0

        index_map = {score: i for i, score in enumerate(sngl_scores)}
        freq = sorted(freq.items(), key=lambda pair: index_map[pair[0]])
        freq = [i[1] for i in freq]

        # plot with same x axis
        ax.bar(sngl_scores, freq, color=colours[i], label=names[i], edgecolor="black", zorder=2)

        ax.grid(linewidth="0.5", linestyle="--", zorder=1)
        ax.legend()
        ax.set_ylabel("Number of hits")
        ax.set_xlabel("Score")

    plt.savefig(f"{os.path.dirname(os.path.realpath(__file__))}/plots/{target}/score_freq_dart_{dart}{file_name_ext}.svg")

def plot_average_over_time(target):
    df = pd.read_csv(f"{os.path.dirname(os.path.realpath(__file__))}/data_store/{target}_practice.csv")

    # want to plot average over time, each row has a date so need to 
    # separate rows into like-dates and calculate the 3 dart averages for each day
    
    # get the 3 dart averages for each recorded session
    avg_array, length_array, avg_of_3dartavg, std_of_3dartavg, min_avg = get_3dartavg_array(df)

    # filter anomalies out of array
    avg_array = filter_anomalous_3dartavgs(avg_array, length_array, avg_of_3dartavg, std_of_3dartavg)

    fig, ax = plt.subplots()

    # now calculate straight line which fits the remaining data
    consecutive_nums = [i for i in range(len(avg_array))]
    popt, pcov = curve_fit(lambda x, m, c: m*x + c, consecutive_nums, avg_array)
    x_fit = np.linspace(consecutive_nums[0], consecutive_nums[-1], 1000)

    # plot data and best fit line
    ax.plot(avg_array, "kx")
    ax.plot(x_fit, popt[0]*x_fit + popt[1], "b--", label=f"y = {popt[0]:.2f}x + {popt[1]:.2f}")

    ax.legend()

    # set limits based on previous minimum (before replacing anomalies with -1)
    # but the current maximum, because some anomalies are very high and we want
    # the maximum of the non anomalies
    ax.set_ylim(min_avg - 5, max(avg_array) + 5)

    ax.grid(linewidth="0.5", linestyle="--", zorder=1)
    ax.set_title(f"3-dart average over time ({target.upper()} practice)")
    ax.set_xlabel(f"Session number")
    ax.set_ylabel(f"3-dart average")
    print(np.sqrt(np.diag(pcov)))

    plt.savefig(f"{os.path.dirname(os.path.realpath(__file__))}/plots/{target}/avg_over_time.png")

# UTILITY FUNCTIONS
def get_all_darts_from_df(df):
    if dart == "all":
        all_darts = [str(i) for i in list(df['Dart1']) + list(df['Dart2']) + list(df['Dart3'])]
    elif "," not in dart:
        all_darts = [str(i) for i in list(df[f'Dart{dart}'])]
    else:
        darts = [i.strip(" ") for i in dart.split(",")]
        dart = f'{darts[0]}_and_{darts[1]}' # for file name
        all_darts = [str(i) for i in list(df[f'Dart{darts[0]}']) + list(df[f'Dart{darts[1]}'])]

    all_sngl = [i for i in all_darts if 'D' not in i and 'T' not in i]
    all_dbl = [i.strip("D") for i in all_darts if 'D' in i]
    all_tbl = [i.strip("T") for i in all_darts if 'T' in i]

    return all_sngl, all_dbl, all_tbl

def get_filename_ext(sngl_dbl_tbl):
    file_name_descriptors = {
        1: "sngl",
        2: "dbl",
        3: "tbl"
    }
    if sngl_dbl_tbl == "all":
        # get all three darts
        i_to_keep = [1, 2, 3]
        i_to_skip = []
    elif "," not in sngl_dbl_tbl:
        # only single dart plot because no commas in string
        i_to_keep = [int(sngl_dbl_tbl)]
        i_to_skip = [i-1 for i in range(1, 4) if i != int(sngl_dbl_tbl)]
    else:
        # commas in string, so at least two darts
        i_to_keep = [int(i.strip(" ")) for i in sngl_dbl_tbl.split(",")]
        i_to_skip = [i-1 for i in range(1, 4) if i not in i_to_keep]

    file_name_ext = ""
    for i in i_to_keep:
        file_name_ext += f"_{file_name_descriptors[i]}"
    
    return file_name_ext, i_to_skip

def get_3dartavg_array(df):
    df_full_length = len(df)
    first_date = df.iloc[1][0]

    df_remaining = df
    current_date = first_date
    avg_array = []
    length_array = []
    cumulative_row_sum = 0
    i = 0
    while True:
        # remove rows that aren't from current date
        df_remaining = df[df['Timestamp'] != current_date]
        df_avg = df.drop(df_remaining.index)

        # calculate 3 dart avg
        avg = sum(df_avg["Total"]/len(df_avg))
        avg_array.append(avg)
        length_array.append(len(df_avg))

        # update variables for loop
        df = df_remaining
        cumulative_row_sum += len(df_avg)

        if cumulative_row_sum == df_full_length - 1 or cumulative_row_sum == df_full_length:
            break

        current_date = df_remaining.iloc[1][0]
        i += 1

    avg_array = np.array(avg_array)
    length_array = np.array(length_array)

    avg_of_3dartavg = np.mean(avg_array)
    std_of_3dartavg = np.std(avg_array)
    min_avg = min(avg_array)

    return avg_array, length_array, avg_of_3dartavg, std_of_3dartavg, min_avg

def filter_anomalous_3dartavgs(avg_array, length_array, avg_of_3dartavg, std_of_3dartavg):
    for i, val in enumerate(avg_array):
        # check if value is more than 3 std devs away from mean
        if abs(val - avg_of_3dartavg) >= 3 * std_of_3dartavg:
            avg_array[i] = -1
        
        # also check if there is not enough data for that day
        # arbitrarly decide this minimum is 10 rows of data
        if length_array[i] < 10:
            avg_array[i] = -1

    # remove -1 data points
    return [i for i in avg_array if i != -1]

t20_linearised_score = ['0', '3', '19', '7', '16', '8', '11', '14', '9', '12', '5', '20', '1', '18', '4', '13', '6', '10', '15', '2', '17', '25', '50']
t19_linearised_score = ['0', '1', '20', '5', '12', '9', '14', '11', '8', '16', '7', '19', '3', '17', '2', '15', '10', '6', '13', '4', '18', '25', '50']

plot_average_over_time('t20')
plot_average_over_time('t19')

# for dart in ["1", "2", "3", "1, 2", "1, 3", "2, 3", "all"]:
#     plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="1")
#     plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="2")
#     plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="3")
#     plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="1, 2")
#     plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="1, 3")
#     plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="2, 3")
#     plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="all")

# for dart in ["1", "2", "3", "1, 2", "1, 3", "2, 3", "all"]:
#     plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="1")
#     plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="2")
#     plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="3")
#     plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="1, 2")
#     plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="1, 3")
#     plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="2, 3")
#     plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="all")