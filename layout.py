from dash import html, dcc

tabs_style = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

page_layout = html.Div([
    html.H1("Batfish Dashboard", style={'textAlign': 'center'}),
    
    ## Tabs to organize elements
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Set Network', value='tab-1'),
        dcc.Tab(label='Batfish Queries', value='tab-2'),
    ], style=tabs_style),
    dcc.Store(id='batfish-network-info'),
    html.Div(id='tabs-content-inline')
])