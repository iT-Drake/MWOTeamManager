import re
from . import MECH_DATA
import csv

def read_mech_data():
    with open(MECH_DATA, newline='') as mech_data_file:
        mech_data = {}
        reader = csv.DictReader(mech_data_file)
        for row in reader:
            mech_data[row['Name']] = row

        return mech_data

mech_data = read_mech_data()

def parse_mechlist(new_mechlist):
    mechlist = dict()
    re_mech_line = re.compile('\w+-\w+')
    re_special_variant = re.compile('\(\w+\)')
    for line in new_mechlist.splitlines():
        line = line.strip()
        if not line:
            continue

        if not re_mech_line.match(line):
            continue

        line = re_special_variant.sub('', line)
        mech_row = mech_data.get(line)
        if mech_row and not line in mechlist:
            mechlist[line] = mech_row
            omni = mech_row.get('OmniMech')
            if omni == 'TRUE':
                chassis = mech_row.get('Chassis')
                name = f"{chassis}-ANY"
                omni_row = mech_data.get(name)
                if omni_row and not name in mechlist:
                    mechlist[name] = omni_row

    return mechlist

def get_mech_data():
    return mech_data
