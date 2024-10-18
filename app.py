import dash
from layout import page_layout
from dash import html, dash_table, callback, Input, Output, State, dcc
from components.batfish import Batfish
import dash_cytoscape as cyto
import pandas as pd
from components.functions import ensure_string_columns, get_layer3_graph, get_bgp_graph

external_stylesheets=['./Assets/bWLwgP.css']

# Create the Dash app
app = dash.Dash(__name__, title='Bat Dash', external_stylesheets=external_stylesheets, suppress_callback_exceptions=True,)

# App Layout
app.layout = page_layout

# Callbacks
# Rendering of items in tab
@callback(Output('tabs-content-inline', 'children'),
          Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        # Input for Batfish Host
        return html.Div([
            html.Label("Batfish Host (default: 'localhost')"), 
            dcc.Input(id='batfish-host', type='text', value='localhost'),
            # Input for Network Name
            html.Label("Network Name"),
            dcc.Input(id='network-name', type='text', value='test_network', placeholder="Enter network name"),
            # Input for Snapshot Name
            html.Label("Snapshot Name"),
            dcc.Input(id='snapshot-name', type='text', value='test_snapshot', placeholder="Enter snapshot name"),
            #Submit button to set snapshot
            html.Button('Submit', id='submit-network', n_clicks=0)])
    elif tab == 'tab-2':
        return html.Div([
            dcc.Tabs(id='batfish-tabs', value='node-props', children=[
                dcc.Tab(label='Node Props', value='node-props'),
                dcc.Tab(label='Layer 3 Edges', value='layer3-edges'),
                dcc.Tab(label='BGP Edges', value='bgp-edges'),
                dcc.Tab(label='Trace Route', value='trace-route')
            ]),
            html.Div(id='batfish-tabs-content')
            ])

# Getting batfish initialize data from tab 1
@callback(
    Output('batfish-network-info', 'data'),
    Input('submit-network', 'n_clicks'),
    State('batfish-host', 'value'),
    State('network-name', 'value'),
    State('snapshot-name', 'value')
)
def initialize_batfish_instance(n_clicks, batfish_host, network_name, snapshot_name):
    if n_clicks > 0:
        # Store the Batfish-related values in dcc.Store
        return {
            'host': batfish_host,
            'network': network_name,
            'snapshot': snapshot_name
        }
    return dash.no_update

# Rendering items in tab 2
@app.callback(
    Output('batfish-tabs-content', 'children'),
    Input('batfish-tabs', 'value')
)
def render_batfish_tab_content(tab):
    if tab == 'node-props':
        return html.Div([
            html.Label("Node Properties:"),
            dcc.Input(id='node-name', type='text', placeholder="Enter node name"),
            html.Button('Get Node Properties', id='submit-node', n_clicks=0),
            html.Div(id='node-output', style={'marginTop': '10px'})
        ])
    elif tab == 'layer3-edges':
        return html.Div([
            html.Button('Get Layer 3 Edges', id='submit-layer3', n_clicks=0),
            html.Div(id='layer3-output', style={'marginTop': '10px'})
        ])
    elif tab == 'bgp-edges':
        return html.Div([
            html.Button('Get BGP Edges', id='submit-bgp', n_clicks=0),
            html.Div(id='bgp-output', style={'marginTop': '10px'})
        ])

@callback(
    Output('node-output', 'children'),
    Input('submit-node', 'n_clicks'),
    State('batfish-network-info', 'data'),  # Stored Batfish data
    State('node-name', 'value')
)
def get_node_properties(n_clicks, batfish_data, node_name):
    if n_clicks > 0 and batfish_data:
        node_properties = Batfish(batfish_data['host'],
            batfish_data['network'],
            batfish_data['snapshot']).node_properties(node_name)

        if node_properties is not None and not node_properties.empty:
            selected_columns = ['Node', 'Configuration_Format', 'Interfaces', 'Routing_Policies']
            node_properties_selected = node_properties[selected_columns].copy()
            #Ensure all columns are string-compatible
            node_properties_selected = ensure_string_columns(node_properties_selected)

            return dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in node_properties_selected.columns],
                data=node_properties_selected.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'whiteSpace': 'normal'},
                style_data_conditional=[{
                        'if': {'column_id': 'Routing_Policies'},
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'overflow': 'hidden',
                    }]
            )
        else:
            return "No data found for the provided node."
    return ""

# Getting data and creating layer 3 graph
@callback(
    Output('layer3-output', 'children'),
    Input('submit-layer3', 'n_clicks'),
    State('batfish-network-info', 'data'),  # Stored Batfish data
)
def get_layer3(n_clicks, batfish_data):
    if n_clicks > 0:
        layer3 = Batfish(batfish_data['host'],
            batfish_data['network'],
            batfish_data['snapshot']).layer3_edges()
        if layer3 is not None:
            return get_layer3_graph(layer3)

# Getting data and creating bgp graph        
@callback(
    Output('bgp-output', 'children'),
    Input('submit-bgp', 'n_clicks'),
    State('batfish-network-info', 'data'),  # Stored Batfish data
)
def get_bgp(n_clicks, batfish_data):
    if n_clicks > 0:
        bgp_info = Batfish(batfish_data['host'],
            batfish_data['network'],
            batfish_data['snapshot']).bgp_edges()
        if bgp_info is not None:
            return get_bgp_graph(bgp_info)

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050,debug=True)
