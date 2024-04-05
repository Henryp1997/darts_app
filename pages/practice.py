import dash
from dash import html, callback
from dash import no_update as nop
from dash.dependencies import Output, Input, State
import math
import os
import pandas as pd
from utils import *

dash.register_page(__name__)

titles = {
    "t20": "Treble 20 Practice",
    "t19": "Treble 19 Practice",
    "bull": "Bullseye Practice"
}

titles_rev = {
    "Treble 20 Practice": "t20",
    "Treble 19 Practice": "t19",
    "Bullseye Practice": "bull"
}

def layout(target=None):
    if target not in ("t20", "t19", "bull"):
        print("hello")
        return html.Div("404", style={"color": "white", "font-size": "2rem"})
    return html.Div([
            html.Div(f"{titles[target]}", id="title", style={"color": "white", "font-size": "2rem", "border-bottom": "1px solid #fff"}),
            html.Div("0", id="n_visits", style={"display": "none"}),
            html.Div(style={"height": "1rem"}),
            html.Div([
                html.Div(style={"height": "0.5rem"}),
                html.Div("..", style={"color": "black", "display": "inline-block"}),
                html.Div("Darts:", style={"color": "white", "display": "inline-block"}),
                html.Div("......", style={"color": "black", "display": "inline-block"}),
                html.Div("_____", id="dart_1", style={"color": "white", "display": "inline-block"}),
                html.Div("......", style={"color": "black", "display": "inline-block"}),
                html.Div("_____", id="dart_2", style={"color": "white", "display": "inline-block"}),
                html.Div("......", style={"color": "black", "display": "inline-block"}),
                html.Div("_____", id="dart_3", style={"color": "white", "display": "inline-block"}),
                html.Div(style={"height": "0.5rem"}),
            ], style={"border": "2px solid #fff"}),
            html.Div(style={"height": "0.5rem"}),
            html.Div([
                html.Div(style={"height": "0.5rem"}),
                html.Div("..", style={"color": "black", "display": "inline-block"}),
                html.Div("3-dart average (current session):", style={"color": "white", "display": "inline-block"}),
                html.Div("......", style={"color": "black", "display": "inline-block"}),
                html.Div("_____", id="3_dart_avg_current", style={"color": "white", "display": "inline-block"}),
                html.Div(style={"height": "0.5rem"}),
            ], style={"border": "2px solid #fff"}),
            html.Div(style={"height": "0.5rem"}),
            html.Div([
                html.Div(style={"height": "0.5rem"}),
                html.Div("..", style={"color": "black", "display": "inline-block"}),
                html.Div("3-dart average (all time):", style={"color": "white", "display": "inline-block"}),
                html.Div("......", style={"color": "black", "display": "inline-block"}),
                html.Div("_____", id="3_dart_avg", style={"color": "white", "display": "inline-block"}),
                html.Div(style={"height": "0.5rem"}),
            ], style={"border": "2px solid #fff"}),
            html.Div(style={"height": "0.5rem"}),
            html.Div([
                html.Div([
                    html.Div([
                        *[html.Button(f"{i}", id=f"btn_{i}") for i in range(1, 6)]
                    ]),
                    html.Div([
                        *[html.Button(f"{i}", id=f"btn_{i}") for i in range(6, 11)]
                    ]),
                    html.Div([
                        *[html.Button(f"{i}", id=f"btn_{i}") for i in range(11, 16)]
                    ]),
                    html.Div([
                        *[html.Button(f"{i}", id=f"btn_{i}") for i in range(16, 21)]                        
                    ]),
                    html.Div([
                        html.Button("25", id="btn_25"),
                        html.Button("Bull", id="btn_bull"),
                        html.Button("Miss", id="btn_miss"),
                    ]),
                    html.Div([
                        html.Button("Double", id="btn_double", className="green_button", style={"width": "7.05rem"}),
                        html.Button("Treble", id="btn_treble", className="green_button", style={"width": "7.05rem"}),
                        html.Button("⬅", id="btn_backspace", className="backspace_button"),
                        html.Button("\u2714", id="btn_confirm", disabled=True, className="green_button")
                    ])
                ])
            ]),
        ])

### CALLBACKS
@callback(
    Output("3_dart_avg", "children"),
    Input("btn_1", "children"),
    State("title", "children")
)
def init_avg_file(n, title):
    # use title as an input but only trigger this callback once - on page load
    target = titles_rev[title]
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger == ".":
        try:
            df = pd.read_csv(f"{data_path}/{target}_practice.csv")
            n_visits = len(df)
            avg = float("%.2f" % df['Total'].mean())
            if math.isnan(avg):
                avg = "0"
            update_3_dart_avg_file(n_visits, avg, target)
            return str(avg)
        except FileNotFoundError:
            # init file if not found
            with open(f"{data_path}/{target}_practice.csv", "w") as f:
                f.write("Timestamp,Dart1,Dart2,Dart3,Total")
            f.close()
            return "_____"        
    return nop

@callback(
    *[Output(f"btn_{i}", "children") for i in range(1, 21)],
    Input("btn_1", "children"),
    Input("btn_double", "n_clicks"),
    Input("btn_treble", "n_clicks"),
    *[Input(f"btn_{i}", "n_clicks") for i in range(1, 21)],
    prevent_initial_call=True
)
def double_treble_text(btn_1_text, n_double, n_treble, *btns):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if "double" in trigger:
        if "D" in btn_1_text:
            return [f"{i}" for i in range(1, 21)]
        return [f"D{i}" for i in range(1, 21)]
    elif "treble" in trigger:
        if "T" in btn_1_text:
            return [f"{i}" for i in range(1, 21)]
        return [f"T{i}" for i in range(1, 21)]
      
    # below code executed if one of the number buttons triggered this callback
    # just returns the button texts to non double or treble after each input
    return [f"{i}" for i in range(1, 21)]

@callback(
    Output("dart_1", "children"),
    Output("dart_2", "children"),
    Output("dart_3", "children"),
    *[Input(f"btn_{i}", "n_clicks") for i in range(1, 21)],
    Input("btn_25", "n_clicks"),
    Input("btn_bull", "n_clicks"),
    Input("btn_miss", "n_clicks"),
    *[State(f"btn_{i}", "children") for i in range(1, 21)],
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def record_thrown_dart(*args):
    if args[-1] != "_____":
        return nop, nop, nop
    trigger = dash.callback_context.triggered[0]['prop_id']
    btn_names = args[23:-3]
    
    value = trigger.split("btn_")[1].split(".n_clicks")[0]
    if value in ['miss', 'bull', '25']:
        return record_miss_bull_25(value, args[-3], args[-2])            
    
    value = int(value)
    if args[-3] == "_____":
        return btn_names[value - 1], nop, nop
    if args[-2] == "_____":
        return nop, btn_names[value - 1], nop
    return nop, nop, btn_names[value - 1]
    
@callback(
    Output("dart_1", "children", allow_duplicate=True),
    Output("dart_2", "children", allow_duplicate=True),
    Output("dart_3", "children", allow_duplicate=True),
    Input("btn_confirm", "n_clicks"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    State("title", "children"),
    prevent_initial_call=True
)
def record_all_3_darts(n_confirm, d1, d2, d3, title):
    write_darts_to_file(d1, d2, d3, titles_rev[title])
    return "_____", "_____", "_____"

@callback(
    Output("dart_1", "children", allow_duplicate=True),
    Output("dart_2", "children", allow_duplicate=True),
    Output("dart_3", "children", allow_duplicate=True),
    Input("btn_backspace", "n_clicks"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def delete_dart_input(n_backspace, d1, d2, d3):
    if d3 != "_____":
        return nop, nop, "_____"
    if d2 != "_____":
        return nop, "_____", "_____"
    return "_____", "_____", "_____"

@callback(
    Output("btn_confirm", "disabled"),
    Input("dart_3", "children"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    prevent_initial_call=True
)
def enable_confirm_btn(dart_3, dart_1, dart_2):
    return dart_3 == "_____"
    
@callback(
    Output("3_dart_avg_current", "children"),
    Output("n_visits", "children"),
    Input("btn_confirm", "n_clicks"),
    State("3_dart_avg_current", "children"),
    State("n_visits", "children"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def record_3_dart_avg(n_confirm, curr_avg, n_visits, dart_1, dart_2, dart_3):
    dart_1 = convert_score(dart_1)
    dart_2 = convert_score(dart_2)
    dart_3 = convert_score(dart_3)

    curr_avg = 0 if curr_avg == "_____" else int(curr_avg)
    n_visits = int(n_visits)
    new_avg = float("%.2f" % (((n_visits * curr_avg) + (dart_1 + dart_2 + dart_3)) / (n_visits + 1)))

    return new_avg, str(n_visits + 1)

@callback(
    Output("3_dart_avg", "children", allow_duplicate=True),
    Input("btn_confirm", "n_clicks"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    State("title", "children"),
    prevent_initial_call=True
)
def record_3_dart_avg_all_time(n_confirm, dart_1, dart_2, dart_3, title):
    target = titles_rev[title]
    dart_1 = convert_score(dart_1)
    dart_2 = convert_score(dart_2)
    dart_3 = convert_score(dart_3)

    n_visits = read_3_dart_avg(target, avg=False)
    curr_avg = read_3_dart_avg(target)
    new_avg = (((n_visits * curr_avg) + (dart_1 + dart_2 + dart_3)) / (n_visits + 1))
    new_avg_2dp = float("%.2f" % new_avg)

    update_3_dart_avg_file(n_visits + 1, new_avg, target)

    return new_avg_2dp
