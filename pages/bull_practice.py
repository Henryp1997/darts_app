import dash
from dash import html, callback
from dash import no_update as nop
from dash.dependencies import Output, Input, State
import pandas as pd

# App specific imports
import utils
import common_elems as elems
from common_elems import v_spacer
from consts import(
    DATA_PATH,
    ARROW_LEFT,
    TICK,
    HIDE,
    BULL_STRS,
    ID_VALUE_MAP
)

dash.register_page(__name__)

def layout():
    return html.Div([
            html.Div("Bullseye Practice", className="page_title_div"),
            html.Div("0", id="n_visits_bp", style=HIDE),
            html.Div("0", id="length_dataframe", style=HIDE),
            v_spacer("2vh"),
            elems.get_darts_hit_bar(page="bull_practice"),
            v_spacer("1vh"),

            html.Div(
                [
                    html.Div([
                        html.Div([
                            v_spacer("1vh"),
                            elems.padded_text_white(text, margin_right=mr),
                            html.Div("_____", id=id, className="white_text_inline"),
                            v_spacer("1vh")
                        ], className="boxed_div"),
                        v_spacer("1vh")
                    ])
                    for text, mr, id in zip(
                        BULL_STRS,
                        ("7.2vw", "21.1vw", "9.2vw", "23.2vw"),
                        ("bull_hits_current", "bull_hits_all", "25_hits_current", "25_hits_all")
                    )
                ]
            ),

            # Score input section
            html.Div([
                html.Div([
                    v_spacer("1vh"),
                    html.Div("Scoring", style={"color": "white"}),
                    v_spacer("1vh"),
                    html.Div([
                        html.Button("25", id="btn_25_bp"),
                        html.Button("Bull", id="btn_bull_bp"),
                        html.Button("Miss", id="btn_miss_bp"),
                    ], className="btn_container"),
                    v_spacer("1.5vh"),
                    html.Div("Additional scoring options", style={"color": "white"}),
                    v_spacer("1vh"),
                    html.Div([
                        html.Button("Outer wire", id="btn_outer", style={"width": "9rem"}),
                        html.Button("Inner wire", id="btn_inner", style={"width": "9rem"}),
                    ], className="btn_container"),
                    v_spacer("1.5vh"),
                    html.Div([
                        html.Button(ARROW_LEFT, id="btn_backspace_bp", className="backspace_button"),
                        html.Button(TICK, id="btn_confirm_bp", disabled=True, className="green_button")
                    ], className="btn_container")
                ])
            ]),
        ])

### CALLBACKS
@callback(
    Output("bull_hits_all", "children"),
    Output("25_hits_all", "children"),
    Output("bull_hits_current", "children"),
    Output("25_hits_current", "children"),
    Output("length_dataframe", "children"),
    Input("btn_25_bp", "children"),
)
def init_bull_file(n):
    # use title as an input but only trigger this callback once - on page load
    trigger = dash.callback_context.triggered[0]['prop_id']
    if trigger == ".":
        try:
            df = pd.read_csv(f"{DATA_PATH}/bull_practice.csv")
            n_visits = len(df)
            n_thrown = n_visits * 3
            all_darts = list(df['Dart1']) + list(df['Dart2']) + list(df['Dart3'])
            all_darts = [str(i) for i in all_darts]
            n_bull = all_darts.count("Bull")
            n_25 = all_darts.count('25') + all_darts.count("25 (IW)")

            perc_bull = 0 if n_thrown == 0 else float("%.1f" % (100 * n_bull / n_thrown))
            perc_25 = 0 if n_thrown == 0 else float("%.1f" % (100 * n_25 / n_thrown))

            return f"{n_bull} / {n_thrown} ({perc_bull}%)", f"{n_25} / {n_thrown} ({perc_25}%)", "0 / 0 (0%)", "0 / 0 (0%)", str(n_visits)
        except FileNotFoundError:
            # init file if not found
            with open(f"{DATA_PATH}/bull_practice.csv", "w") as f:
                f.write("Timestamp,Dart1,Dart2,Dart3")
            f.close()
            return "_____", "_____", "_____", "_____", "0"    
    return nop


@callback(
    Output("dart_1_bp", "children"),
    Output("dart_2_bp", "children"),
    Output("dart_3_bp", "children"),
    Input("btn_25_bp", "n_clicks"),
    Input("btn_bull_bp", "n_clicks"),
    Input("btn_miss_bp", "n_clicks"),
    Input("btn_outer", "n_clicks"),
    Input("btn_inner", "n_clicks"),
    State("dart_1_bp", "children"),
    State("dart_2_bp", "children"),
    State("dart_3_bp", "children"),
    prevent_initial_call=True
)
def record_thrown_dart(n_25, n_bp, n_miss, n_outer, n_inner, d1, d2, d3):
    trigger = dash.callback_context.triggered[0]['prop_id']
    id = trigger.split(".n_clicks")[0]
    value = ID_VALUE_MAP[id]

    return utils.record_dart_in_correct_place(d1, d2, d3, value)


@callback(
    Output("dart_1_bp", "children", allow_duplicate=True),
    Output("dart_2_bp", "children", allow_duplicate=True),
    Output("dart_3_bp", "children", allow_duplicate=True),
    Input("btn_backspace_bp", "n_clicks"),
    State("dart_1_bp", "children"),
    State("dart_2_bp", "children"),
    State("dart_3_bp", "children"),
    prevent_initial_call=True
)
def delete_dart_input(n_backspace, d1, d2, d3):
    return utils.clear_last_dart(d1, d2, d3)


@callback(
    Output("btn_confirm_bp", "disabled"),
    Input("dart_3_bp", "children"),
    State("dart_1_bp", "children"),
    State("dart_2_bp", "children"),
    prevent_initial_call=True
)
def enable_confirm_btn(dart_3, dart_1, dart_2):
    return dart_3 == "_____"


@callback(
    Output("dart_1_bp", "children", allow_duplicate=True),
    Output("dart_2_bp", "children", allow_duplicate=True),
    Output("dart_3_bp", "children", allow_duplicate=True),
    Input("btn_confirm_bp", "n_clicks"),
    State("dart_1_bp", "children"),
    State("dart_2_bp", "children"),
    State("dart_3_bp", "children"),
    prevent_initial_call=True
)
def record_all_3_darts(n_confirm, d1, d2, d3):
    utils.write_darts_to_file(d1, d2, d3, target="bull")
    return "_____", "_____", "_____"


@callback(
    Output("n_visits_bp", "children"),
    Output("bull_hits_current", "children", allow_duplicate=True),
    Output("25_hits_current", "children", allow_duplicate=True),
    Output("bull_hits_all", "children", allow_duplicate=True),
    Output("25_hits_all", "children", allow_duplicate=True),
    Input("btn_confirm_bp", "n_clicks"),
    State("n_visits_bp", "children"),
    State("length_dataframe", "children"),
    State("bull_hits_current", "children"),
    State("25_hits_current", "children"),
    State("bull_hits_all", "children"),
    State("25_hits_all", "children"),
    State("dart_1_bp", "children"),
    State("dart_2_bp", "children"),
    State("dart_3_bp", "children"),
    prevent_initial_call = True
)
def update_currents(n, n_visits_now, n_visits_all, bull_hits_now, hits_25_now, bull_hits_all, hits_25_all, d1, d2, d3):
    n_bull_in_visit = [d1, d2, d3].count("Bull")
    n_25_in_visit = [d1, d2, d3].count("25") + [d1, d2, d3].count("25 (IW)")

    total_bulls_now = int(bull_hits_now.split(" /")[0]) + n_bull_in_visit
    total_bulls_all = int(bull_hits_all.split(" /")[0]) + n_bull_in_visit

    total_25s_now = int(hits_25_now.split(" /")[0]) + n_25_in_visit
    total_25s_all = int(hits_25_all.split(" /")[0]) + n_25_in_visit

    n_throws_now = 3 * (int(n_visits_now) + 1)
    # need to always add n_visits_all since this is only
    # updated at the start when the dataframe is read
    n_throws_all = 3 * (int(n_visits_all) + int(n_visits_now) + 1)

    perc_bull_now = float("%.1f" % (100 * total_bulls_now / n_throws_now))
    perc_bull_all = float("%.1f" % (100 * total_bulls_all / n_throws_all))
    
    perc_25_now = float("%.1f" % (100 * total_25s_now / n_throws_now))
    perc_25_all = float("%.1f" % (100 * total_25s_all / n_throws_all))
    
    bull_hits_output_now = f"{total_bulls_now} / {n_throws_now} ({perc_bull_now}%)"
    bull_hits_output_all = f"{total_bulls_all} / {n_throws_all} ({perc_bull_all}%)"

    hits_25_output_now = f"{total_25s_now} / {n_throws_now} ({perc_25_now}%)"
    hits_25_output_all = f"{total_25s_all} / {n_throws_all} ({perc_25_all}%)"

    return str(int(n_visits_now) + 1), bull_hits_output_now, hits_25_output_now, bull_hits_output_all, hits_25_output_all
