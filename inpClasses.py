class Network:
    def __init__(self,Name,Title=[],Juncs=[],Reservoirs=[],Tanks=[],Pipes=[],Pumps=[],Valves=[],Tags=[],Demands=[],Patterns=[],Curves=[],Controls=[],Emitters=[],Coordinates=[],Vertices=[],Labels=[],Options=[]):
        self.name = Name
        self.titles = Title
        self.juncs = Juncs
        self.reservoirs = Reservoirs
        self.tanks = Tanks
        self.pipes = Pipes
        self.pumps = Pumps
        self.valves = Valves
        self.tags = Tags
        self.demands = Demands
        self.patterns = Patterns
        self.curves = Curves
        self.controls = Controls
        self.emitters = Emitters
        self.coordinates = Coordinates
        self.labels = Labels
        self.options = Options
        self.vertices = Vertices

    #def SWMM_file(self,filename):
    #    self.filename = filename
    #    f = open(self.filename,w)



class Junc:
    """
    This is the junction class, it allows you to input data from a EPANET format and has functions for writing to a SWMM format.
    """
    def __init__(self,id,elevation,demand,pattern = None):
        self.id = id
        self.elev = elevation
        self.demand = demand
        self.pattern = pattern

    def SWMM_writer(self,max_depth = 1000,init_depth = 0,surcharge_depth = 0,ponded_area=0):
        """
        This function will produce a list formatted in the order required by SWMM inp files.
        It uses junction ids and elevations previously read into the class and the following additional optional inputs:
        :param max_depth:   If not specified will default to
        :param init_depth:  If not specified will default to 0
        :param surcharge_depth:  If not specified will default to 0
        :param ponded_area:  If not specified will default to 0
        :return list formatted in SWMM junction format:
        """
        junction = [self.id,str(self.elev),str(max_depth),str(init_depth),str(surcharge_depth),str(ponded_area)]
        return junction

    def SWMM_demand_writer(self,Constit='FLOW', timeSeries='""', pattType='FLOW', mFactor=1.0, sFactor=1.0):
        demand = [str(self.id), str(Constit), str(timeSeries), str(pattType), str(mFactor), str(sFactor),
                      str(-float(self.demand)), str(self.pattern)]
        return demand

class Title:
    def __init__(self,text):
        self.text = text

class Reservoir:
    def __init__(self, id, head):
        self.id = id
        self.head = head

    def SWMM_writer(self,maxDepth=1000,initDepth=1,shape='FUNCTIONAL',param1=10000,param2=0,param3=1000000000):
        """
        Creates a tank with a very very large area so that it won't change with outflow, as close as I can get to a true reservoir
        initDepth needs to be bigger than 0 to ensure there is water in the res.
        by default it takes the elevation to be EPANET.head - 1 with initial Depth = 1.
        :param maxDepth:
        :param initDepth:
        :param shape:
        :param param1:
        :param param2:
        :param param3:
        :return:
        """
        res = [str(self.id),str(float(self.head)-initDepth),str(maxDepth),str(initDepth),str(shape),str(param1),str(param2),str(param3)]
        return res

class Tank:
    def __init__(self, id, elevation, initLevel, minLevel, maxLevel, diameter, minVol, volCurve = None):
        self.id = id
        self.elev = elevation
        self.initLevel = initLevel
        self.minLevel = minLevel
        self.maxLevel = maxLevel
        self.diameter = diameter
        self.minVol = minVol
        self.volCurve = volCurve
        self.area = 3.1415 * float(self.diameter)**2 / 4.

    def SWMM_writer(self, shape='FUNCTIONAL', param1=0, param2=0):
        tank = [str(self.id), str(self.elev), str(self.maxLevel), str(self.initLevel), str(shape), str(param1), str(param2),
               str(self.area)]
        return tank

class Pipe:
    def __init__(self, id, node1, node2, length, diameter, roughness, minorLoss, status):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.length = length
        self.diameter = float(diameter)/1000.
        self.roughness = roughness
        self.minorLoss = minorLoss
        self.status = status

    def SWMM_writer(self,inHeight = 0,outHeight=0,initFlow=0,Geom2=0,Geom3=0,Geom4=0,Barrels=1):
        conduit = [str(self.id),str(self.node1),str(self.node2),str(self.length),str(self.roughness),str(inHeight),str(outHeight),str(initFlow)]
        section = [str(self.id),'CIRCULAR',str(self.diameter),str(Geom2),str(Geom3),str(Geom4),str(Barrels)]
        return conduit, section
class Pump:
    def __init__(self, id, node1, node2, parameter):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.parameter = parameter

    def SWMM_writer(self,curve = '',initStatus='ON'):
        pump = [str(self.id),str(self.node1),str(self.node2),str(curve),str(initStatus)]
        return pump

class Valve:
    def __init__(self, id, node1, node2, diameter, type, setting, minorLoss):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.diameter = diameter
        self.type = type
        self.setting = setting
        self.minorLoss = minorLoss

    def SWMM_writer(self,type = 'SIDE',offset = 0,Qcoeff=0.65,gated='NO',closeTime=0):
        valve = [str(self.id),str(self.node1),str(self.node2),str(type),str(offset),str(Qcoeff),str(gated),str(closeTime)]
        return valve
class Tag:
    def __init__(self):
        self.id

class Demand:
    def __init__(self,junction, demand, pattern, category):
        self.junction = junction
        self.demand = demand
        self.pattern = pattern
        self.category = category

    def SWMM_writer(self,Constit='FLOW',timeSeries='""',pattType='FLOW',mFactor=1.0,sFactor=1.0):
        demand = [str(self.junction),str(Constit),str(timeSeries),str(pattType),str(mFactor),str(sFactor),str(-float(self.demand)),str(self.pattern)]
        return demand
class Pattern:
    def __init__(self,id,multipliers,firstInstance=True):
        self.id = id
        self.multipliers = multipliers
        self.firstInstance = firstInstance

    def SWMM_writer(self,Type = 'HOURLY'):
        demand = [str(self.id)]
        if self.firstInstance == True:
            demand.append(str(Type))
        for multi in self.multipliers:
            demand.append(str(multi))

        return demand
class Curve:
    def __init__(self, id, X,Y):
        self.id= id
        self.x_Value = X
        self.y_Value = Y

class Control:
    def __init__(self,rule):
        self.rule = rule

class Emitter:
    def __init__(self,junction, coefficient):
        self.junction = junction
        self.coefficient = coefficient

class Coordinate:
    def __init__(self, node, X, Y):
        self.node = node
        self.x_Coord = X
        self.y_Coord = Y
    def SWMM_writer(self):
        coord = [str(self.node),str(self.x_Coord),str(self.y_Coord)]
        return coord
class Vertice:
    def __init__(self,link, X,Y):
        self.link = link
        self.x_Coord = X
        self.y_Coord = Y

    def SWMM_writer(self):
        coord = [str(self.link), str(self.x_Coord), str(self.y_Coord)]
        return coord

class Label:
    def __init__(self, X, Y, label):
        self.x_Coord = X
        self.y_Coord = Y
        self.label = label

    def SWMM_writer(self):
        label = [str(self.x_Coord),str(self.y_Coord),str(self.label)]
        return label

class Options:
    def __init__(self,option, value):
        self.option = option
        self.value = value

    def SWMM_writer(self):
        if self.option == 'Units':
            self.option = 'FLOW_UNITS'
        option_string = str(self.option)+'\t\t\t'+str(self.value)+'\n'
        return option_string