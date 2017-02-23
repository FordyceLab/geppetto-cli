def pressurize(client, valve_number):
    """
    Function to pressurize the valve of a given number

    Args:
    - valve_number (int): number of valve to pressurize
    """

    # Offset the register number
    register_number = 512 + valve_number

    # Read the state of the valve in question
    state = client.read_coils(register_number, 1).bits[0]

    # Valve is currently depressurized if the register state is True
    if state:
        client.write_coil(valve_number, False)


def depressurize(client, valve_number):
    """
    Function to depressurize the valve of a given number

    Args:
    - valve_number (int): number of valve to pressurize
    """

    # Offset the register number
    register_number = 512 + valve_number

    # Read the state of the valve in question
    state = client.read_coils(register_number, 1).bits[0]

    # Valve is currently pressurized if the register state is False
    if not state:
        client.write_coil(valve_number, True)


def read_valve(client, register_number):
    """
    Function to read a specific register number

    Args:
    - register_number (int): register number to read

    Returns:
    - state of the register (True if depressurized, False if pressurized)
    """
    return client.read_coils(register_number, 1).bits[0]
