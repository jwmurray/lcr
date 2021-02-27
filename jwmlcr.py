#!/usr/bin/env python3
import time

from lcr import API as LCR


from configparser import ConfigParser
config = ConfigParser()

config.read('/Users/jmurray/config.ini')
# config.add_section('default')
# config.set('default', 'username', 'username_text')
# config.set('default', 'password', 'password_text')
username = config.get('default', 'username')
password = config.get('default', 'password')
unitNumber = int(config.get('default', 'unit'))

# with open('/Users/jmurray/config.ini', 'w') as f:
#     config.write(f)

lcr = LCR(username, password, unitNumber)

# time.sleep(1)
months = 5
move_ins = lcr.members_moved_in(months)
# time.sleep(8)
for member in move_ins:
    if member['householdPosition'] == 'Head of Household':
        print("{}: {}, {}, in {}".format(member['name'], member['address'], member['age'], member['moveDate']))
    else:
        print("{}: {}, {} in {}".format(member['name'], member['address'], member['age'], member['moveDate']))
