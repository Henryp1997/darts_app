from dash import html

# App-specific imports
from pages.helpers.common import v_spacer


def create_player_window(pnum):
    """
    Create the window which shows the current target and contains the MISS and HIT buttons
    This is the same for both player 1 and 2 (aside from IDs), hence this function
    """
    return html.Div([
        v_spacer("1.5vh"),
        html.Div(f"Player {pnum} Target:", style={"textAlign": "center"}),
        v_spacer("3vh"),
        html.Div("1", style={"width": "100%", "textAlign": "center", "font-size": "3rem"}),
        v_spacer("3vh"),
        html.Div([
            html.Button(
                "MISS",
                id=f"atc_btn_miss{pnum}",
                className="backspace_button",
                style={"width": "30%", "margin-right": "3vw", "margin-left": "3vw"}
            ),
            html.Button(
                "HIT",
                id=f"atc_btn_miss{pnum}",
                className="green_button",
                style={"width": "30%", "margin-left": "3vw"}
            ),
            html.Div(style={"height": "0.5rem"}),
            ], className="btn_container centered"),
        v_spacer("1.5vh"),
        ], id=f"atc_main_window{pnum}", className="grey_window", style={"width": "90%"}
    )
