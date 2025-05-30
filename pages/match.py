import dash
from dash import html, callback
from dash import no_update as nop
from dash.dependencies import Output, Input, State

# App specific imports
import utils
import common_elems as elems
from common_elems import v_spacer
from consts import ARROW_LEFT, TICK, HIDE

dash.register_page(__name__)

def layout(start=None):
    if start not in ("301", "501"):
        return html.Div("404", style={"color": "white", "font-size": "2rem"})
    return html.Div([
            html.Div("0", id="n_visits_p1", style=HIDE),
            html.Div("0", id="n_visits_p2", style=HIDE),
            html.Div("0", id="running_total_p1", style=HIDE),
            html.Div("0", id="running_total_p2", style=HIDE),
            html.Div("0", id="3_dart_avg_p1", style=HIDE),
            html.Div("0", id="3_dart_avg_p2", style=HIDE),
            html.Div(id="player_started_store", style=HIDE),
            html.Div(id="start_score", style=HIDE),

            # Initialisation div
            html.Div([
                v_spacer("15vh"),
                html.Div([
                    v_spacer("1.5vh"),
                    html.Div("Choose player to start", style={"font-size": "1.5rem", "text-align": "center"}),
                    v_spacer("1.5vh"),
                    html.Div([
                        html.Button("Player 1", id="btn_choose_p1", className="green_button", style={"width": "30vw", "margin-right": "5%"}),
                        html.Button("Player 2", id="btn_choose_p2", className="backspace_button", style={"width": "30vw"}),
                    ], className="btn_container centered"),
                    v_spacer("1.5vh"),
                    html.Div([
                        html.Div("Player 1 starts?", id="init_choice_text", style={"display": "inline-block", "font-size": "1.5rem", "margin-right": "5%"}),
                        html.Button(TICK, id="btn_confirm_init"),
                    ], className="btn_container centered"),
                    v_spacer("1.5vh"),
                ], style={"color": "white", "border": "2px solid white"}),
            ], id="init_screen"),

            html.Div([
                html.Div([
                    html.Div([
                        v_spacer("1vh"),
                        html.Div(".", className="black_text_inline_spacer", style={"width": "2.2rem"}),
                        html.Div("Player 1", id="p1_name", className="white_text_inline", style={"font-size": "2rem"}),
                        html.Div(".", className="black_text_inline_spacer", style={"width": "4.4rem"}),
                        html.Div("Player 2", id="p2_name", className="grey_#aaa_text_inline", style={"font-size": "2rem"}),
                        v_spacer("1vh"),
                    ]),

                    html.Div([
                        html.Div(style={"height": "0.2rem"}),
                        html.Div(".", className="black_text_inline_spacer", style={"margin-right": "4rem"}),
                        html.Div(f"{start}", id="p1_score", className="white_text_inline", style={"font-size": "2rem"}),
                        html.Div(".", className="black_text_inline_spacer", style={"margin-right": "8.5rem"}),
                        html.Div(f"{start}", id="p2_score", className="grey_#aaa_text_inline", style={"font-size": "2rem"}),
                        v_spacer("1vh"),
                    ]),

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
                        v_spacer("1vh"),
                    ]),
                ], className="boxed_div"),

                v_spacer("1vh"),
                
                html.Div([
                    v_spacer("1vh"),
                    html.Div("..", className="black_text_inline_spacer"),
                    elems.padded_text_white("Score:"),
                    html.Div(".", className="black_text_inline_spacer", style={"width": "25vw"}),
                    html.Div("_____", id="numpad_score", className="white_text_inline"),
                    v_spacer("1vh"),
                ], id="numpad_view", className="boxed_div"),

                v_spacer("1vh"),
                html.Div([
                    html.Div([
                        # NUMPAD INPUT MODE
                        html.Div([
                            html.Div([
                                v_spacer("1vh"),
                                html.Div([
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad", className="numpad_button") for i in range(1, 4)]
                                ], className="btn_container centered"),
                                v_spacer("1vh"),
                                html.Div([
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad", className="numpad_button") for i in range(4, 7)]
                                ], className="btn_container centered"),
                                v_spacer("1vh"),
                                html.Div([
                                    *[html.Button(f"{i}", id=f"btn_{i}_numpad", className="numpad_button") for i in range(7, 10)]
                                ], className="btn_container centered"),
                                v_spacer("1vh"),
                                html.Div([
                                    html.Button("0", id=f"btn_0_numpad", className="numpad_button"),
                                    html.Button(ARROW_LEFT, id="btn_backspace_numpad", className="backspace_button", style={"width": "25%"}),
                                    html.Button(TICK, id="btn_confirm_numpad", disabled=True, className="green_button", style={"width": "25%"})
                                ], className="btn_container centered"),
                                v_spacer("1vh"),
                            ], id="numpad_background", className="numpad_background"),
                        ], id="numpad_display"),
                    ])
                ]),
            ], id="game_screen", style=HIDE),

            # CONFIRM DOUBLE CHECKOUT DIV
            v_spacer("10vh"),
            html.Div([
                html.Div([
                    v_spacer("1vh"),
                    html.Div("Checkout! Correctly finished on double?"),
                    v_spacer("1vh"),
                    html.Div([
                            html.Button("NO", id="checkout_double_NO", className="backspace_button", style={"margin-right": "5vw"}),
                            html.Button("YES", id="checkout_double_YES", className="green_button"),
                            html.Div(style={"height": "0.5rem"}),
                        ], className="btn_container centered"),
                    v_spacer("1vh"),
                    ],
                    className="checkout_box"
                )
            ], id="checkout_double_div", style=HIDE),

            # SCORE TOO HIGH POPUP DIV
            v_spacer("10vh"),
            html.Div([
                html.Div([
                    v_spacer("1vh"),
                    html.Div("Score not possible!"),
                    v_spacer("1vh"),
                    html.Div([
                            html.Button("OK", id="score_too_high_OK", className="green_button", style={"width": "30vw"}),
                        ], className="btn_container centered"),
                    v_spacer("1vh")
                    ],
                    className="checkout_box"
                )
            ], id="score_too_high_div", style=HIDE)
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
    if "1" in trigger:
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
    i = 1 if "1" in trigger else 2
    return f"Player {i} starts?"


@callback(
    Output("player_started_store", "children"),
    Input("btn_confirm_init", "n_clicks"),
    State("init_choice_text", "children"),
    prevent_initial_call=True
)
def init_player_started_value(_, choice):
    return "1" in choice


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
        return *(("white_text_inline",)*4), *(("grey_aaa_text_inline",)*4), {}, HIDE
    return *(("grey_aaa_text_inline",)*4), *(("white_text_inline",)*4), {}, HIDE


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
        if utils.verify_checkout_numpad(int(numpad_score), int(p1_score)):
            return *((nop,)*8), {}, HIDE, HIDE
        
        if int(numpad_score) > 180:
            return *((nop,)*7), "_____", HIDE, {}, HIDE

        new_p1_score = utils.calc_remaining_score_numpad(int(p1_score), int(numpad_score))
        new_p2_score = p2_score
    else:
        if utils.verify_checkout_numpad(int(numpad_score), int(p2_score)):
            return *((nop,)*8), {}, HIDE, HIDE
        
        if int(numpad_score) > 180:
            return *((nop,)*7), "_____", HIDE, {}, HIDE
        
        new_p1_score = p1_score
        new_p2_score = utils.calc_remaining_score_numpad(int(p2_score), int(numpad_score))

    return *((nop,)*4), new_p1_score, new_p2_score, nop, "_____", nop, HIDE, {}


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
    next_to_start = "1"
    if player_started == "1":
        next_to_start = "2"

    # check if player 1 did finish on a double by asking the user
    if "NO" in trigger:
        return "_____", nop, nop, nop, HIDE, {}
    
    # YES was pressed
    return "_____", start_score, start_score, next_to_start, HIDE, {}


@callback(
    Output("score_too_high_div", "style", allow_duplicate=True),
    Output("game_screen", "style", allow_duplicate=True),
    Input("score_too_high_OK", "n_clicks"),
    prevent_initial_call=True
)
def open_double_check_div(n_OK):   
    return HIDE, {}