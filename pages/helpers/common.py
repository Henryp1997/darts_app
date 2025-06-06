from dash import html


def v_spacer(height):
    """ 
    Return a html.Div with a vertical height but no contents 
    `height` must be a valid css value
    """
    return html.Div(style={"height": height})


def padded_text_white(text, margin_left="2vw", margin_right="0"):
    """ Get a html.Div in white text with a left and right margin """
    return html.Div(
        text,
        className="white_text_inline",
        style={"margin-left": margin_left, "margin-right": margin_right}
    )
