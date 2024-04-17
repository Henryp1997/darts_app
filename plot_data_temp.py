import pandas as pd
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

    colours = ['blue', 'red', 'green']
    names = ['Singles', 'Doubles', 'Trebles']

    file_name_descriptors = {
        1: "sngl",
        2: "dbl",
        3: "tbl"
    }
    if sngl_dbl_tbl == "all":
        i_to_keep = [1, 2, 3]
        i_to_skip = []
    elif "," not in sngl_dbl_tbl:
        i_to_keep = [int(sngl_dbl_tbl)]
        i_to_skip = [i-1 for i in range(1, 4) if i != int(sngl_dbl_tbl)]
    else:
        i_to_keep = [int(i.strip(" ")) for i in sngl_dbl_tbl.split(",")]
        i_to_skip = [i-1 for i in range(1, 4) if i not in i_to_keep]

    file_name_ext = ""
    for i in i_to_keep:
        file_name_ext += f"_{file_name_descriptors[i]}"

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

t20_linearised_score = ['0', '3', '19', '7', '16', '8', '11', '14', '9', '12', '5', '20', '1', '18', '4', '13', '6', '10', '15', '2', '17', '25', '50']
t19_linearised_score = ['0', '1', '20', '5', '12', '9', '14', '11', '8', '16', '7', '19', '3', '17', '2', '15', '10', '6', '13', '4', '18', '25', '50']

for dart in ["1", "2", "3", "1, 2", "1, 3", "2, 3", "all"]:
    plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="1")
    plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="2")
    plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="3")
    plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="1, 2")
    plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="1, 3")
    plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="2, 3")
    plot_score_freq("t20", t20_linearised_score, dart=dart, sngl_dbl_tbl="all")

for dart in ["1", "2", "3", "1, 2", "1, 3", "2, 3", "all"]:
    plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="1")
    plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="2")
    plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="3")
    plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="1, 2")
    plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="1, 3")
    plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="2, 3")
    plot_score_freq("t19", t19_linearised_score, dart=dart, sngl_dbl_tbl="all")