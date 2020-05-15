#import numpy as np
#import pylab as pp
#from epanettools import epanet2 as epa
import inpClasses as inp
import os
import sys



#inp_filename = 'Example_Networks/CW.inp'
#SWMM_filename = 'Example_Networks/CW_SWMM.inp'

#### Creating the list of objects

inp_filename = sys.argv[1]
SWMM_filename = sys.argv[2]

inp_file = open(inp_filename,'r')
section = None          #Which section of the EPANET inp file are we currently reading
Net = 0
Net = inp.Network(os.path.splitext(os.path.basename(inp_filename))[0])
CurrentPattern = None
for line in inp_file:
    if line.startswith(';') or line.strip() == "":
        continue
    elif line.startswith('['):
        section = line.strip()
    else:
        vals = line.split()
        if section == '[TITLE]':
            Net.titles.append(inp.Title(line))

        elif section == '[JUNCTIONS]':
            try:
                Net.juncs.append(inp.Junc(vals[0], vals[1], vals[2],pattern=vals[3]))
            except:
                Net.juncs.append(inp.Junc(vals[0],vals[1],vals[2]))

        elif section == '[RESERVOIRS]':
            Net.reservoirs.append(inp.Reservoir(vals[0],vals[1]))

        elif section == '[TANKS]':
            Net.tanks.append(inp.Tank(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6]))

        elif section == '[PIPES]':
            Net.pipes.append(inp.Pipe(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7]))

        elif section == '[PUMPS]':
            Net.pumps.append(inp.Pump(vals[0],vals[1],vals[2],vals[3]))

        elif section == '[VALVES]':
            Net.valves.append(inp.Valve(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6]))

        elif section == '[TAGS]':
            Net.tags.append(inp.Tag(vals[0]))

        elif section == '[DEMANDS]':
            Net.demands.append(inp.Demand(vals[0],vals[1],vals[2],vals[3]))

        elif section == '[PATTERNS]':
            #print(vals[0],vals[1:])
            Name = vals[0]
            if Name == CurrentPattern:
                firstInstance = False
            else:
                firstInstance = True
            CurrentPattern = Name
            Net.patterns.append(inp.Pattern(vals[0],vals[1:],firstInstance))

        elif section == '[CURVES]':
            Net.curves.append(inp.Curve(vals[0],vals[1],vals[2]))

        elif section == '[CONTROLS]':
            Net.controls.append(inp.Control(line))

        elif section == '[EMITTERS]':
            Net.emitters.append(inp.Emitter(vals[0],vals[1]))

        elif section == '[COORDINATES]':
            Net.coordinates.append(inp.Coordinate(vals[0],vals[1],vals[2]))

        elif section == '[LABELS]':
            Net.labels.append(inp.Label(vals[0],vals[1],vals[2]))

        elif section == '[OPTIONS]':
            Net.options.append(inp.Options(vals[0],vals[1]))

        elif section == '[VERTICES]':
            Net.vertices.append(inp.Vertice(vals[0],vals[1],vals[2]))
inp_file.close()

out_file = open(SWMM_filename,'w')
####  Title
out_file.write('[TITLE]\n')
out_file.write(';;Project Title/Notes\n')
for line in Net.titles:
    out_file.write(line.text)
out_file.write('Converted using pyEPANETtoSWMM\n')
out_file.write('\n')

#### Junctions
out_file.write('[JUNCTIONS]\n')
out_file.write(';;Name\t\t\tElevation\t\t\tMaxDepth\t\t\tInitDepth\t\t\tSurDepth\t\t\tAponded\n')
for junc in Net.juncs:
    out_file.write('\t\t\t'.join(junc.SWMM_writer())+'\n')
out_file.write('\n')

#### Inflows / Demands
out_file.write('[INFLOWS]\n')
out_file.write(';;Node           Constituent      Time Series      Type     Mfactor  Sfactor  Baseline Pattern\n')
for demand in Net.demands:
    out_file.write('\t\t\t'.join(demand.SWMM_writer())+'\n')
for junction in Net.juncs:
    if float(junction.demand) != 0:
        out_file.write('\t\t\t'.join(junction.SWMM_demand_writer()) + '\n')
out_file.write('\n')

#### Storage
out_file.write('[STORAGE]\n')
out_file.write(';;Name           Elev.    MaxDepth   InitDepth  Shape      Curve Name/Params            N/A      Fevap    Psi      Ksat     IMD   \n')
for reservoir in Net.reservoirs:
    out_file.write('\t\t\t'.join(reservoir.SWMM_writer()) + '\n')
for tank in Net.tanks:
    out_file.write('\t\t\t'.join(tank.SWMM_writer()) + '\n')
out_file.write('\n')

#### Conduits
out_file.write('[CONDUITS]\n')
out_file.write(';;Name           From Node        To Node          Length     Roughness  InOffset   OutOffset  InitFlow   MaxFlow  \n')
Sections = []
for pipe in Net.pipes:
    conduit,section = pipe.SWMM_writer()
    out_file.write('\t\t\t'.join(conduit)+'\n')
    Sections.append(section)
out_file.write('\n')

#### Sections
out_file.write('[XSECTIONS]\n')
out_file.write(';;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels    Culvert \n')
for section in Sections:
    out_file.write('\t\t\t'.join(section)+'\n')
out_file.write('\n')

#### Pumps
out_file.write('[PUMPS]\n')
out_file.write(';;Name             InNode             OutNode             Curve            initStatus \n')
for pump in Net.pumps:
    out_file.write('\t\t\t'.join(pump.SWMM_writer())+'\n')
out_file.write('\n')


#### Coordinates
out_file.write('[COORDINATES]\n')
out_file.write(';;Node           X-Coord            Y-Coord \n')
for coord in Net.coordinates:
    out_file.write('\t\t\t'.join(coord.SWMM_writer()) + '\n')
out_file.write('Dummy\t\t\t0\t\t\t0')
out_file.write('\n')

#### Outfalls
out_file.write('[OUTFALLS]\n')
out_file.write(';;Name           Elevation  Type       Stage Data       Gated    Route To         \n')
out_file.write('Dummy                0          FREE                        NO                      \n')
out_file.write('\n')

#### Labels
out_file.write('[LABELS]\n')
out_file.write(';;X-Coord         	Y-Coord           	Label \n')
for label in Net.labels:
    out_file.write('\t\t\t'.join(label.SWMM_writer())+ '\n')
out_file.write('\n')

#### Vertices
out_file.write('[VERTICES]\n')
out_file.write(';;Link             X-Coord          Y-Coord \n')
for vertex in Net.vertices:
    out_file.write('\t\t\t'.join(vertex.SWMM_writer())+ '\n')
out_file.write('\n')

#### Orifices
out_file.write('[ORIFICES]\n')
out_file.write(';;Name           From Node        To Node          Type         Offset     Qcoeff     Gated    CloseTime \n')
for valve in Net.valves:
    out_file.write('\t\t\t'.join(valve.SWMM_writer())+ '\n')
out_file.write('\n')



#### Patterns
out_file.write('[PATTERNS]\n')
out_file.write(';;Name             Type       Multipliers\n')
for pattern in Net.patterns:
    out_file.write('\t\t\t'.join(pattern.SWMM_writer())+'\n')
out_file.write('\n')

#### Options
out_file.write('[OPTIONS]\n')
out_file.write('FLOW_ROUTING         DYNWAVE\n')
out_file.write('\n')


out_file.write('START_DATE\t\t\t01/01/2020\n')
out_file.write('START_TIME           00:00:00\n')
out_file.write('REPORT_START_DATE\t\t\t01/01/2020\n')
out_file.write('REPORT_START_TIME    00:00:00\n')
out_file.write('END_DATE             01/01/2020\n')
out_file.write('END_TIME             06:00:00\n')











out_file.close()