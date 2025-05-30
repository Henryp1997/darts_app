from dash import html

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


def padded_text_white(text, margin_left="2vw", margin_right="0"):
    """ Get a html.Div in white text with a left and right margin """
    return html.Div(
        text,
        className="white_text_inline",
        style={"margin-left": margin_left, "margin-right": margin_right}
    )


def v_spacer(height):
    """ 
    Return a html.Div with a vertical height but no contents 
    `height` must be a valid css value
    """
    return html.Div(style={"height": height})
