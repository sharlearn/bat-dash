import pandas as pd
from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *

class Batfish():
  def __init__(self, batfish_host, network_name='test_network', snapshot_name='test_snapshot', snapshot_directory='./networks/test_configs'):
    self.batfish_host = batfish_host
    self.snapshot_directory = snapshot_directory
    self.bf = Session(host=batfish_host)
    self.network_name = network_name
    self.snapshot_name = snapshot_name
    # Set the network and initialize the snapshot
    self.set_network(self.network_name)
    self.initialize_snapshot()

  def set_network(self, network_name):
    try:
      self.bf.set_network(network_name)
      print(f"Network '{network_name}' set successfully.")
    except Exception as e:
       print(f"Error setting network '{network_name}': {e}")

  def initialize_snapshot(self):
    try:
        self.bf.init_snapshot(self.snapshot_directory, name=self.snapshot_name, overwrite=True)
        print(f"Snapshot '{self.snapshot_name}' initialized successfully.")
    except Exception as e:
        print(f"Error initializing snapshot '{self.snapshot_name}': {e}")

  # Get Node Properties
  def node_properties(self, nodes_requested):
    print(f'nodes requests {nodes_requested}')
    print(f'type of node requested: {type(nodes_requested)}')
    ##Fetches node properties for the requested nodes.
    try:
        result = self.bf.q.nodeProperties(nodes=nodes_requested).answer().frame()
        print("Node properties retrieved successfully.")
        return result
    except Exception as e:
        print(f"Error retrieving node properties: {e}")
        return None
    
  # Get Layer 3 Edges

  # Get interface properties
  def interface_properties(self, interfaces=None):
    try:
       if interfaces is None:
            # If no interfaces specified, query all interfaces
            return self.bf.q.interfaceProperties().answer().frame()
       else:
            return self.bf.q.interfaceProperties(interfaces=interfaces).answer().frame()
    except Exception as e:
        print(f"Error retrieving interface properties: {e}")
        return None


  # Get BGP Edges
