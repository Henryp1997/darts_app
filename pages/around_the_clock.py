import dash
from dash import html, callback, dcc
from dash import no_update as nop
from dash.dependencies import Output, Input, State

# App specific imports
import utils
from pages.helpers import around_the_clock_helper as helper
from common_elems import v_spacer
from consts import CLOCK, TICK, HIDE

dash.register_page(__name__)

def layout():
    return html.Div([
            html.Div(f"{CLOCK} Around the Clock", className="page_title_div"),

            # Initialisation window
            html.Div([
                v_spacer("12vh"),

                # Number of players setting
                html.Div([
                    v_spacer("1.5vh"),
                    html.Div("Choose Number of Players", style={"font-size": "1.5rem", "text-align": "center"}),
                    v_spacer("1.5vh"),
                    html.Div([
                        html.Button("One Player", id="btn_one_player", className="green_button", style={"width": "30vw", "margin-right": "5%"}),
                        html.Button("Two Players", id="btn_two_player", className="backspace_button", style={"width": "30vw"}),
                    ], className="btn_container centered"),
                    v_spacer("1.5vh"),
                ], className="boxed_div"),
                v_spacer("1.5vh"),

                # Mode setting
                html.Div([
                    v_spacer("1.5vh"),
                    html.Div("Choose Mode", style={"font-size": "1.5rem", "text-align": "center"}),
                    v_spacer("1.5vh"),
                    html.Div([
                        html.Button("Ordered", id="btn_mode_ordered", className="green_button", style={"width": "30vw", "margin-right": "5%"}),
                        html.Button("Random", id="btn_mode_random", className="backspace_button", style={"width": "30vw"}),
                    ], className="btn_container centered"),
                    v_spacer("1.5vh"),
                ], className="boxed_div"),
                v_spacer("1.5vh"),

                # Confirmation box
                html.Div([
                    v_spacer("1.5vh"),
                    html.Div([
                        html.Div("One Player / Ordered Mode?", id="chosen_settings", style={"display": "inline-block", "font-size": "1.2rem", "margin-right": "5%"}),
                        html.Button(TICK, id="btn_mode_confirm"),
                    ], className="btn_container centered"),
                    v_spacer("1.5vh"),
                ], className="boxed_div"),
            ], id="settings_screen"),

            # Main window
            html.Div([
                v_spacer("1.5vh"),
                html.Div(
                    id="atc_info_bar",
                    className="grey_window",
                    style={
                        "font-size": "1rem",
                        "textAlign": "left",
                        "padding-left": "2vw", "padding-top": "0.5vh", "padding-bottom": "0.5vh"
                    }
                ),
                v_spacer("2.5vh"),
                helper.create_player_window(1, v_spacer),
                v_spacer("2.5vh"),
                helper.create_player_window(2, v_spacer)
            ], id="atc_main_window", style=HIDE),

            # Array storage
            dcc.Store(id="p1_array", data=[]),
            dcc.Store(id="p2_array", data=[])
        ])

### CALLBACKS

@callback(
    Output("p1_array", "data"),
    Output("p2_array", "data"),
    Input("btn_mode_confirm", "n_clicks"),
    State("chosen_settings", "children"),
    prevent_initial_call=True
)
def create_target_arrays(_, settings):
    nplayers = 2 if "Two" in settings else 1
    mode = "random" if "Random" in settings else "ordered"
    return utils.create_atc_arrays(nplayers, mode)


@callback(
    Output("settings_screen", "style"),
    Output("atc_main_window", "style"),
    Output("atc_main_window1", "style"),
    Output("atc_main_window2", "style"),
    Output("atc_info_bar", "children"),
    Input("btn_mode_confirm", "n_clicks"),
    State("chosen_settings", "children"),
    prevent_initial_call=True
)
def show_main_window(_, settings):
    p2_style = {} if "Two" in settings else HIDE
    return HIDE, {}, {}, p2_style, f"Current Mode: {settings.split("/ ")[1].split(" Mode?")[0]}"


@callback(
    Output("btn_one_player", "className"),
    Output("btn_two_player", "className"),
    Input("btn_one_player", "n_clicks"),
    Input("btn_two_player", "n_clicks"),
    prevent_initial_call=True
)
def change_btn_style(n1, n2):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if "one" in trigger:
        return "green_button", "backspace_button"
    return "backspace_button", "green_button"


@callback(
    Output("btn_mode_ordered", "className"),
    Output("btn_mode_random", "className"),
    Input("btn_mode_ordered", "n_clicks"),
    Input("btn_mode_random", "n_clicks"),
    prevent_initial_call=True
)
def change_btn_style(n1, n2):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if "ordered" in trigger:
        return "green_button", "backspace_button"
    return "backspace_button", "green_button"


@callback(
    Output("chosen_settings", "children"),
    Input("btn_one_player", "n_clicks"),
    Input("btn_two_player", "n_clicks"),
    Input("btn_mode_ordered", "n_clicks"),
    Input("btn_mode_random", "n_clicks"),
    State("chosen_settings", "children"),
    prevent_initial_call=True
)
def change_choice_text(_1, _2, _3, _4, settings):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if "one" in trigger or "two" in trigger:
        nplayers = "One" if "one" in trigger else "Two"
        return f"{nplayers} Player / {settings.split("/ ")[1]}"

    mode = "Ordered Mode" if "ordered" in trigger else "Random Mode"
    return f"{settings.split(" /")[0]} / {mode}?"
