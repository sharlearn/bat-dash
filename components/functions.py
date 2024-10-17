import dash_cytoscape as cyto
import pandas as pd
import re

# Function to convert data within column to string, this is required for dash_table function
def ensure_string_columns(df):
    ##Ensure all columns in the DataFrame contain string data.
    ##If a column contains non-string values, convert them to strings.
    for col in df.columns:
        if not pd.api.types.is_string_dtype(df[col]):
            # Convert to string
            df[col] = df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
    return df


def create_graph(elements):
    print('inside create graph')
    children = [
        cyto.Cytoscape(
            id='cytoscape',
            responsive=True,

            style={
                'width': '1500px',
                'height': '700px',
            },
            elements=elements,
            stylesheet=[
                {
                    'selector': 'edge',
                    'style': {
                        'source-text-rotation': 'autorotate',
                        'edge-text-rotation': 'autorotate',
                        'target-text-rotation': 'autorotate',
                        'source-label': 'data(source_label)',
                        'target-label': 'data(target_label)',
                        'source-text-offset': '100',
                        'target-text-offset': '100',
                        'text-background-opacity': 1,
                        'text-background-color': '#ffffff',
                        'text-background-shape': 'roundrectangle',
                        'text-border-style': 'solid',
                        'text-border-opacity': 1,
                        'text-border-width': '1px',
                        'text-border-color': 'darkgray',
                        'text-background-padding': '3px',
                        'curve-style': 'haystack'
                    }
                },
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(id)',
                        'text-outline-color': '#ffffff',
                        'background-image': 'assets/img/Router2.png',
                        'background-fit': 'cover',
                        'width': 100,
                        'height': 100,
                        'text-background-opacity': 1,
                        'text-background-color': '#ffffff',
                        'text-background-shape': 'roundrectangle',
                        'text-border-style': 'solid',
                        'text-border-opacity': 1,
                        'text-border-width': '1px',
                        'text-border-color': 'darkgray',
                        'font-weight': 'bold',
                        'text-background-padding': '5px',
                    }
                },
                {
                    'selector': '.parent',
                    'style': {
                        'background-image': 'none',
                        'background-color': 'ghostwhite',
                        'border-color':'#555555',
                    }
                },
            ],
            layout={'name': 'breadthfirst',
                    'padding': 60,
                    'spacingFactor': 2.5,
                    }
        ),

    ]
    print('before create graph return')
    print(children)
    return children


## Layer 3 Graph Functions
def getnodes(batfish_df):
    print('inside get nodes')
    node_x = [re.sub('\[.*', '', str(x)) for x in batfish_df['Interface']]
    nodes = [{'data': {'id': device, 'label': device}} for device in
             set(node_x)]
    return nodes

def getedges(batfish_df):
    print('inside get edges')
    test_edges = set(
        tuple(zip(batfish_df['Interface'], batfish_df['Remote_Interface'])))
    new_edges = []
    new_new_edges = []
    for edge in test_edges:
        if edge not in new_edges:
            if edge[::-1] not in new_edges:
                new_edges.append(edge)
                test = []
                for x in edge:
                    x = re.sub('\]', '', str(x))
                    x_test = x.split('[')
                    x_test[1] = re.sub("\..*", ".subints", x_test[1])
                    x_test[1] = re.sub("^Ethernet", "eth", x_test[1])
                    x_test[1] = re.sub("^TenGigabitEthernet", "Ten", x_test[1])
                    x_test[1] = re.sub("^GigabitEthernet", "Ge", x_test[1])
                    x_test[1] = re.sub("^port-channel", "po", x_test[1])
                    x_test[1] = re.sub("^Port-Channel", "po", x_test[1])
                    x_test[1] = re.sub(r"([^-]+-\S{4})(.*)",r"\1", x_test[1])  #shorten the AWS interface names
                    test += x_test
                new_new_edges.append(test)
    new_new_edges = list(set(tuple(sub) for sub in new_new_edges))
    edges = [
        {'data': {'source': source, 'target': target,
                  'source_label': source_int, 'target_label': target_int}}
        for source, source_int, target, target_int in new_new_edges]
    return edges

# Create Graphs
def get_layer3_graph(batfish_df):
    print('get layer 3 graph inside')
    return create_graph(getnodes(batfish_df) + getedges(batfish_df))