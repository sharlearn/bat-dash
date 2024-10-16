import dash
from layout import page_layout
from dash import html, dash_table, callback, Input, Output, State
from components.batfish import Batfish
import dash_cytoscape as cyto
import pandas as pd
from components.functions import ensure_string_columns

# Create the Dash app
app = dash.Dash(__name__, title='Bat Dash')

# App Layout
app.layout = page_layout


# Callbacks
@callback(
    Output('output-table', 'children'),
    Input('submit-button', 'n_clicks'),
    State('batfish-host', 'value'),
    State('network-name', 'value'),
    State('snapshot-name', 'value'),
    State('nodes', 'value')
)
def update_table(n_clicks, batfish_host, network_name, snapshot_name, nodes):
    if n_clicks > 0:
        # Create an instance of Batfish with the provided network and snapshot names
        bf = Batfish(batfish_host, network_name, snapshot_name)
        
        # Fetch node properties using Batfish
        node_properties = bf.node_properties(nodes)
        
        # Check if we got valid results
        if node_properties is not None and not node_properties.empty:
            print(node_properties)

            abbreviated_df = node_properties[['Node', 'VRFs', 'Routing_Policies']]
            abbreviated_df = ensure_string_columns(abbreviated_df)
            print(abbreviated_df)
            display_table = dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in abbreviated_df.columns],
                data=abbreviated_df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'maxWidth': '150px'},
                style_data_conditional=[
                    {
                        'if': {'column_id': 'Routing_Policies'},  # Replace with the actual column name
                        'whiteSpace': 'normal',  # Enable text wrapping
                        'height': 'auto',        # Allow dynamic row height based on content
                        'overflow': 'hidden',
                    }]
            )
            # Create a DataTable to display the node properties
            return display_table
        else:
            return html.Div("No data returned. Please check the input values.")
    return html.Div()

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050,debug=True)
