import dash
from dash import html, callback
from dash import no_update as nop
from dash.dependencies import Output, Input, State

# App specific imports
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
                html.Div([
                    html.Div(style={"height": "1rem"}),
                    html.Div("Current Target: "),
                    html.Div([
                            html.Button("MISS", className="backspace_button", style={"width": "30%"}),
                            html.Button("HIT", className="green_button", style={"width": "30%"}),
                            html.Div(style={"height": "0.5rem"}),
                        ])
                    ],
                    className="grey_window", style={"width": "90%"}
                )
            ], id="atc_main_window", style=HIDE)
        ])

### CALLBACKS
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
def change_choice_text(n1, n2, n3, n4, settings):
    trigger = dash.callback_context.triggered[0]['prop_id']
    if "one" in trigger or "two" in trigger:
        nplayers = "One" if "one" in trigger else "Two"
        return f"{nplayers} Player / {settings.split("/ ")[1]}"

    mode = "Ordered Mode" if "ordered" in trigger else "Random Mode"
    return f"{settings.split(" /")[0]} / {mode}?"


@callback(
    Output("settings_screen", "style"),
    Output("atc_main_window", "style"),
    Input("btn_mode_confirm", "n_clicks"),
    prevent_initial_call=True
)
def show_main_window(_):
    return HIDE, {}
