from lcr import API as LCR

lcr = LCR("gardenway", "lancer83", 259950)

months = 5
move_ins = lcr.members_moved_in(months)

for member in move_ins:
    print("{}: {}".format(member['spokenName'], member['textAddress']))