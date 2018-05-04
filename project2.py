# Header
print('')
print('Script Name:             | project.py 101')
print('File Date:               | 2017-11')
print('Author:                  | Chris Fong')
print('Version:                 | 0.1')
print('Python Version:          | 3.x')
print('Tab:                     | 4 spaces')
print('Library Dependencies:    | netmiko; csv; getpass')
print('Special Thanks-')
print('Tim G')
print('')
# End Header

# |----------------------------80 Character Ruler------------------------------|

'''
README:

Expected CSV Headers/Columns
Node_Name,IP_Address,Device_Type

This project assumes a Windows OS to make relative folder paths for saving
output.

'''

# Import Library Dependencies
import getpass
import csv
import os

from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException

#######################################
# Define Global Variables
# Input Username, Password and Enable Password
# Input CSV
#######################################

username = str(input("Please Enter your username: "))
print('The username you entered was: ', username)

# Input password without echoing password
try:
    p = getpass.getpass(prompt='Please enter your password: ')
except Exception as error:
    print('ERROR: No password entered', error)
else:
    print('Password has been accepted.')

# Input Enable password without echoing passwor
try:
    ep = getpass.getpass(prompt='Please enter your Enable password: ')
except Exception as error:
    print('ERROR: No Enable password entered', error)
else:
    print('Enable Password has been accepted.')

# Input CSV File Name
print ('')
print ('')
print('#######################################')
print('Example Local Path: ')
print('inventory.csv')
print('Example Windows Relative Path: ')
print('CSV_Input\inventory.csv')
print('CSV Headers:')
print('Node_Name,IP_Address,Device_Type')
print('#######################################')
file_name=str(input("Please Enter the input CSV file name: "))
print('Input CSV file:', file_name)
print ('')
print ('')
# enddef


#######################################
# Define Functions
#######################################




# Define connection
def my_connection(hostname, device, ip_addr, username, p, ep):
    """
    Attempts connection to device with NetMiko and handles errors.
    Args:
        device      string - Device type (per NetMiko)
        ip_addr     string - Device IP address
        username    string - Device username
        p           string - Device password
        ep          string - Device enable password

    Returns:
        NetMiko connection handle if successfully connected,
        False if connection fails.
    """

    try:
        connection = ConnectHandler(device_type=device, ip=ip_addr,
                                    username=username,
                                    password=p, secret=ep)
    except NetMikoTimeoutException:
        print(hostname + " Connection timed out!")
        return False
    except NetMikoAuthenticationException:
        print(hostname + " Authentication failed!")
        return False
    except NetMikoAuthenticationException:
        print(hostname + " Authentication failed!")
        return False
    except TimeoutError:
        print(hostname + " Other timeout error!")
        return False
    # endtry

    return connection
# enddef


# Define single command
def run_cmd(command, prompt, connection, quiet=False, show_prompt=True,
            delay_factor=1):
    """
    Runs a single command on a device and displays output.
    Args:
        command         string - Command to execute
        prompt          string - Device prompt (typically hostname#)
        connection      object - Connection to device (NetMiko)
        quiet           bool - Hide command output? Defaults to False
        show_prompt     bool - Echo the prompt/command? Defaults to true
        delay_factor    int - Change timeout of command-run. Defaults to 1.
    Returns:
        Output of command
    """

    try:
        output = connection.send_command(command, delay_factor=delay_factor)
    except IOError:
        # Seen when delay not long enough
        print_err("send_command(" + command + ") IOError!")
        return  # Skip additional output.
    # endtry

    if show_prompt and not quiet:
        print(prompt + " " + command)  # Echo prompt and executed command
    # endif

    if not quiet:
        print(output)  # Echo output of command executed
    # endif

    return output  # Return output of executed command
# enddef

# def run_cmds():
#
# def run_en_cmd():
#
# def run_en_cmds():
#
# def run_pair_cmds():

# Create directories for a Node
def create_folder(hostname):
    path = os.getcwd()
    newdir = os.path.join(path, 'OutputConfigurations', hostname)
    os.makedirs(newdir)
    return newdir

# Open CSV file with DictReader
def read_csv_file(commands):
    with open(file_name, mode='r') as csvfile:
        readCSV = csv.DictReader(csvfile)
        for row in readCSV:
            hostname = row['Node_Name']
            ip_addr = row['IP_Address']
            device = row['Device_Type']

            # Uncomment below for testing
            # print(hostname)
            # print(ip_addr)
            # print(device)
            # print(username)
            # print(p)
            # print(ep)
            create_folder(hostname)
            node = {
                'device_type': device,
                'ip': ip_addr,
                'username': username,
                'password': p,
                'secret': ep,
                'verbose': False,
            }

            # Print for readability
            print('\n#######################################\n')
            print(">>>>>>>>> {0}".format(row['Node_Name']))
            print(">>>>>>>>> {0}\n".format(row['IP_Address']))

            # Connect to device
            net_connect = my_connection(hostname, device, ip_addr, username,
            p, ep)
            if not net_connect:
                continue  # Skip this node due to connection issues.
            prompt = net_connect.find_prompt()
            for command in commands:
                run_cmd(command, prompt, net_connect)
            net_connect.disconnect()
            print("\n>>>>>>>>> End <<<<<<<<<\n\n")




# Main Appilication
def main():
    # Enter command below
    # EXAMPLE:
    # commands = ["dir flash: | include .bin",
    #             "show run | include boot system",
    #             "show version | include image file"]
    commands = ["dir | include .bin", "show run | include boot system", "show version | include image file"]
    read_csv_file(commands)
    exit()

if __name__ == "__main__":
    main()
