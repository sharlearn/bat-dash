from dash import html, dcc

tabs_styles = {
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
    html.H1("Batfish Dashboard"),
    
    ## Tabs to organize elements
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='1: Set Snapshot', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='2: Batfish Queries', value='tab-2', style=tab_style, selected_style=tab_selected_style),
    ]),

    html.Div(id='tabs-content-inline'),

    # # Input for Batfish Host
    # html.Label("Batfish Host (default: 'localhost')"),
    # dcc.Input(id='batfish-host', type='text', value='localhost'),

    # # Input for Network Name
    # html.Label("Network Name"),
    # dcc.Input(id='network-name', type='text', value='test_network', placeholder="Enter network name"),

    # # Input for Snapshot Name
    # html.Label("Snapshot Name"),
    # dcc.Input(id='snapshot-name', type='text', value='test_snapshot', placeholder="Enter snapshot name"),

    # # Input for Nodes (comma-separated list)
    # html.Label("Node"),
    # dcc.Input(id='nodes', type='text', value='', placeholder="Enter node"),

    # # Submit button
    # html.Button('Submit', id='submit-button', n_clicks=0),

    # # Output Table
    # html.Div([
    #   dcc.Loading(
    #     id='loading-table',
    #     type='default',
    #     children=[html.Div(id='output-table')])])
])