# Header
print('')
print('Script Name:             | project.py 101')
print('File Date:               | 2017-12')
print('Author:                  | Chris Fong')
print('Version:                 | 0.1')
print('Python Version:          | 3.x')
print('Tab:                     | 4 spaces')
print('Library Dependencies:    | netmiko; csv; getpass')
print('')
# End Header

# |----------------------------80 Character Ruler------------------------------|

'''
README:

Expected CSV Headers/Columns
HOSTNAME,IP_ADDRESS,IOS_TYPE


'''

# Import Library Dependencies
import getpass
import csv

from netmiko import ConnectHandler


# Define Global Variables
# Input Username

username = str(input("Please Enter your username: "))
print('The username you entered was: ', username)

# Input password without echoing password
try:
    p = getpass.getpass(prompt='Please enter your password: ')
except Exception as error:
    print('ERROR: No password entered', error)
else:
    print('Password has been accepted.')

# Manipulate variables to add an apostrophe
username="'"+username+"'"
p="'"+p+"'"

# Input CSV File Name
file_name=str(input("Please Enter the input CSV file name: "))
print('Input CSV file:', file_name)
# enddef


# Open CSV file
def r_cvs_file():
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        hostnames = []
        ip_addrs = []
        devices = []
        for row in readCSV:
            hostname = [row[0]]
            ip_addr = [row[1]]
            device = [row[2]]

            # Change from list to string
            hostname = str(hostname)
            ip_addr = str(ip_addr)
            device = str(device)

            # Manipulate string to remove brackets
            hostname = hostname.replace('[','').replace(']','')
            ip_addr = ip_addr.replace('[','').replace(']','')
            device = device.replace('[','').replace(']','')

            # Testing
            print(hostname)
            print(ip_addr)
            print(device)
            print(username)
            print(p)

            # Connect
            net_connect = ConnectHandler(device_type=device, ip=ip_addr, username=username, password=p)
            net_connect.find_prompt()
            output = net_connect.send_command("show run | in hostname")
            print(output)
# enddef


def main():
    print ('') 
    print ('')
    r_cvs_file()
    exit()

if __name__ == "__main__":
    main()
