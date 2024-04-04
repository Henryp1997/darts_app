import dash
from dash import html, callback
from dash import no_update as nop
from dash.dependencies import Output, Input, State

dash.register_page(__name__, path="/")

def layout():
    return html.Div([
        html.Div("Darts Practice App", style={"color": "white", "font-size": "2.5rem", "text-align": "center"}),
        html.Div(style={"height": "1rem"}),
        html.Div("Practice", className="home_heading"),
        html.Div(style={"height": "1rem"}),
        html.Div([
            html.A(f"▸ Treble 20s", href='t20-practice', className="home_link_inner"),
            html.Div(style={"height": "1rem"}),
            html.A(f"▸ Treble 19s", href='t19-practice', className="home_link_inner"),
        ]),
        html.Div(style={"height": "1rem"}),
        html.Div("Plotting and analysis", className="home_heading"),
        html.Div(style={"height": "1rem"}),
        html.Div([
            html.A(f"▸ Treble 20s", href='t20-plotting', className="home_link_inner"),
            html.Div(style={"height": "1rem"}),
            html.A(f"▸ Treble 19s", href='t19-plotting', className="home_link_inner"),
        ])
    ])