import dash
from dash import html, callback
from dash import no_update as nop
from dash.dependencies import Output, Input, State
import math
import os
import pandas as pd
import dash_bootstrap_components as dbc
from utils import *

dash.register_page(__name__)

def layout(start=None):
    if start not in ("301", "501"):
        return html.Div("404", style={"color": "white", "font-size": "2rem"})
    return html.Div([
            html.Div("0", id="n_visits", style={"display": "none"}),
            html.Div(id="player_started_store", style={"display": "none"}),
            html.Div(id="start_score", style={"display": "none"}),
            # init div
            html.Div([
                html.Div(style={"height": "10rem"}),
                html.Div([
                    html.Div(style={"height": "1rem"}),
                    html.Div("Choose player to start", style={"font-size": "1.5rem", "text-align": "center"}),
                    html.Div(style={"height": "0.5rem"}),
                    html.Div([
                        html.Button("Player 1", id="btn_choose_p1", className="green_button", style={"width": "7.05rem", "margin-right": "2rem"}),
                        html.Button("Player 2", id="btn_choose_p2", className="backspace_button", style={"width": "7.05rem"}),
                    ], style={"text-align": "center"}),
                    html.Div(style={"height": "1rem"}),
                    html.Div([
                        html.Div("Player 1 starts", id="init_choice_text", style={"display": "inline-block", "margin-right": "1rem"}),
                        html.Button("\u2714", id="btn_confirm_init"),
                    ], style={"text-align": "center"}),
                    html.Div(style={"height": "1rem"}),
                ], style={"color": "white", "border": "2px solid white"}),
            ], id="init_screen"),

            html.Div([
                html.Div([
                    html.Div(style={"height": "0.5rem"}),
                    html.Div(".", style={"color": "black", "display": "inline-block", "width": "2.2rem"}),
                    html.Div("Player 1", id="p1_name", style={"font-size": "2rem", "color": "white", "display": "inline-block"}),
                    html.Div(".", style={"color": "black", "display": "inline-block", "width": "4.4rem"}),
                    html.Div("Player 2", id="p2_name", style={"font-size": "2rem", "color": "#aaaaaa", "display": "inline-block"}),
                    html.Div(style={"height": "0.5rem"}),
                ], style={"border": "2px solid #fff", "border-bottom": "none"}),

                html.Div([
                    html.Div(style={"height": "0.2rem"}),
                    html.Div(".", style={"color": "black", "display": "inline-block", "margin-right": "4rem"}),
                    html.Div(f"{start}", id="p1_score", style={"font-size": "2rem", "color": "white", "display": "inline-block"}),
                    html.Div(".", style={"color": "black", "display": "inline-block", "margin-right": "8.5rem"}),
                    html.Div(f"{start}", id="p2_score", style={"font-size": "2rem", "color": "#aaaaaa", "display": "inline-block"}),
                    html.Div(style={"height": "0.5rem"}),
                ], style={"border": "2px solid #fff", "border-top": "none", "border-bottom": "none"}),

                html.Div([
                    html.Div(style={"height": "0.2rem"}),
                    html.Div(".", style={"color": "black", "display": "inline-block", "margin-right": "1rem"}),
                    html.Div("Avg. =", id="p1_avg_text", style={"font-size": "1rem", "color": "white", "display": "inline-block"}),
                    html.Div(".", style={"color": "black", "display": "inline-block", "margin-right": "0.5rem"}),
                    html.Div("_____", id="p1_avg_value", style={"font-size": "1rem", "color": "white", "display": "inline-block"}),
                    html.Div(".", style={"color": "black", "display": "inline-block", "margin-right": "6rem"}),
                    html.Div("Avg. =", id="p2_avg_text", style={"font-size": "1rem", "color": "#aaaaaa", "display": "inline-block"}),
                    html.Div(".", style={"color": "black", "display": "inline-block", "margin-right": "0.5rem"}),   
                    html.Div("_____", id="p2_avg_value", style={"font-size": "1rem", "color": "#aaaaaa", "display": "inline-block"}),
                    html.Div(style={"height": "0.5rem"}),
                ], style={"border": "2px solid #fff", "border-top": "none"}),

                html.Div(style={"height": "0.5rem"}),
                html.Div([
                    html.Div(style={"height": "0.5rem"}),
                    html.Div("..", style={"color": "black", "display": "inline-block"}),
                    html.Div("Darts:", id="darts_heading", style={"color": "white", "display": "inline-block"}),
                    html.Div("......", style={"color": "black", "display": "inline-block"}),
                    html.Div("_____", id="dart_1_match", style={"color": "white", "display": "inline-block"}),
                    html.Div("......", style={"color": "black", "display": "inline-block"}),
                    html.Div("_____", id="dart_2_match", style={"color": "white", "display": "inline-block"}),
                    html.Div("......", style={"color": "black", "display": "inline-block"}),
                    html.Div("_____", id="dart_3_match", style={"color": "white", "display": "inline-block"}),
                    html.Div(style={"height": "0.5rem"}),
                ], id="darts_view", style={"border": "2px solid #fff", "width": "16rem", "display": "inline-block"}),
                
                html.Div([
                    html.Div(style={"height": "0.5rem"}),
                    html.Div("..", style={"color": "black", "display": "inline-block"}),
                    html.Div("Score:", style={"color": "white", "display": "inline-block"}),
                    html.Div("......................", style={"color": "black", "display": "inline-block"}),
                    html.Div("_____", id="numpad_score", style={"color": "white", "display": "inline-block"}),
                    html.Div(style={"height": "0.5rem"}),
                ], id="numpad_view", style={"border": "2px solid #fff", "width": "16rem", "display": "inline-block"}),

                html.Div([
                    html.Div(dbc.Checkbox(id="numpad_toggle"), style={"display": "inline-block", "margin-left": "1rem"}),
                    html.Div("Numpad", style={"display": "inline-block"}),
                ], style={"color": "white", "display": "inline-block"}),

                html.Div(style={"height": "0.5rem"}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                *[html.Button(f"{i}", id=f"btn_{i}_match") for i in range(1, 6)]
                            ]),
                            html.Div([
                                *[html.Button(f"{i}", id=f"btn_{i}_match") for i in range(6, 11)]
                            ]),
                            html.Div([
                                *[html.Button(f"{i}", id=f"btn_{i}_match") for i in range(11, 16)]
                            ]),
                            html.Div([
                                *[html.Button(f"{i}", id=f"btn_{i}_match") for i in range(16, 21)]                        
                            ]),
                            html.Div([
                                html.Button("25", id="btn_25_match"),
                                html.Button("Bull", id="btn_bull_match"),
                                html.Button("Miss", id="btn_miss_match"),
                            ]),
                            html.Div([
                                html.Button("Double", id="btn_double_match", className="green_button", style={"width": "7.05rem"}),
                                html.Button("Treble", id="btn_treble_match", className="green_button", style={"width": "7.05rem"}),
                                html.Button("⬅", id="btn_backspace_match", className="backspace_button"),
                                html.Button("\u2714", id="btn_confirm_match", disabled=True, className="green_button")
                            ])
                        ], id="button_display"),

                        # NUMPAD INPUT MODE
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div(".", style={"width": "4.95rem", "display": "inline-block"}),
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad") for i in range(1, 4)]
                                ]),
                                html.Div([
                                    html.Div(".", style={"width": "4.95rem", "display": "inline-block"}),
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad") for i in range(4, 7)]
                                ]),
                                html.Div([
                                    html.Div(".", style={"width": "4.95rem", "display": "inline-block"}),
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad") for i in range(7, 10)]
                                ]),
                                html.Div([
                                    html.Div(".", style={"width": "4.95rem", "display": "inline-block"}),
                                    html.Button("0", id=f"btn_0_numpad"),
                                    html.Button("⬅", id="btn_backspace_numpad", className="backspace_button"),
                                    html.Button("\u2714", id="btn_confirm_numpad", disabled=True, className="green_button")
                                ]),
                            ], id="numpad_background", style={"background-color": "#161d2a"}),
                        ], id="numpad_display", style={"display": "none"}),
                    ])
                ]),
            ], id="game_screen", style={"display": "none"})  
        ])

### CALLBACKS
# init screen
@callback(
    Output("start_score", "children"),
    Input("btn_1_match", "n_clicks"),
    State("p1_score", "children")
)
def store_start_score(n, score):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger == ".":
        return score
    return nop

@callback(
    Output("btn_choose_p1", "className"),
    Output("btn_choose_p2", "className"),
    Input("btn_choose_p1", "n_clicks"),
    Input("btn_choose_p2", "n_clicks"),
    prevent_initial_call=True
)
def change_btn_style(n_p1, n_p2):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if '1' in trigger:
        return "green_button", "backspace_button"
    return "backspace_button", "green_button"

@callback(
    Output("init_choice_text", "children"),
    Input("btn_choose_p1", "n_clicks"),
    Input("btn_choose_p2", "n_clicks"),
    prevent_initial_call=True
)
def change_choice_text(n_p1, n_p2):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if '1' in trigger:
        return "Player 1 starts"
    return "Player 2 starts"

@callback(
    Output("player_started_store", "children"),
    Input("btn_confirm_init", "n_clicks"),
    State("init_choice_text", "children"),
    prevent_initial_call=True
)
def init_player_started_value(n, choice):
    if '1' in choice:
        return '1'
    return '2'

@callback(
    Output("p1_name", "style"),
    Output("p2_name", "style"),
    Output("p1_score", "style"),
    Output("p2_score", "style"),
    Output("p1_avg_text", "style"),
    Output("p1_avg_value", "style"),
    Output("p2_avg_text", "style"),
    Output("p2_avg_value", "style"),
    Output("game_screen", "style"),
    Output("init_screen", "style"),
    Input("player_started_store", "children"),
    Input("btn_confirm_match", "n_clicks"),
    Input("btn_confirm_numpad", "n_clicks"),
    State("p1_name", "style"),
    prevent_initial_call=True
)
def init_screen_and_player(player_started, n_match, n_numpad, p1_name_style):
    name_style = {"font-size": "2rem", "color": "white", "display": "inline-block"}
    score_style = {"font-size": "2rem", "color": "white", "display": "inline-block"}
    avg_style = {"font-size": "1rem", "color": "white", "display": "inline-block"}

    name_style_grey = {"font-size": "2rem", "color": "#666666", "display": "inline-block"}
    score_style_grey = {"font-size": "2rem", "color": "#666666", "display": "inline-block"}
    avg_style_grey = {"font-size": "1rem", "color": "#666666", "display": "inline-block"}

    # use this block of code to switch between player focus after entering three darts
    trigger = dash.callback_context.triggered[0]['prop_id']
    if 'confirm' in trigger:
        player_started = '1'
        if p1_name_style['color'] == "white":
            player_started = '2'

    if player_started == '1':
        return name_style, name_style_grey, score_style, score_style_grey, avg_style, avg_style, avg_style_grey, avg_style_grey, {}, {"display": "none"}
    return name_style_grey, name_style, score_style_grey, score_style, avg_style_grey, avg_style_grey, avg_style, avg_style, {}, {"display": "none"}

# main game
@callback(
    *[Output(f"btn_{i}_match", "children") for i in range(1, 21)],
    Input("btn_1_match", "children"),
    Input("btn_double_match", "n_clicks"),
    Input("btn_treble_match", "n_clicks"),
    *[Input(f"btn_{i}_match", "n_clicks") for i in range(1, 21)],
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
    Output("dart_1_match", "children"),
    Output("dart_2_match", "children"),
    Output("dart_3_match", "children"),
    *[Input(f"btn_{i}_match", "n_clicks") for i in range(1, 21)],
    Input("btn_25_match", "n_clicks"),
    Input("btn_bull_match", "n_clicks"),
    Input("btn_miss_match", "n_clicks"),
    *[State(f"btn_{i}_match", "children") for i in range(1, 21)],
    State("dart_1_match", "children"),
    State("dart_2_match", "children"),
    State("dart_3_match", "children"),
    prevent_initial_call=True
)
def record_thrown_dart(*args):
    d1, d2, d3 = args[-3:]
    if d3 != "_____":
        return nop, nop, nop
    trigger = dash.callback_context.triggered[0]['prop_id']
    btn_names = args[23:-3]
    
    value = trigger.split("btn_")[1].split(".n_clicks")[0]
    return record_dart_in_correct_place(value, btn_names, d1, d2)
    
@callback(
    Output("dart_1_match", "children", allow_duplicate=True),
    Output("dart_2_match", "children", allow_duplicate=True),
    Output("dart_3_match", "children", allow_duplicate=True),
    Input("btn_confirm_match", "n_clicks"),
    State("dart_1_match", "children"),
    State("dart_2_match", "children"),
    State("dart_3_match", "children"),
    prevent_initial_call=True
)
def record_all_3_darts(n_confirm, d1, d2, d3):
    return "_____", "_____", "_____"

@callback(
    Output("dart_1_match", "children", allow_duplicate=True),
    Output("dart_2_match", "children", allow_duplicate=True),
    Output("dart_3_match", "children", allow_duplicate=True),
    Input("btn_backspace_match", "n_clicks"),
    State("dart_1_match", "children"),
    State("dart_2_match", "children"),
    State("dart_3_match", "children"),
    prevent_initial_call=True
)
def delete_dart_input(n_backspace, d1, d2, d3):
    if d3 != "_____":
        return nop, nop, "_____"
    if d2 != "_____":
        return nop, "_____", "_____"
    return "_____", "_____", "_____"

@callback(
    Output("btn_confirm_match", "disabled"),
    Input("dart_3_match", "children"),
    State("dart_1_match", "children"),
    State("dart_2_match", "children"),
    prevent_initial_call=True
)
def enable_confirm_btn(dart_3, dart_1, dart_2):
    return dart_3 == "_____"

@callback(
    Output("p1_score", "children"),
    Output("p2_score", "children"),
    Output("player_started_store", "children", allow_duplicate=True),
    Input("btn_confirm_match", "n_clicks"),
    State("dart_1_match", "children"),
    State("dart_2_match", "children"),
    State("dart_3_match", "children"),
    State("p1_name", "style"),
    State("p1_score", "children"),
    State("p2_score", "children"),
    State("player_started_store", "children"),
    State("start_score", "children"),
    prevent_initial_call=True
)
def subtract_score(n_confirm, d1, d2, d3, p1_name_style, p1_score, p2_score, player_started, start_score):
    darts = [d1, d2, d3]
    new_darts = []
    for i, dart in enumerate(darts):
        if dart == "Bull":
            new_darts.append(50)
        elif 'T' in dart:
            new_darts.append(3 * int(dart.split("T")[1]))
        elif 'D' in dart:
            new_darts.append(2 * int(dart.split("D")[1]))
        else:
            new_darts.append(int(dart))

    next_to_start = '1'
    if player_started == '1':
        next_to_start = '2'

    total = sum(new_darts)
    if p1_name_style['color'] == "white":
        for i, dart in enumerate(darts):
            if "D" in dart:
                total_thrown_inc_dbl = 2 * int(dart.split("D")[1]) + new_darts[i - 1] + new_darts[i - 2]
                if total_thrown_inc_dbl == int(p1_score):
                    return start_score, start_score, next_to_start

        new_p1_score = str(int(p1_score) - total) if total < int(p1_score) - 1 else p1_score
        new_p2_score = p2_score
    else:
        for i, dart in enumerate(darts):
            if "D" in dart:
                total_thrown_inc_dbl = 2 * int(dart.split("D")[1]) + new_darts[i - 1] + new_darts[i - 2]
                if total_thrown_inc_dbl == int(p2_score):
                    return start_score, start_score, next_to_start
        new_p1_score = p1_score
        new_p2_score = str(int(p2_score) - total) if total < int(p2_score) - 1 else p2_score
    
    return new_p1_score, new_p2_score, nop

### NUMPAD CALLBACKS
@callback(
    Output("numpad_display", "style"),
    Output("button_display", "style"),
    Output("numpad_view", "style"),
    Output("darts_view", "style"),
    Input("numpad_toggle", "value")
)
def toggle_input_mode(toggled):
    darts_record_style = {"border": "2px solid #fff", "width": "16rem", "display": "inline-block"}
    if toggled:
        return {}, {"display": "none"}, darts_record_style, {'display': 'none'}
    return {"display": "none"}, {}, {"display": "none"}, darts_record_style

@callback(
    Output("numpad_score", "children"),
    Output("btn_confirm_numpad", "disabled"),
    *[Input(f"btn_{i}_numpad", "n_clicks") for i in range(0, 10)],
    Input("p1_name", "style"),
    Input("p2_name", "style"),
    Input("btn_backspace_numpad", "n_clicks"),
    State("numpad_score", "children"),
    prevent_initial_call=True
)
def record_score(*args):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if 'name' in trigger:
        return "_____", True
    
    if "backspace" in trigger and args[-1] != "_____":
        score = args[-1][:-1]
        if len(score) == 0:
            return "_____", True
        return score, False
    elif "backspace" in trigger and args[-1] == "_____":
        return nop, True
       
    value = trigger.split("btn_")[1].split("_numpad")[0]
    score = args[-1] + value
    if args[-1] == "_____":
        return value, False
    if len(score) > 3:
        return score[:-1], False
    return score, False

@callback(
    Output("numpad_score", "children", allow_duplicate=True),
    Output("p1_score", "children", allow_duplicate=True),
    Output("p2_score", "children", allow_duplicate=True),
    Output("player_started_store", "children", allow_duplicate=True),
    Input("btn_confirm_numpad", "n_clicks"),
    State("p1_name", "style"),
    State("p1_score", "children"),
    State("p2_score", "children"),
    State("numpad_score", "children"),
    State("player_started_store", "children"),
    State("start_score", "children"),
    prevent_initial_call=True
)
def numpad_subtract_score(n, p1_name_style, p1_score, p2_score, numpad_score, player_started, start_score):
    next_to_start = '1'
    if player_started == '1':
        next_to_start = '2'

    numpad_score = int(numpad_score)
    if p1_name_style['color'] == "white":
        if numpad_score == int(p1_score) and int(p1_score) <= 170:
            return "_____", start_score, start_score, next_to_start

        new_p1_score = str(int(p1_score) - numpad_score) if numpad_score < int(p1_score) - 1 else p1_score
        new_p2_score = p2_score
    else:
        if numpad_score == int(p1_score) and int(p1_score) <= 170:
            return "_____", start_score, start_score, next_to_start

        new_p1_score = p1_score
        new_p2_score = str(int(p2_score) - numpad_score) if numpad_score < int(p2_score) - 1 else p2_score
    
    return "_____", new_p1_score, new_p2_score, nop

# @callback(
    
#     Input("numpad_toggle", "value"),
#     prevent_initial_call=True
# )
# def toggle_darts_view_style(toggled):
#     div_style = {"border": "2px solid #fff", "width": "16rem", "display": "inline-block"}
#     div_style_grey = {"border": "2px solid #444", "width": "16rem", "display": "inline-block"}
#     heading_style = {"color": "white", "display": "inline-block"}
#     heading_style_grey = {"color": "#444", "display": "inline-block"}
#     if toggled:
#         return div_style_grey, *(heading_style_grey,)*4
#     return div_style, *(heading_style,)*4

# @callback(
#     Output("3_dart_avg_current", "children"),
#     Output("n_visits", "children"),
#     Input("btn_confirm", "n_clicks"),
#     State("3_dart_avg_current", "children"),
#     State("n_visits", "children"),
#     State("dart_1", "children"),
#     State("dart_2", "children"),
#     State("dart_3", "children"),
#     prevent_initial_call=True
# )
# def record_3_dart_avg(n_confirm, curr_avg, n_visits, dart_1, dart_2, dart_3):
#     dart_1 = convert_score(dart_1)
#     dart_2 = convert_score(dart_2)
#     dart_3 = convert_score(dart_3)

#     curr_avg = 0 if curr_avg == "_____" else int(curr_avg)
#     n_visits = int(n_visits)
#     new_avg = float("%.2f" % (((n_visits * curr_avg) + (dart_1 + dart_2 + dart_3)) / (n_visits + 1)))

#     return new_avg, str(n_visits + 1)

# @callback(
#     Output("3_dart_avg", "children", allow_duplicate=True),
#     Input("btn_confirm", "n_clicks"),
#     State("dart_1", "children"),
#     State("dart_2", "children"),
#     State("dart_3", "children"),
#     State("title", "children"),
#     prevent_initial_call=True
# )
# def record_3_dart_avg_all_time(n_confirm, dart_1, dart_2, dart_3, title):
#     target = titles_rev[title]
#     dart_1 = convert_score(dart_1)
#     dart_2 = convert_score(dart_2)
#     dart_3 = convert_score(dart_3)

#     n_visits = read_3_dart_avg(target, avg=False)
#     curr_avg = read_3_dart_avg(target)
#     new_avg = (((n_visits * curr_avg) + (dart_1 + dart_2 + dart_3)) / (n_visits + 1))
#     new_avg_2dp = float("%.2f" % new_avg)

#     update_3_dart_avg_file(n_visits + 1, new_avg, target)

#     return new_avg_2dp
