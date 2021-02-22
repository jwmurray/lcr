#!/usr/bin/env python3

from lcr import API as LCR

lcr = LCR("gardenway", "lancer83", 259950)

months = 5
move_ins = lcr.members_moved_in(months)

for member in move_ins:
    if member['householdPosition'] == 'Head of Household':
        print("{}: {}, {}, in {}".format(member['name'], member['address'], member['age'], member['moveDate']))
    else:
        print("{}: {}, {} in {}".format(member['name'], member['address'], member['age'], member['moveDate']))
