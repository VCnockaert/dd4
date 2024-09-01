# ----------------------
# Written by Vincent Cnockaert as a submission to the Decode Demcon Challenge 4 (https://bit.ly/3yv0RmD).
# ----------------------

import random
import sys

# default settings
file_in = "in.txt"
file_out = ""
separator = " "
min_stages = 1
mode = "c"
modes = {"c": "concentrate", "d": "distribute", "r": "random"}
info = False
overview = False
occupancy = False

# --- input handling ---

# read argv arguments and apply settings accordingly
i = 1
while i < len(sys.argv):    
    match sys.argv[i]:
        case '-h':
            print("Festival schedule generator. Written for the Decode Demcon Challenge #4.\n")
            print("Arguments:")
            print("   -h        Display this help and exit.")
            print("   -c        Set schedule mode to 'concentrate'. (Default)")
            print("   -d        Set schedule mode to 'distribute'.")
            print("   -r        Set schedule mode to 'random'.")
            print("   -m N      Set minimum stages to N. (Default: 1)")
            print("   -i IN     Read input from file IN. (Default: in.txt)")
            print("   -o OUT    Write output to file OUT. (No output file by default)")
            print("   -v        Print general info.")
            print("   -p        Print stage overview.")
            print("   -s        Print stage occupancy.")
            exit()
        case '-c':
            mode = "c"
        case '-d':
            mode = "d"
        case '-r':
            mode = "r"
        case '-p':
            overview = True
        case '-s':
            occupancy = True
        case '-v':
            info = True
        case '-m':
            try:
                min_stages = abs(int(sys.argv[i + 1]))
                i = i + 1
            except (ValueError, IndexError):
                print("Expected an integer N after argument '-m'. Use '-h' for help.")
                exit()
        case '-i':
            try:
                file_in = sys.argv[i + 1]
                i = i + 1
            except IndexError:
                print("Expected an input file name after '-i'. Use '-h' for help.")
                exit()
        case '-o':
            try:
                file_out = sys.argv[i + 1]
                i = i +1
            except IndexError:
                print("Expected an output file name after '-o'. Use '-h' for help.")
                exit()
        case _:
            print(f"Invalid argument '{sys.argv[i]}'. Use '-h' to see valid arguments.")
            exit()
    i = i + 1

# read the input file
buff = []
try:
    with open(file_in, 'r') as file:
        buff = file.readlines()
except FileNotFoundError:
    print(f"Could not find specified file '{file_in}'. Use '-h' for help.")
    exit()

# split input lines and remove trailing returns
shows = [b[0:-1].split(separator) for b in buff]
while shows[-1] == ['']: shows = shows[0:-1]

# basic input sanity checks and cleaning
for s in range(len(shows)):
    try:
        shows[s][1] = int(shows[s][1])
        shows[s][2] = int(shows[s][2])
    except IndexError:
        print(f"Expected 3 entries (got {len(shows[s])}) at line {s + 1} in input file '{file_in}': {shows[s]}")
        exit()
    except ValueError:
        print(f"Could not parse value to integer at line {s + 1} in input file '{file_in}': {shows[s][1]} and {shows[s][2]}")
        exit()
    if shows[s][1] > shows[s][2]:
        print(f"Provided starting time slot is after ending time slot at line {s + 1} in input file '{file_in}': {shows[s][1]} > {shows[s][2]}")
        exit()
    if shows[s][1] < 1:
        print(f"Provided time slots should be greater then zero. Line {s + 1} in input file '{file_in}': {shows[s][1]} and {shows[s][2]}")
        exit()

# --- schedule algoritm ---

# sort shows based on starting time slot and modify internal order
shows = [[s[i] for i in [1, 2, 0]] for s in shows]
shows.sort()

# index 0: starting time slot
# index 1: ending time slot
# index 2: show nane

# distribute shows over stages, modify stage order list based on mode
stages = []
while (len(stages) < min_stages): stages.append([]) 
for show in shows:
    added = False
    stage_order = list(range(len(stages)))
    if "r" == mode:
        random.shuffle(stage_order)
    if "d" == mode:
        buff = [[len(stages[i]), i] for i in stage_order]
        buff.sort()
        stage_order = [b[1] for b in buff]
    for n in stage_order:
        if len(stages[n]) == 0:
            stages[n].append(show)
            added = True
            break
        if stages[n][-1][1] < show[0]:
            stages[n].append(show)
            added = True
            break
    if not added:
        stages.append([show])

# --- output handling ---
 
# print general info
if info:
    print("[Info]\n")
    print(f"input file: {file_in}")
    print(f"shows: {len(shows)}")
    print(f"minimum stages: {min_stages}")
    print(f"mode: {modes[mode]}")
    print(f"used stages: {len(stages)}")
    if len(file_out): print(f"output file: {file_out}")
    print("")

# print overview of all stages
if overview:
    print("[Stage overview]\n")
    i = 1
    for stage in stages:
        print(f" --- stage {i} ---");
        for show in stage:
            buff = show[2]
            while (len(buff) < 12): buff = buff +' '
            buff = buff + str(show[0])
            while (len(buff) < 16): buff = buff + ' '
            buff = buff + "to  " + str(show[1])
            print(buff)
        print("")
        i = i + 1

# print stage occupancy
if occupancy:
    print("[Stage occupancy]\n")
    max_slot = max([s[1] for s in shows])
    for n in range(len(stages)):
        buff = f"stage {n + 1}:"
        while (len(buff) < 10): buff = buff + ' '
        shows = stages[n]
        if len(shows) == 0:
            buff = buff + max_slot * '-'
        else:
            buff = buff + (shows[0][0] - 1) * '-'
            for s in range(len(shows)):
                buff = buff + (shows[s][1] - shows[s][0] + 1) * '#'
                if s + 1 < len(shows):
                    buff = buff + (shows[s+1][0] - shows[s][1] - 1) * '-'
            buff = buff + (max_slot - shows[-1][1]) * '-'
        print(buff)
    print("")

# write to output file
if len(file_out) > 0:
    buff = []
    i = 1
    for stage in stages:
        for show in stage:
            buff.append(separator.join([f"stage_{i}", show[2], str(show[0]), str(show[1])]) + "\n")
        i = i + 1
    with open(file_out, 'w') as file:
        file.writelines(buff)

