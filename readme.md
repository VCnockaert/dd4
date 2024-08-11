# Festival Schedule Generator

## Info

This program was written by Vincent Cnockaert as a submission to the [Decode Demcon Challenge #4](https://bit.ly/3yv0RmD). The goal was to create a planning program which takes a list of shows, and their start and end timeslots, and generates a planning on different stages in such a way that shows dont overlap.

## Usage

The festival schedule generator is written using Python 3.11.9. The program reads in an ASCII text file containing the start and end timeslots of an arbitrary amount of shows. These shows are then scheduled on as many different stages as required. The format of the input file is the same as inducated in the challenge description:

```
show_1 29 33
show_2 2 9
show_3 44 47
...
```

The shows are separated by new-lines (`"\n"` or `"\r\n"`) and the show name, start timeslot and end timeslot are separated by spaces (`" "`).

The program can be run by passing the `main.py` script to the Python 3 interpreter. For most systems, the Python 3 interpreter is aliased as `python3`. The scheduler has a build-in help function which can be accessed by using '-h' as a command line argument. In Linux terminal or from Windows command line:

```
python3 main.py -h
```

This outputs following help page:

```
Festival schedule generator. Written for the Decode Demcon Challenge #4.

Arguments:
   -h        Display this help and exit.
   -c        Set schedule mode to 'concentrate'. (Default)
   -d        Set schedule mode to 'distribute'.
   -r        Set schedule mode to 'random'.
   -m N      Set minimum stages to N. (Default: 1)
   -i IN     Read input from file IN. (Default: in.txt)
   -o OUT    Write output to file OUT. (No output file by Default)
   -v        Print general info.
   -p        Print stage overview.
   -s        Print stage occupancy.
```

The help page provides an overview of all available arguments and how they are used.

### Input

The `-i` argument can be used to provide the name of the input file that should be read. For example:

```
python3 main.py -i myfile.txt
```

If this argument is omitted, the default input file name `in.txt` will be used.

### Output

The arguments `-v`, `-p` and `-s` can be used to control what information is printed to the command line or terminal. By default, no output is provided. Following information can be printed:

 - General info (`-v`): Provides information such as mode, amount of shows and amount of stages required.
 - Stage overview (`-p`): Prints all stages, which shows play on them and for what timeslots.
 - Stage occupancy (`-s`): Generates a visual overview of all stages and at which time a show is playing and at which time no show is playing.

Providing all possible output information can thus be done using:

```
python3 main.py -v -p -s
```

The `-o` argument can be used to write the generated stage schedule to an output file. This file has the same format as the input file but also contains the stage at which each show is schedules, additional to the start and end timeslots.

For example:

```
python3 main.py -v -o out.txt
```

This command will generate a schedule based on the default input file `in.txt` and write the schedule to the specified output file `out.txt`. In addition, the stage occupancy is written to the command line or terminal to get a visual overview of the distribution of shows over all stages.

### Schedule mode

The arguments `-c`, `-d` and `-r` can be used to set the mode of the schedule algoritm: 

 - Concentrate (`-c`): Shows are scheduled is such a way that stages are filled as much as possible, leaving some stages that might only host a single show.
 - Distribute (`-d`): Tries to distribute shows over all stages equally, makes sure all stages host a similar number of shows.
 - Random (`-r`): Random schedules shows. The result will be somewhat in between the `-c` and `-d` modes.

The first two modes provide deterministic results. The third mode provides a stochastic result that will be different each time the program is run. It can thus be used to explore different possible schedules.

### Number of stages

The `-m` argument can be used to provide the minimum number of stages that should be used to schedule the shows on. Stages will however be added when required. Specifying the minimum number of stages can also lead to stages to be left without shows. If the number of stages is, for example, greater then the number of shows.

## Program structure

The program consists of three parts, the input handler, the algoritm itself and the output handler. The schedule algoritm only consists out of a small portion of the program, only 32 of the 196 lines of python code. The remainder is input and output handling.

## The schedule algoritm

First, all shows are sorted, based on their start time slot. Next, the algoritm loops over all sorted shows and stages and adds shows to a stage if the show fits behind the current stage schedule. The priority of which stages are considered first for adding shows, is controlled by the schedule mode. If none of the existing stages can accomodate the show, a new stage is added.

### Complexity

When the amount of shows is very large, in comparison to the amount of required stages, the complexity of the program lays in sorting the shows based on their starting time. This is done using the build-in `sort()` function which has nlog(n) time complexity. This is thus also the complexity of the algoritm for large input data sets.

## Contact

vincent.cnockaert@novonormali.com

