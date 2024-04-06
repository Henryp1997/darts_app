import dash
from dash import html
from dash import dcc

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.title = 'Darts score recorder'

app.layout = html.Div([
    dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=5000)
