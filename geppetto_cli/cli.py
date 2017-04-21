import argparse
import yaml
from tqdm import *
from pymodbus3.client.sync import ModbusTcpClient
from .valves import *
import time

# Create the argument parser
desc = "Run scripted control of pneumatic system"

parser = argparse.ArgumentParser(description=desc)

parser.add_argument("map",
                    type=str,
                    help="YAML file mapping valve names to solenoids")

parser.add_argument("protocol",
                    type=str,
                    help="YAML protocol file")


def timer(duration, name):
    """
    Create a timer

    Args:
    - duration (int) - duration of the timer in seconds
    - name (str) - name for the timer
    """

    # Make timer
    for i in tqdm(range(duration), desc = name):
        time.sleep(1)


def handle_valves(step, valve_map, client):
    """
    Function to handle valve switching with each step

    Args:
    - step (dict): dictionary of changes for the current step
    - valve_map (dict): dictionary of valve name mappings
    - client (pymodbus): pymodbus3 connection to Wago
    """

    # Handle pressurizing the appropriate valves
    if "pressurize" in step:
        pressurize = step["pressurize"]

        for valve in pressurize:
            pressurize(client, valve_map[valve])

    # Handle depressurizing the appropriate valves           
    if "depressurize" in step:
        depressurize = step["depressurize"]
        
        for valve in depressurize:
            depressurize(client, valve_map[valve])


def main(args):
    """
    Run the command line interface

    Args:
    - args (list): list of command line arguments
    """

    # Parse the command line arguments
    args = parser.parse_args(args)

    # Open and read the valve map file
    with open(args.map, "r") as map_file:
        valve_map = yaml.load(map_file)

    # Open and read the protocol file
    with open(args.protocol, "r") as protocol_file:
        protocol = yaml.load(protocol_file)

    # Connect the modbus interface
    client = ModbusTcpClient(protocol["ip_address"])

    # Give the user some info
    tqdm.write("Running script: " + str(protocol["name"]))

    # Handle the initial setting for each valve
    if "initial_settings" in protocol:
        initial_settings = protocol["initial_settings"]
        handle_valves(initial_settings, valve_map, client)              

    # Set the step number
    step_num = 1

    # Handle each individual step
    for step in tqdm(protocol["steps"], desc = "Steps completed"):
        handle_valves(step, valve_map, client)
        if "name" in step:
            timer(step["duration"], step["name"])
        else:
            timer(step["duration"], "Step " + str(step_num))

