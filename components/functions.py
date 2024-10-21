from dash import html, dcc
import dash_cytoscape as cyto
import pandas as pd
import re
import dash_bootstrap_components as dbc

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
                'width': '100%',
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
                        'text-background-padding': '5px',
                        'curve-style': 'haystack'
                    }
                },
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(id)',
                        'text-outline-color': '#ffffff',
                        'background-image': './Assets/Router.png',
                        'background-fit': 'cover',
                        'width': 100,
                        'height': 100,
                        'text-background-opacity': 1,
                        'text-background-color': '#ffffff',
                        'text-background-shape': 'roundrectangle',
                        'text-border-style': 'solid',
                        'text-border-opacity': 1,
                        'text-border-width': '1px',
                        'text-border-color': 'black',
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


## Layer 3 Graph Functions
def getnodes(batfish_df):
    node_x = [re.sub('\[.*', '', str(x)) for x in batfish_df['Interface']]
    nodes = [{'data': {'id': device, 'label': device}} for device in
             set(node_x)]
    return nodes

def getedges(batfish_df):
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

# Create layer 3 Graphs
def get_layer3_graph(batfish_df):
    return create_graph(getnodes(batfish_df) + getedges(batfish_df))

def get_bgp_nodes(batfish_df):
    local_node = set(tuple(zip(batfish_df['Node'], batfish_df['AS_Number'])))
    remote_node = set(
        tuple(zip(batfish_df['Remote_Node'], batfish_df['Remote_AS_Number'])))
    all_nodes = list(local_node) + list(remote_node)
    nodes = [
        {
            'data': {'id': device, 'label': device,
                     'parent': 'AS ' + as_number}, 'classes': 'bgp_node',
        }
        for device, as_number in list(set(all_nodes))
    ]
    return nodes



### BGP Graph Functions
def get_bgp_edges(batfish_df):
    test_edges = set(tuple(zip(batfish_df['Node'], batfish_df['Remote_Node'])))
    new_edges = []
    for edge in test_edges:
        if edge[::-1] not in new_edges:
            new_edges.append(edge)

    new_edges = list(set(tuple(sub) for sub in new_edges))
    edges = [
        {'data': {'source': source, 'target': target}}
        for source, target in new_edges]
    return edges

def getparents(batfish_df):
    as_numbers = list(batfish_df['AS_Number']) + list(
        batfish_df['Remote_AS_Number'])
    parent_nodes = [
        {
            'data': {'id': 'AS ' + asn, 'label': 'AS ' + asn}, 'classes': 'parent',
        }
        for asn in list(set(as_numbers))
    ]
    return parent_nodes

def get_bgp_graph(batfish_df):
    return create_graph(getparents(batfish_df) + get_bgp_nodes(
        batfish_df) + get_bgp_edges(batfish_df))
        


## Trace Route Graph
def create_traceroute_graph(elements, stylesheet):
    children = [
        cyto.Cytoscape(
            id='traceroute-cytoscape',
            style={
                'width': '1720px',
                'height': '500px',
            },

            elements=elements,
            stylesheet=stylesheet,
            layout={'name': 'preset',
                    'padding': 60,
                    }
        ),
    ]
    return children

def get_elements(nodes, trace_edges, max_value, node_list):
    start = node_list[0]
    finish = node_list[-1]

    edges = [
        {'data': {'source': source, 'target': target}, 'classes': trace}
        for trace, source, target, in trace_edges]
    nodes = [{'data': {'id': device, 'label': device},
              'position': {'x': position[0] * 200, 'y': position[1] * 200},
              'classes':'Router'}
             for device, position in nodes.items()]
    start_node = [
        {'data': {'id': start, 'label': start},
         'position': {'x': 0, 'y': 0}}]
    finish_node = [{'data': {'id': finish, 'label': finish},
         'position': {'x': (max_value + 1) * 200, 'y': 0}}]
    all_nodes = start_node + finish_node + nodes

    return all_nodes + edges

def get_traceroute_details(direction, result, bidir, chaos=False):
    """
    :param direction:
        The direction of the trace:
            String: "forward" or "reverse"
    :param result:
        traceroute pandas dataframe
    :param bidir:
        If the traceroute is bidirectional:
            boolean: true or false
    :return:
        Graph of the trace route and trace route details
    """

    if bidir:
        if direction == "forward":
            traces = result.Forward_Traces[0]
        else:
            traces = result.Reverse_Traces[0]
            if traces == []:
                return [None, None]
    else:
        if chaos:
            traces = result.Traces[0]

        else:
            traces = result.Traces[0]

    stylesheet = [
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier'
            }
        },
        {
            'selector': 'node',
            'style': {
                'label': 'data(id)',
                'text-outline-color': '#ffffff',
                'background-image': 'assets/img/Router2.png',
                'background-fit': 'cover',
                'width': 50,
                'height': 50,
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
    ]

    colors = ["red", "blue", "green", "black", "brown", "cyan",
              "grey", "lime", "purple",
              "violet", "teal", "silver", "orange", "pink", "yellow"]
    trace_count = 0
    trace_tabs_children = []
    node_list = []
    nodes = {}
    trace_edges = []
    for x in traces:
        trace = traces[trace_count]
        hops = trace.dict()['hops']
        count = 0
        step_row_children = []
        x = 0
        y = 0
        first_edge_node_count = 0
        second_edge_node_count = 1
        for hop in hops:
            outside_toast_children = []
            node = hop['node']

            # Node positioning
            if node not in nodes:

                if node not in nodes:
                    all_x_values = [value[0] for value in nodes.values()]
                    if x in all_x_values:
                        nodes[node] = [x, all_x_values.count(x)]
                    else:
                        node_list.append(node)
                        nodes[node] = [x, y]
            x += 1

            pair = []

            # builds edges
            if second_edge_node_count < len(trace):
                first_edge_node = hops[first_edge_node_count]["node"]
                second_edge_node = hops[second_edge_node_count]["node"]

                pair.append('trace_' + str(trace_count))
                pair.append(first_edge_node)
                pair.append(second_edge_node)
                trace_edges.append(tuple(pair))
            first_edge_node_count += 1
            second_edge_node_count += 1


            # Gets details of each hop
            hop_steps = hop['steps']
            outside_toast_id = "trace_{trace_count}_step_{step_count}".format(
                trace_count=trace_count, step_count=count)
            outside_toast_header = "Step: {step_count} Node: {node}".format(
                step_count=count, node=node)

            for step_detail in hop_steps:
                step_detail_dict = step_detail['detail']
                step_action = step_detail['action']
                inside_toast_content = ""
                inside_toast_header = step_action
                inside_toast_content_html = None
                inside_toast_id = "trace_{trace_count}_step_{step_count}_{step_action}".format(
                    trace_count=trace_count, step_count=count,
                    step_action=step_action)
                for outside_key, outside_value in step_detail_dict.items():

                    inside_toast_children = []
                    inside_value_dict = ""

                    if outside_key == "routes":
                        if outside_value:
                            for inside_key, inside_value in outside_value[0].items():
                                inside_value_dict += "{key} : {value}\n".format(
                                    key=inside_key, value=inside_value)
                            inside_toast_content_html = html.Details(
                                [html.Summary(outside_key),
                                 html.Div(html.Pre(inside_value_dict))])
                        else:
                            inside_toast_content_html = html.Details(
                                [html.Summary(outside_key),
                                 html.Div(html.Pre("NO ROUTE"))])

                    elif outside_key == "flow":
                        for inside_key, inside_value in outside_value.items():
                            inside_value_dict += "{key} : {value}\n".format(
                                key=inside_key, value=inside_value)
                        inside_toast_content_html = html.Details(
                            [html.Summary(outside_key),
                             html.Div(html.Pre(inside_value_dict))])
                    else:
                        inside_toast_content += "{key} : {value}\n".format(
                            key=outside_key, value=outside_value)

                inside_toast_children.append(html.Pre(inside_toast_content))
                inside_toast_children.append(inside_toast_content_html)
                inside_toast = dbc.Toast(
                    inside_toast_children,
                    id=inside_toast_id,
                    header=inside_toast_header,
                    style={"min-width": "200px",
                           "font-size": "12px"})

                outside_toast_children.append(inside_toast)
            count += 1

            step_toast = dbc.Toast(
                outside_toast_children,
                is_open=True,
                id={
                    'type': 'Step_Toast',
                    'index': outside_toast_id
                },
                header=outside_toast_header,
                style={"min-width": "300px",
                       "font-size": "15px"},

            )

            step_row_children.append(step_toast)
        try:

            max_value = max(all_x_values)
        except ValueError:
            max_value = 0
        step_row = html.Div(
            dbc.Row(children=step_row_children,

                    style={"display": "flex",
                           "min-width": "100%",
                           "min-height": "300px",
                           "overflowX": "auto",
                           "flex-wrap": "nowrap",
                           'margin-bottom': '20px'}),
            style={
                'whiteSpace': 'nowrap',
                'width': '1690px',
                'height': 'auto',
                'margin-left':"15px"


            },
        )
        tab_style = {
            'borderBottom': '1px solid #d6d6d6',
            'padding': '6px',
            'fontWeight': 'bold',
            "color": colors[0],
            "font-size":"18px"

        }

        tab_selected_style = {
            'borderTop': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'backgroundColor': colors[0],
            'color': 'white',
            'padding': '6px',
            "font-size":"18px"
        }
        trace_tab = dcc.Tab(className='trace-tab',
                            label="Trace " + str(trace_count),
                            children=step_row,
                            style=tab_style,
                            selected_style=tab_selected_style)

        trace_tabs_children.append(trace_tab)

        trace_style = [{
            'selector': 'edge.' + 'trace_' + str(trace_count),
            'style': {
                'target-arrow-color': colors[0],
                'target-arrow-shape': 'triangle',
                'line-color': colors[0]
            }
        }]
        trace_count += 1
        del colors[0]
        stylesheet = stylesheet + trace_style

    return [create_traceroute_graph(
        get_elements(nodes, trace_edges, max_value, node_list), stylesheet),
        trace_tabs_children]