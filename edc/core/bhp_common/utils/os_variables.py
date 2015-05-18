import socket


def os_variables():

    variables = {}
    variables['hostname'] = socket.gethostname()
    variables['wlan_network'] = ""
    variables['warnings'] = []
    return variables
