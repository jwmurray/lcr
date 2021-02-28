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
# move_ins = lcr.members_moved_in(months)
# for member in move_ins:
#     if member['householdPosition'] == 'Head of Household':
#         print("{}: {}, {}, in {}".format(member['name'], member['address'], member['age'], member['moveDate']))
#     else:
#         print("{}: {}, {} in {}".format(member['name'], member['address'], member['age'], member['moveDate']))
# 
if False:
    members_json = lcr.member_list()
    member_list = []
    for member in member_list:
        member_list.append(member)
    member_list.sort(key=lambda s: s['birthDateSort'])

    for member in member_list:
        print("{} ({}, {}): Action: {}".format(member['name'], member['age'], member['birthDateFormatted'], member['ailActionType']))



# time.sleep(8)

else:
    interviews = lcr.action_interview_list()
    interview_list = []
    semi_annual_interview_list = []
    for member in interviews:
        if "ANNUAL_INTERVIEW" == member['ailActionType']:
            interview_list.append(member)
        if "SEMIANNUAL_INTERVIEW" == member['ailActionType']:
            semi_annual_interview_list.append(member)
    interview_list.sort(key=lambda s: s['birthDateSort'])
    semi_annual_interview_list.sort(key=lambda s: s['birthDateSort'])

    for member in interview_list:
        print("{} ({}, {}): Action: {}".format(member['name'], member['age'], member['birthDateFormatted'], member['ailActionType']))


    for member in semi_annual_interview_list:
        print("{} ({}, {}): Action: {}".format(member['name'], member['age'], member['birthDateFormatted'], member['ailActionType']))

# time.sleep(8)

