from dash import html

# App-specific imports
from pages.helpers.common import v_spacer, padded_text_white


def get_darts_hit_bar(page):
    """ Get the top bar html.Div which will show the scores from user button presses """
    if page == "practice":
        prefix = ""
    elif page == "bull_practice":
        prefix = "_bp"

    return html.Div([
        v_spacer("1vh"),
        padded_text_white("Darts:", margin_right="7.5vw"),
        html.Div("_____", id=f"dart_1{prefix}", className="white_text_inline", style={"margin-right": "7.5vw"}),
        html.Div("_____", id=f"dart_2{prefix}", className="white_text_inline", style={"margin-right": "7.5vw"}),
        html.Div("_____", id=f"dart_3{prefix}", className="white_text_inline", style={"margin-right": "7.5vw"}),
        v_spacer("1vh"),
    ], style={"border": "2px solid #fff"})
