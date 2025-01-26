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
            html.Div("0", id="n_visits_p1", style={"display": "none"}),
            html.Div("0", id="n_visits_p2", style={"display": "none"}),
            html.Div("0", id="running_total_p1", style={"display": "none"}),
            html.Div("0", id="running_total_p2", style={"display": "none"}),
            html.Div("0", id="3_dart_avg_p1", style={"display": "none"}),
            html.Div("0", id="3_dart_avg_p2", style={"display": "none"}),
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
                        html.Button("Player 1", id="btn_choose_p1", className="green_button", style={"width": "30%", "margin-right": "5%"}),
                        html.Button("Player 2", id="btn_choose_p2", className="backspace_button", style={"width": "30%"}),
                    ], style={"text-align": "center"}),
                    html.Div(style={"height": "1rem"}),
                    html.Div([
                        html.Div("Player 1 starts", id="init_choice_text", style={"display": "inline-block", "margin-right": "5%"}),
                        html.Button("\u2714", id="btn_confirm_init"),
                    ], style={"text-align": "center"}),
                    html.Div(style={"height": "1rem"}),
                ], style={"color": "white", "border": "2px solid white"}),
            ], id="init_screen"),

            html.Div([
                html.Div([
                    html.Div(style={"height": "0.5rem"}),
                    html.Div(".", className="black_text_inline_spacer", style={"width": "2.2rem"}),
                    html.Div("Player 1", id="p1_name", className="white_text_inline", style={"font-size": "2rem"}),
                    html.Div(".", className="black_text_inline_spacer", style={"width": "4.4rem"}),
                    html.Div("Player 2", id="p2_name", className="grey_#aaa_text_inline", style={"font-size": "2rem"}),
                    html.Div(style={"height": "0.5rem"}),
                ], style={"border": "2px solid #fff", "border-bottom": "none"}),

                html.Div([
                    html.Div(style={"height": "0.2rem"}),
                    html.Div(".", className="black_text_inline_spacer", style={"margin-right": "4rem"}),
                    html.Div(f"{start}", id="p1_score", className="white_text_inline", style={"font-size": "2rem"}),
                    html.Div(".", className="black_text_inline_spacer", style={"margin-right": "8.5rem"}),
                    html.Div(f"{start}", id="p2_score", className="grey_#aaa_text_inline", style={"font-size": "2rem"}),
                    html.Div(style={"height": "0.5rem"}),
                ], style={"border": "2px solid #fff", "border-top": "none", "border-bottom": "none"}),

                html.Div([
                    html.Div(style={"height": "0.2rem"}),
                    html.Div(".", className="black_text_inline_spacer", style={"margin-right": "1rem"}),
                    html.Div("Avg. =", id="p1_avg_text", className="white_text_inline", style={"font-size": "1rem"}),
                    html.Div(".", className="black_text_inline_spacer", style={"margin-right": "0.5rem"}),
                    html.Div("_____", id="p1_avg_value", className="white_text_inline", style={"font-size": "1rem"}),
                    html.Div(".", className="black_text_inline_spacer", style={"margin-right": "6rem"}),
                    html.Div("Avg. =", id="p2_avg_text", className="grey_#aaa_text_inline", style={"font-size": "1rem"}),
                    html.Div(".", className="black_text_inline_spacer", style={"margin-right": "0.5rem"}),   
                    html.Div("_____", id="p2_avg_value", className="grey_#aaa_text_inline", style={"font-size": "1rem"}),
                    html.Div(style={"height": "0.5rem"}),
                ], style={"border": "2px solid #fff", "border-top": "none"}),

                html.Div(style={"height": "0.5rem"}),
                
                html.Div([
                    html.Div(style={"height": "0.5rem"}),
                    html.Div("..", className="black_text_inline_spacer"),
                    html.Div("Score:", className="white_text_inline"),
                    html.Div("......................", className="black_text_inline_spacer"),
                    html.Div("_____", id="numpad_score", className="white_text_inline"),
                    html.Div(style={"height": "0.5rem"}),
                ], id="numpad_view", style={"border": "2px solid #fff", "width": "16rem", "display": "inline-block"}),

                html.Div(style={"height": "0.5rem"}),
                html.Div([
                    html.Div([
                        # NUMPAD INPUT MODE
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div(".", className="numpad_button_spacer"),
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad", className="numpad_button") for i in range(1, 4)]
                                ]),
                                html.Div([
                                    html.Div(".", className="numpad_button_spacer"),
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad", className="numpad_button") for i in range(4, 7)]
                                ]),
                                html.Div([
                                    html.Div(".", className="numpad_button_spacer"),
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad", className="numpad_button") for i in range(7, 10)]
                                ]),
                                html.Div([
                                    html.Div(".", className="numpad_button_spacer"),
                                    html.Button("0", id=f"btn_0_numpad", className="numpad_button"),
                                    html.Button("⬅", id="btn_backspace_numpad", className="backspace_button", style={"width": "25%"}),
                                    html.Button("\u2714", id="btn_confirm_numpad", disabled=True, className="green_button", style={"width": "25%"})
                                ]),
                            ], id="numpad_background", className="numpad_background"),
                        ], id="numpad_display"),
                    ])
                ]),
            ], id="game_screen", style={"display": "none"}),

            # CONFIRM DOUBLE CHECKOUT DIV
            html.Div(style={"height": "5rem"}),
            html.Div([
                html.Div([
                    html.Div("Checkout! Correctly finished on double?"),
                    html.Div([
                            html.Button("NO", id="checkout_double_NO", className="backspace_button"),
                            html.Div(".", style={"color": "#444444", "width": "7.5%", "display": "inline-block"}),
                            html.Button("YES", id="checkout_double_YES", className="green_button"),
                            html.Div(style={"height": "0.5rem"}),
                        ])
                    ],
                    className="checkout_box"
                )
            ], id="checkout_double_div", style={"display": "none"}),

            # SCORE TOO HIGH POPUP DIV
            html.Div(style={"height": "5rem"}),
            html.Div([
                html.Div([
                    html.Div("Score not possible!"),
                    html.Div([
                            html.Button("OK", id="score_too_high_OK", className="green_button"),
                            html.Div(style={"height": "0.5rem"}),
                        ])
                    ],
                    className="checkout_box"
                )
            ], id="score_too_high_div", style={"display": "none"})
        ])

### CALLBACKS
# init screen
@callback(
    Output("start_score", "children"),
    Input("btn_0_numpad", "n_clicks"), # need to use an input object
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
    Output("p1_name", "className"),
    Output("p1_score", "className"),
    Output("p1_avg_text", "className"),
    Output("p1_avg_value", "className"),
    
    Output("p2_name", "className"),
    Output("p2_score", "className"),
    Output("p2_avg_text", "className"),
    Output("p2_avg_value", "className"),

    Output("game_screen", "style"),
    Output("init_screen", "style"),
    Input("player_started_store", "children"),
    Input("btn_confirm_numpad", "n_clicks"),
    State("p1_name", "className"),
    State("numpad_score", "children"),
    prevent_initial_call=True
)
def init_screen_and_player(player_started, n_numpad, p1_name_class, numpad_score):
    # use this block of code to switch between player focus after entering three darts
    trigger = dash.callback_context.triggered[0]['prop_id']
    if 'confirm' in trigger:
        if int(numpad_score) > 180:
            return ((nop,)*10)
        player_started = '1'
        if p1_name_class == "white_text_inline":
            player_started = '2'

    if player_started == '1':
        return *(("white_text_inline",)*4), *(("grey_aaa_text_inline",)*4), {}, {"display": "none"}
    return *(("grey_aaa_text_inline",)*4), *(("white_text_inline",)*4), {}, {"display": "none"}

### MAIN GAME
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
    Output("3_dart_avg_p1", "children"),
    Output("n_visits_p1", "children"),
    Output("3_dart_avg_p2", "children"),
    Output("n_visits_p2", "children"),
    Output("p1_score", "children", allow_duplicate=True),
    Output("p2_score", "children", allow_duplicate=True),
    Output("player_started_store", "children", allow_duplicate=True),
    Output("numpad_score", "children", allow_duplicate=True),

    Output("checkout_double_div", "style", allow_duplicate=True),
    Output("score_too_high_div", "style", allow_duplicate=True),
    Output("game_screen", "style", allow_duplicate=True),
    
    Input("btn_confirm_numpad", "n_clicks"),

    State("p1_name", "className"),
    State("p1_score", "children"),
    State("p2_score", "children"),
    State("numpad_score", "children"),
    prevent_initial_call=True
)
def numpad_subtract_score(n, p1_name_class, p1_score, p2_score, numpad_score):
    numpad_score = int(numpad_score)
    if p1_name_class == "white_text_inline":
        if verify_checkout_numpad(int(numpad_score), int(p1_score)):
            return *((nop,)*8), {}, {'display': 'none'}, {'display': 'none'}
        
        if int(numpad_score) > 180:
            return *((nop,)*7), "_____", {'display': 'none'}, {}, {'display': 'none'}

        new_p1_score = calc_remaining_score_numpad(int(p1_score), int(numpad_score))
        new_p2_score = p2_score
    else:
        if verify_checkout_numpad(int(numpad_score), int(p2_score)):
            return *((nop,)*8), {}, {'display': 'none'}, {'display': 'none'}
        
        if int(numpad_score) > 180:
            return *((nop,)*7), "_____", {'display': 'none'}, {}, {'display': 'none'}
        
        new_p1_score = p1_score
        new_p2_score = calc_remaining_score_numpad(int(p2_score), int(numpad_score))

    return nop, nop, nop, nop, "_____", new_p1_score, new_p2_score, nop, {'display': 'none'}, {'display': 'none'}, {}

@callback(
    Output("numpad_score", "children", allow_duplicate=True),
    Output("p1_score", "children", allow_duplicate=True),
    Output("p2_score", "children", allow_duplicate=True),
    Output("player_started_store", "children", allow_duplicate=True),
    Output("checkout_double_div", "style", allow_duplicate=True),
    Output("game_screen", "style", allow_duplicate=True),

    Input("checkout_double_NO", "n_clicks"),
    Input("checkout_double_YES", "n_clicks"),

    State("player_started_store", "children"),
    State("start_score", "children"),
    prevent_initial_call=True
)
def open_double_check_div(n_NO, n_YES, player_started, start_score):
    trigger = dash.callback_context.triggered[0]['prop_id']
    next_to_start = '1'
    if player_started == '1':
        next_to_start = '2'

    # check if player 1 did finish on a double by asking the user
    if 'NO' in trigger:
        return "_____", nop, nop, nop, {'display': 'none'}, {}
    
    # YES was pressed
    return "_____", start_score, start_score, next_to_start, {'display': 'none'}, {}

@callback(
    Output("score_too_high_div", "style", allow_duplicate=True),
    Output("game_screen", "style", allow_duplicate=True),
    Input("score_too_high_OK", "n_clicks"),
    prevent_initial_call=True
)
def open_double_check_div(n_OK):   
    return {'display': 'none'}, {}