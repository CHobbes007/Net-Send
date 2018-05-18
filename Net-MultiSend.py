# Header
print('')
print('Script Name:             | project.py 101')
print('File Date:               | 2018-05')
print('Author:                  | Chris Fong')
print('Version:                 | 0.1')
print('Python Version:          | 3.x')
print('Tab:                     | 4 spaces')
print('Library Dependencies:    | netmiko; csv; getpass, os, datetime')
print('')
print('')
# End Header

# |----------------------------80 Character Ruler------------------------------|

'''
README:
Example Local Path: inventory.csv
Example Windows Relative Path: CSV_Input\inventory.csv

CSV Headers:
Node_Name,IP_Address,Device_Type,Commands,Global_Config_Commands

Example Commands:
show run,show ver | in image

Example Global_Config_Commands:
do wr mem,int gi0/0,description Test Description

This project assumes a Windows OS to make relative folder paths for saving
output.

TO DO
Add timestamps
Multithreading
If path or folder exists, do not create
write to file  - functionize
Lots of error handling
    Print Error to Error Log
Lots of documentation
Print an error status
Special Thanks - tgrabrian and ktbyers

'''



# Import Library Dependencies
import getpass
import csv
import os
from datetime import datetime

from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from paramiko.buffered_pipe import PipeTimeout
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
print('Example Local Path: inventory.csv')
print('Example Windows Relative Path: CSV_Input\inventory.csv')
print('')
print('CSV Headers:')
print('Node_Name,IP_Address,Device_Type,Commands,Global_Config_Commands')
print('')
print('Example Commands:')
print('show run,show ver | in image')
print('')
print('Example Global_Config_Commands:')
print('do wr mem,int gi0/0,description Test Description')
print('#######################################')
print ('')
print ('')
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
        # Print to Console
        print(hostname + " Connection timed out!")

        path = os.getcwd()
        # Write to Error Log
        file_error = os.path.join(path, "Log", "Error.txt")
        f=open(file_error, 'a')
        f.write(hostname + " Connection timed out!")
        f.write('\n')
        f.close()

        return False

    except NetMikoAuthenticationException:
        # Print to Console
        print(hostname + " Authentication failed!")

        path = os.getcwd()
        # Write to Error Log
        file_error = os.path.join(path, "Log", "Error.txt")
        f=open(file_error, 'a')
        f.write(hostname + " Authentication failed!")
        f.write('\n')
        f.close()

        return False

    except paramiko.buffered_pipe.PipeTimeout:
        # Print to Console
        print(hostname + " Command Timed Out")

        path = os.getcwd()
        # Write to Error Log
        file_error = os.path.join(path, "Log", "Error.txt")
        f=open(file_error, 'a')
        f.write(hostname + " Command Timed Out")
        f.write('\n')
        f.close()

        return False

    except socket.timeout:
        # Print to Console
        print(hostname + " Command Timed Out")

        path = os.getcwd()
        # Write to Error Log
        file_error = os.path.join(path, "Log", "Error.txt")
        f=open(file_error, 'a')
        f.write(hostname + " Command Timed Out")
        f.write('\n')
        f.close()

        return False

    except TimeoutError:
        # Print to Console
        print(hostname + " Other timeout error!")

        path = os.getcwd()
        # Write to Error Log
        file_error = os.path.join(path, "Log", "Error.txt")
        f=open(file_error, 'a')
        f.write(hostname + " Other timeout error!")
        f.write('\n')
        f.close()

        return False
    # endtry

    return connection
# enddef


# Define single command
def run_cmd(command, prompt, connection, hostname, quiet=False, show_prompt=True,
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
        print("send_command(" + command + ") IOError!")

        path = os.getcwd()
        # Write to Error Log
        file_error = os.path.join(path, "Log", "Error.txt")
        f=open(file_error, 'a')
        f.write('\n')
        f.write("send_command(" + command + ") IOError!")
        f.write('\n')
        f.close()

        return  # Skip additional output.
    # endtry

    if show_prompt and not quiet:
        # Print to Console
        print('\n')
        print(prompt + " " + command)  # Echo prompt and executed command

        path = os.getcwd()
        # Write to invididual log
        file_name = os.path.join(path, "OutputConfigurations", hostname+".txt")
        f=open(file_name, 'a')
        f.write('\n')
        f.write(prompt + " " + command)
        f.write('\n')
        f.close()

        # Write to Log
        file_log = os.path.join(path, "Log", "log.txt")
        f=open(file_log, 'a')
        f.write('\n')
        f.write(prompt + " " + command)
        f.write('\n')
        f.close()
    # endif

    if not quiet:
        # Print to Console
        print(output)  # Echo output of command executed

        path = os.getcwd()
        # Write to invididual log
        file_name = os.path.join(path, "OutputConfigurations", hostname+".txt")
        f=open(file_name, 'a')
        f.write(output)
        f.write('\n')
        f.close()

        # Write to Log
        file_log = os.path.join(path, "Log", "log.txt")
        f=open(file_log, 'a')
        f.write(output)
        f.write('\n')
        f.close()

    # endif

    return output  # Return output of executed command
# enddef

def run_en_cmds(command, prompt, connection, hostname, quiet=False, show_prompt=True,
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
        output = connection.send_config_set(command, delay_factor=delay_factor)
    except IOError:
        # Seen when delay not long enough

        # Print to Console
        print("send_command(" + command + ") IOError!")

        path = os.getcwd()
        # Write to Error Log
        file_error = os.path.join(path, "Log", "Error.txt")
        f=open(file_error, 'a')
        f.write("send_command(" + command + ") IOError!")
        f.write('\n')
        f.close()

        return  # Skip additional output.
    # endtry

#    if show_prompt and not quiet:
#        # Print to Console
#        print('\n')
#        print(prompt + " " + command)  # Echo prompt and executed command
#
#        path = os.getcwd()
#        # Write to invididual log
#        file_name = os.path.join(path, "OutputConfigurations", hostname+".txt")
#        f=open(file_name, 'a')
#        f.write('\n')
#        f.write(prompt + " " + command)
#        f.write('\n')
#        f.close()
#
#        # Write to Log
#        file_log = os.path.join(path, "Log", "log.txt")
#        f=open(file_log, 'a')
#        f.write('\n')
#        f.write(prompt + " " + command)
#        f.write('\n')
#        f.close()

    # endif

    if not quiet:
        # Print to Console
        print(output)  # Echo output of command executed

        path = os.getcwd()
        # Write to invididual log
        file_name = os.path.join(path, "OutputConfigurations", hostname+".txt")
        f=open(file_name, 'a')
        f.write(output)
        f.write('\n')
        f.close()

        # Write to Log
        file_log = os.path.join(path, "Log", "log.txt")
        f=open(file_log, 'a')
        f.write(output)
        f.write('\n')
        f.close()
    # endif

    return output  # Return output of executed command

# Open CSV file with DictReader
def read_csv_file():
    with open(file_name, mode='r') as csvfile:
        readCSV = csv.DictReader(csvfile)
        for row in readCSV:
            hostname = row['Node_Name']
            ip_addr = row['IP_Address']
            device = row['Device_Type']
            cmd = row['Commands']
            cmds = row['Global_Config_Commands']
            commands = cmd.split(',')
            global_config_commands = cmds.split(',')

            # Print for readability
            print('\n#######################################')
            print(">>>>>>>>> {0}".format(row['Node_Name']))
            print(">>>>>>>>> {0}\n".format(row['IP_Address']))
            # Timestamp
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print('The time is:')
            print(now_time)
            print('#######################################\n')

            path = os.getcwd()
            # Write to Log
            file_log = os.path.join(path, "Log", "log.txt")
            f=open(file_log, 'a')
            f.write('#######################################\n')
            f.write('>>>>>>>>> Hostname: ' + hostname + '\n')
            f.write('>>>>>>>>> IP Address: ' + ip_addr + '\n')
            f.write('>>>>>>>>> Commands: ' + cmd + '\n')
            f.write('>>>>>>>>> Global Configuration Commands: ' + cmds + '\n')
            f.write('#######################################\n')
            f.close()

            # Write to Error log
            file_error = os.path.join(path, "Log", "Error.txt")
            f=open(file_error, 'a')
            f.write('#######################################\n')
            f.write('>>>>>>>>> Hostname: ' + hostname + '\n')
            f.write('>>>>>>>>> IP Address: ' + ip_addr + '\n')
            f.write('>>>>>>>>> Commands: ' + cmd + '\n')
            f.write('>>>>>>>>> Global Configuration Commands: ' + cmds + '\n')
            f.write('#######################################\n')
            f.close()

            # Connect to device
            net_connect = my_connection(hostname, device, ip_addr, username, p, ep)
            if not net_connect:
                continue # Skip this node due to connection issues.
            prompt = net_connect.find_prompt()
            for command in commands:
                run_cmd(command, prompt, net_connect, hostname)
            for command in global_config_commands:
                run_en_cmds(command, prompt, net_connect, hostname)
            net_connect.disconnect()

            print("\n>>>>>>>>> End <<<<<<<<<\n\n")

            # Write to Log
            file_log = os.path.join(path, "Log", "log.txt")
            f=open(file_log, 'a')
            f.write('\n>>>>>>>>> End <<<<<<<<<\n\n')
            f.close()

            # Write to Error log
            file_error = os.path.join(path, "Log", "Error.txt")
            f=open(file_error, 'a')
            f.write('\n>>>>>>>>> End <<<<<<<<<\n\n')
            f.close()

# Main Appilication
def main():
    # Start Time
    start_time = datetime.now()
    read_csv_file()
    end_time = datetime.now()
    total_time = end_time - start_time

    print("The Total Elapsed Time is:")
    print(total_time)
    exit()

if __name__ == "__main__":
    main()
