#import numpy as np
#import pylab as pp
#from epanettools import epanet2 as epa
import inpClasses as inp

inp_filename = 'Example_Networks/Net1.inp'

#### Creating the list of objects
Juncs = []
Reservoirs = []
Tanks = []
Pipes = []
Pumps = []
Valves = []
Tags = []
Demands = []
Patterns = []
Curves = []
Controls = []
Emitters = []
Coordinates = []
Vertices = []
Labels = []
Option = []


inp_file = open(inp_filename,'r')
section = None          #Which section of the EPANET inp file are we currently reading
for line in inp_file:
    if line.startswith(';') or line.strip() == "":
        continue
    elif line.startswith('['):
        section = line.strip()
    else:
        vals = line.split()
        if section == '[JUNCTIONS]':
            Juncs.append(inp.Junc(vals[0],vals[1],vals[2]))

        elif section == '[RESERVOIRS]':
            Reservoirs.append(inp.Reservoir(vals[0],vals[1]))

        elif section == '[TANKS]':
            Tanks.append(inp.Tank(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6]))

        elif section == '[PIPES]':
            Pipes.append(inp.Pipe(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7]))

        elif section == '[PUMPS]':
            Pumps.append(inp.Pump(vals[0],vals[1],vals[2],vals[3]))

        elif section == '[VALVES]':
            Valves.append(inp.Valve(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6]))
