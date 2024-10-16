import dash_cytoscape as cyto
import pandas as pd

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
    return children