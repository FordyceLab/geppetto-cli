# Geppetto-CLI

This repository contains the command line interface for the [Geppetto microfluidic pneumatic control software](https://github.com/FordyceLab/geppetto). This command line interface allows scripting of extended control protocols.

## Installation

The `geppetto-cli` toolset requires Python 3.

Currently, the library can be cloned and installed with:

```
git clone https://github.com/FordyceLab/geppetto-cli.git
cd geppetto-cli
pip install .
```

This installation will make the `geppetto.py` command line utility accessible. You can access the `help` function from the command line with `geppetto.py -h`.

## Usage

The help function of `geppetto.py` (`geppeto.py -h`) gives a description of the two files needed to run a specific automated protocol. 

```
usage: geppetto.py [-h] map protocol

Run scripted control of pneumatic system

positional arguments:
  map         YAML file mapping valve names to solenoids
  protocol    YAML protocol file

optional arguments:
  -h, --help  show this help message and exit
```

### Map file

The first file is the `map` file. This file is a [YAML](http://www.yaml.org/) file that maps names onto individual valve numbers. For instance, if you wanted to control four valves (named `input`, `flow`, `wash`, and `output`, mapped to valves 1 through 4), your `map` file would look like the one below: 

```
input: 1
flow: 2
wash: 3
output: 4
```

### Protocol

The second file contains the protocol information. A skeleton of the file is given below:

```
name:
ip_address:
initial_settings:
    pressurize:
    depressurize:

steps:
    - name:
      duration:
      pressurize:
      depressurize:
    - name:
      duration:
      pressurize:
      depressurize:
    - ...
```

We start with the name of the protocol on line one. The second line provides the IP address for the Wago controller. The block starting at the third line gives the initial state for all of the valves listed in the `map` file. This dictionary has two sublists. The `pressurize` sublist lists all of the valves that should start in the pressurized state. The `depressurize` sublist lists all valves that should start in the depressurized state.

Next all of the steps of the protocol are given. Each should have a name, a duration (in seconds), and sublists for the valves to be pressurized or depressurized at the beginning of that step. If a step does not have any valves that need to be pressurized or depressurized, simply omit the correct sublist.

An complete example of this file is given below:

```
name: Example protocol
ip_address: 192.168.1.3
initial_settings:
    pressurize:
        - input
        - output
        - wash
        - flow

steps:
    - name: Flow
      duration: 60
      depressurize:
        - input
        - output
        - flow
    - name: Wash
      duration: 30
      pressurize:
        - flow
      depressurize:
        - wash
    - name: Incubate
      duration: 60
      pressurize:
        - input
        - output
        - wash
```
