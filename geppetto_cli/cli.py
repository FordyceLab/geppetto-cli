import argparse
import yaml
from tqdm import *
from pymodbus3.client.sync import ModbusTcpClient
from .valves import *
import time

desc = "Run scripted control of pneumatic system"

parser = argparse.ArgumentParser(description=desc)

parser.add_argument("map",
                    type=str,
                    help="YAML file mapping valve names to solenoids")

parser.add_argument("protocol",
                    type=str,
                    help="YAML protocol file")


def timer(duration, name):
    for i in tqdm(range(duration), desc = name):
        time.sleep(1)

def handle_valves(step, valve_map):
    if "pressurize" in step:
        pressurize = step["pressurize"]

        for valve in pressurize:
                pressurize(client, valve_map[valve])

    if "depressurize" in step:
        depressurize = step["depressurize"]
        
        for valve in depressurize:
                depressurize(client, valve_map[valve])

def main(args):

    args = parser.parse_args(args)

    with open(args.map, "r") as map_file:
        valve_map = yaml.load(map_file)

    with open(args.protocol, "r") as protocol_file:
        protocol = yaml.load(protocol_file)

    client = ModbusTcpClient(protocol["ip_address"])

    tqdm.write("Running script: " + str(protocol["name"]))

    if "initial_settings" in protocol:
        initial_settings = protocol["initial_settings"]
        handle_valves(initial_settings, valve_map)                

    step_num = 1
    for step in tqdm(protocol["steps"], desc = "Steps completed"):
        handle_valves(step, valve_map)
        if "name" in step:
            timer(step["duration"], step["name"])
        else:
            timer(step["duration"], "Step " + str(step_num))

