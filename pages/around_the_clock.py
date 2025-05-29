import dash
from dash import html, callback
from dash import no_update as nop
from dash.dependencies import Output, Input, State

dash.register_page(__name__)

def layout():
    return html.Div([
            html.Div(f"\U0001F553 Around the Clock", id="title", style={"color": "white", "font-size": "2rem", "border-bottom": "1px solid #fff"}),

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
            ])
        ])

### CALLBACKS