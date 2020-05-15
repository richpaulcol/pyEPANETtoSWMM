class Junc:
    def __init__(self,id,elevation,demand,pattern = None):
        self.id = id
        self.elev = float(elevation)
        self.demand = demand

class Reservoir:
    def __init__(self, id, head):
        self.id = id
        self.head = head

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

class Pipe:
    def __init__(self, id, node1, node2, length, diameter, roughness, minorLoss, status):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.length = length
        self.diameter = diameter
        self.roughness = roughness
        self.minorLoss = minorLoss
        self.status = status

class Pump:
    def __init__(self, id, node1, node2, parameter):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.parameter = parameter

class Valve:
    def __init__(self, id, node1, node2, diameter, type, setting, minorLoss):
        self.id = id
        self.node1 = node1
        self.node2 = node2
        self.diameter = diameter
        self.type = type
        self.setting = setting
        self.minorLoss = minorLoss


class Tag:
    def __init__(self):
        self.id

class Demand:
    def __init__(self,junction, demand, pattern, category):
        self.junction = junction
        self.demand = demand
        self.pattern = pattern
        self.category = category

class Pattern:
    def __init__(self,id,multipliers):
        self.id = id
        self.multipliers = multipliers

class Curve:
    def __init__(self, id, X,Y):
        self.id= id
        self.x_Value = X
        self.y_Value = Y

class Control:
    def __init(self,rule):
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

class Vertice:
    def __init__(self,link, X,Y):
        self.link = link
        self.x_Coord = X
        self.y_Coord = Y

class Label:
    def __init__(self, X, Y, label):
        self.x_Coord = X
        self.y_Coord = Y
        self.lable = label

class Options:
    def __init__(self,option, value):
        self.option = option
        self.value = value