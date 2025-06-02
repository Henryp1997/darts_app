import dash
from dash import html, callback
from dash import no_update as nop
from dash.dependencies import Output, Input, State
import pandas as pd

# App imports
import utils
import common_elems as elems
from common_elems import v_spacer
from consts import DATA_PATH, ARROW_LEFT, TICK, HIDE, ID_VALUE_MAP

dash.register_page(__name__)

titles = {
    "t20": "Treble 20 Practice",
    "t19": "Treble 19 Practice",
}

titles_rev = {
    "Treble 20 Practice": "t20",
    "Treble 19 Practice": "t19",
}

def layout(target=None):
    if target not in ("t20", "t19"):
        return html.Div("404", style={"color": "white", "font-size": "2rem"})
    return html.Div([
            html.Div(f"{titles[target]}", id="title", className="page_title_div"),
            html.Div("0", id="n_visits", style=HIDE),
            html.Div("0", id="running_total", style=HIDE),
            html.Div("0", id="n_visits_alltime", style=HIDE),
            html.Div("0", id="all_time_total", style=HIDE),
            html.Div(id="recalculate_avgs", style=HIDE),
            v_spacer("2vh"),
            
            # Main game window
            html.Div([
                elems.get_darts_hit_bar(page="practice"),
                v_spacer("1vh"),
                html.Div([
                    v_spacer("1vh"),
                    elems.padded_text_white("3-dart average (current session):", margin_right="7.3vw"),
                    html.Div("_____", id="3_dart_avg_current", className="white_text_inline"),
                    v_spacer("1vh"),
                ], style={"border": "2px solid #fff"}),
                v_spacer("1vh"),
                html.Div([
                    v_spacer("1vh"),
                    elems.padded_text_white("3-dart average (all time):", margin_right="21.3vw"),
                    html.Div("_____", id="3_dart_avg", className="white_text_inline"),
                    v_spacer("1vh"),
                ], style={"border": "2px solid #fff"}),
                v_spacer("1vh"),

                # All buttons
                html.Div([
                    html.Div([
                        html.Div([
                            *[html.Button(f"{i}", id=f"btn_{i}") for i in range(1, 6)]
                        ], className="btn_container"),
                        v_spacer("0.75vh"),
                        html.Div([
                            *[html.Button(f"{i}", id=f"btn_{i}") for i in range(6, 11)]
                        ], className="btn_container"),
                        v_spacer("0.75vh"),
                        html.Div([
                            *[html.Button(f"{i}", id=f"btn_{i}") for i in range(11, 16)]
                        ], className="btn_container"),
                        v_spacer("0.75vh"),
                        html.Div([
                            *[html.Button(f"{i}", id=f"btn_{i}") for i in range(16, 21)]                   
                        ], className="btn_container"),
                        v_spacer("0.75vh"),
                        html.Div([
                            html.Button("25", id="btn_25"),
                            html.Button("Bull", id="btn_bull"),
                            html.Button("Miss", id="btn_miss"),
                            html.Button("Delete last score", id="btn_del_last", className="del_last_score_btn")
                        ], className="btn_container"),
                        v_spacer("0.75vh"),
                        html.Div([
                            html.Button("Double", id="btn_double", className="green_button", style={"width": "27vw"}),
                            html.Button("Treble", id="btn_treble", className="green_button", style={"width": "27vw"}),
                            html.Button(ARROW_LEFT, id="btn_backspace", className="backspace_button"),
                            html.Button(TICK, id="btn_confirm", disabled=True, className="green_button")
                        ], className="btn_container"),
                    ])
                ]),

            ], id="main_game_window"),

            # delete last score window
            html.Div(style={"height": "6vh"}),
            html.Div([
                html.Div([
                    v_spacer("2vh"),
                    html.Div("Delete last score saved in the database?"),
                    v_spacer("2vh"),
                    html.Div([
                            html.Button("NO", id="btn_del_last_NO", className="backspace_button", style={"width": "30vw"}),
                            html.Button("YES", id="btn_del_last_YES", className="green_button", style={"width": "30vw"}),
                        ], className="btn_container centered"),
                    v_spacer("2vh"),
                    ],
                    className="grey_window", style={"width": "80vw"}
                )
            ], id="del_last_score_window", style=HIDE)
        ])

### CALLBACKS
@callback(
    Output("3_dart_avg", "children"),
    Output("all_time_total", "children"),
    Output("n_visits_alltime", "children"),
    Input("btn_1", "children"),
    State("title", "children")
)
def init_avg_file(n, title):
    # Use title as an input but only trigger this callback once - on page load
    target = titles_rev[title]
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger == ".":
        try:
            df = pd.read_csv(f"{DATA_PATH}/{target}_practice.csv")
            return utils.initialise_3_dart_avg(df)
        except FileNotFoundError:
            # Init file if not found
            utils.create_3_dart_avg_file(DATA_PATH, target)
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
    
    if "double" in trigger or "treble" in trigger:
        return utils.convert_all_btns_to_dbl_tbl(
            btn_1_text, 
            d_or_t="D" if "double" in trigger else "T"
        )
      
    # Below code executed if one of the number buttons triggered this callback
    # This just returns the button texts to non double or treble
    return [f"{i}" for i in range(1, 21)]


@callback(
    Output("dart_1", "children"),
    Output("dart_2", "children"),
    Output("dart_3", "children"),

    *[Input(f"btn_{i}", "n_clicks") for i in range(1, 21)],
    Input("btn_25", "n_clicks"),
    Input("btn_bull", "n_clicks"),
    Input("btn_miss", "n_clicks"),

    State("btn_1", "children"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    prevent_initial_call=True
)
def record_thrown_dart(*args):
    btn_1_text = args[-4]
    d1, d2, d3 = args[-3:]
    trigger = dash.callback_context.triggered[0]['prop_id']
    id = trigger.split(".n_clicks")[0]

    value = ID_VALUE_MAP[id]
    if id not in ("btn_25", "btn_bull", "btn_miss"):
        if "D" in btn_1_text: value = f"D{value}"
        if "T" in btn_1_text: value = f"T{value}"
    return utils.record_dart_in_correct_place(d1, d2, d3, value)


@callback(
    Output("dart_1", "children", allow_duplicate=True),
    Output("dart_2", "children", allow_duplicate=True),
    Output("dart_3", "children", allow_duplicate=True),
    Output("running_total", "children", allow_duplicate=True),
    Input("btn_confirm", "n_clicks"),
    State("dart_1", "children"),
    State("dart_2", "children"),
    State("dart_3", "children"),
    State("running_total", "children"),
    State("title", "children"),
    prevent_initial_call=True
)
def record_all_3_darts(_, d1, d2, d3, running_total, title):
    total = utils.calculate_total(d1, d2, d3)
    utils.write_darts_to_file(d1, d2, d3, target=titles_rev[title])
    return "_____", "_____", "_____", str(int(running_total) + total)


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
    return utils.clear_last_dart(d1, d2, d3)


@callback(
    Output("btn_confirm", "disabled"),
    Input("dart_3", "children"),
    prevent_initial_call=True
)
def enable_confirm_btn(dart_3):
    return dart_3 == "_____"
    

@callback(
    Output("3_dart_avg", "children", allow_duplicate=True),
    Output("3_dart_avg_current", "children", allow_duplicate=True),
    Output("n_visits", "children", allow_duplicate=True),
    Output("recalculate_avgs", "children", allow_duplicate=True),

    Input("running_total", "children"),

    State("recalculate_avgs", "children"),
    State("all_time_total", "children"),
    State("n_visits", "children"),
    State("n_visits_alltime", "children"),
    prevent_initial_call=True
)
def record_3_dart_avg(running_total, recalc_avgs, alltime_total, n_visits_current, n_visits_all):
    n_visits_return = str(int(n_visits_current) + 1)
    just_deleted = False
    if recalc_avgs == "yes":
        n_visits_return = nop
        just_deleted = True

    # Calculate current session average
    new_curr_avg = utils.calc_session_3_dart_avg(n_visits_current, running_total, just_deleted)
    new_curr_avg = f"{new_curr_avg:.2f}"

    # Calculate all time average
    new_alltime_avg = utils.calc_alltime_3_dart_avg(n_visits_current, n_visits_all, running_total, alltime_total, just_deleted)
    new_alltime_avg = f"{new_alltime_avg:.2f}"
    
    return new_alltime_avg, new_curr_avg, n_visits_return, "no"


@callback(
    Output("del_last_score_window", "style"),
    Output("main_game_window", "style"),
    Output("n_visits_alltime", "children", allow_duplicate=True),
    Output("all_time_total", "children", allow_duplicate=True),
    Output("n_visits", "children", allow_duplicate=True),
    Output("running_total", "children", allow_duplicate=True),
    Output("recalculate_avgs", "children"),

    Input("btn_del_last", "n_clicks"),
    Input("btn_del_last_NO", "n_clicks"),
    Input("btn_del_last_YES", "n_clicks"),
    
    State("n_visits", "children"),
    State("n_visits_alltime", "children"),
    State("running_total", "children"),
    State("all_time_total", "children"),
    State("title", "children"),
    prevent_initial_call=True
)
def open_delete_score_window(n1, n2, n3, n_visits, n_visits_all, running_total, alltime_total, title):
    trigger = dash.callback_context.triggered[0]["prop_id"]
    if "NO" in trigger:
        return HIDE, {}, *((nop,)*4), "no"
    
    if "YES" in trigger:
        last_score = int(utils.delete_last_entry_in_file(target=titles_rev[title]))
        if int(n_visits) == 0:
            n_visits_all = str(int(n_visits_all) - 1)
            alltime_total = str(int(alltime_total) - last_score)
            return HIDE, {}, n_visits_all, alltime_total, "0", "0", "yes"

        n_visits = str(int(n_visits) - 1)
        running_total = str(int(running_total) - last_score)
        return HIDE, {}, nop, nop, n_visits, running_total, "yes"

    return {"display": "flex", "justify-content": "center"}, HIDE, *((nop,)*4), "no"
