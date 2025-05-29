import dash
from dash import html

# App specific imports
from consts import TRI_RIGHT

dash.register_page(__name__, path="/")

def layout():
    return html.Div([
        html.Div(id="hidden_div1", style={"display": "none"}),
        html.Div("Darts Practice App", style={"color": "white", "font-size": "2.5rem", "text-align": "center"}),
        html.Div(style={"height": "1rem"}),
        html.Div("Match", className="home_heading"),
        html.Div(style={"height": "1rem"}),
        html.Div([
            html.A(f"{TRI_RIGHT} 301", id="301_link", href="match?start=301", className="home_link_inner"),
            html.Div(style={"height": "1rem"}),
            html.A(f"{TRI_RIGHT} 501", id="501_link", href="match?start=501", className="home_link_inner"),
        ]),
        html.Div(style={"height": "1rem"}),
        html.Div("Practice", className="home_heading"),
        html.Div(style={"height": "1rem"}),
        html.Div([
            html.A(f"{TRI_RIGHT} Treble 20s", id="t20_link", href="practice?target=t20", className="home_link_inner"),
            html.Div(style={"height": "1rem"}),
            html.A(f"{TRI_RIGHT} Treble 19s", id="t19_link", href="practice?target=t19", className="home_link_inner"),
            html.Div(style={"height": "1rem"}),
            html.A(f"{TRI_RIGHT} Bullseye", id="bull_link", href="bull-practice", className="home_link_inner"),
        ]),
        html.Div(style={"height": "1rem"}),
        html.Div("Plotting and analysis", className="home_heading"),
        html.Div(style={"height": "1rem"}),
        html.Div([
            html.A(f"{TRI_RIGHT} Treble 20s", href="t20-plotting", className="home_link_inner"),
            html.Div(style={"height": "1rem"}),
            html.A(f"{TRI_RIGHT} Treble 19s", href="t19-plotting", className="home_link_inner"),
        ])
    ])
