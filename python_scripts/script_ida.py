# Original author: Olivier Decourbe, thanks ;)
# Modified by: Lesly-Ann Daniel

import subprocess
import os.path
from idautils import *
from idc import *

# Trace options #
trace_path = "/tmp/binsec/traces/"
coverage_color = 0x99e6ff
explor_color = 0xdd0000
secure_color = 0x00dd00
insecure_color = 0x0000dd
timeout_color = 0x00ffff
coverage_file = trace_path + "tracecoverage_0"
explor_file = trace_path + "traceexplor_0"
secure_file = trace_path + "tracesecure_0"
insecure_file = trace_path + "traceinsecure_0"
timeout_file = trace_path + "tracetimeout_0"


# Function from:
# https://unit42.paloaltonetworks.com/using-idapython-to-make-your-life-easier-part-4/
def get_new_color(current_color):
    colors = [0x99e6ff, 0x33ccff, 0x00ace6, 0x0086b3]
    if current_color == 0xFFFFFFFF:
        return colors[0]
    if current_color in colors:
        pos = colors.index(current_color)
        if pos == len(colors)-1:
            return colors[pos]
        else:
            return colors[pos+1]
    return current_color


def color_trace(trace_file, color):
    print("----- ------ ----- ------")
    print("Current trace file: " + trace_file)
    if os.path.isfile(trace_file): 
        cur_trace = open(trace_file, 'r')
        for line in cur_trace:
            for addr in line.split():
                addr = int(addr, 16)
                SetColor(addr, CIC_ITEM, color)
    print("----- ------ ----- ------")


print("=== Script Begin ===")

# Counters #
local_counter = 0
total_counter = 0
uniq_addr_list = []

# Reset all colors
# TODO !

# Gather all traces related to the current binary #
# Get the name of the current file
# current_file = idaapi.get_root_filename()
# get the folder where the traces are
try:
    dir_res = subprocess.check_output(["ls " + trace_path + "path_*"], shell=True)
    dir_res.replace("\n", " ")
    sp_dir_res = dir_res.split()
    print("sp_dir_res = " + str(sp_dir_res))

    # For each trace, color hitted instructions #
    for trace_name in sp_dir_res:
        # trace_name = one_trace.split("/")[3]
        print("----- ------ ----- ------")
        print("Current trace file: " + trace_name)
        cur_trace = open(trace_name, 'r')
        for line in cur_trace:
            for addr in line.split():
                local_counter += 1
                addr = int(addr, 16)
                current_color = GetColor(addr, CIC_ITEM)
                new_color = get_new_color(current_color)
                SetColor(addr, CIC_ITEM, new_color)
        print("Mark instructions for this trace : " + str(local_counter))
        print("----- ------ ----- ------")
        local_counter = 0
        uniq_addr_list = []
except (subprocess.CalledProcessError):
    pass

color_trace(coverage_file, coverage_color)
color_trace(explor_file, explor_color)
color_trace(secure_file, secure_color)
color_trace(insecure_file, insecure_color)
color_trace(timeout_file, timeout_color)

print("=== Script End ===")
