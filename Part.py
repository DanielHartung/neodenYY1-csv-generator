import re
from yy1 import *

class YY1Part:
    designator = str("R1")
    comment = str("1k")
    footprint = str("0603D")
    mid_x = 30.93
    mid_y = 17.68
    rotation = -90.0
    head = 1
    feeder = 1
    speed = 100
    pick_high = 0
    place_high = 0
    mode = 1
    skip = False

    def __init__(self):
        self.name = "Partname"

class EaglePart:
    '''
    Class that represents a Eagle part
    '''
    partname = str("C1")
    value = str("0,47µ")
    body = str("C0805")
    pos_x = 6.35
    pox_y = 53.34
    rotation = 270


class Fusion:
    parts = []

    def __init__(self, path):
        self.parse(path)

    def parse(self, path):
        file1 = open(path, 'r')
        Lines = file1.readlines()

        for line in Lines:
            result = re.search(r"(\S+);(\S+)\s+(\S+)\s(\S+)\s+(\S+)\s(.*)", line)

            if (result):
                part = EaglePart()
                part.partname = result.group(1)
                part.pos_x = result.group(2)
                part.pos_y = result.group(3)
                part.rotation = result.group(4)
                part.value = result.group(5)
                part.body = result.group(6)
                self.parts.append(part)


class EagleFile:
    parts = []

    def __init__(self, path):
        self.parse(path)

    def parse(self, file):
        file1 = open(file, 'r')
        Lines = file1.readlines()

        for line in Lines:
            result = re.search(r"(\S+)\s+(\S+)\s+(\S+)\s(\S+)\s+(\S+)\s(.*)", line)

            if(result):
                part = EaglePart()
                part.partname = result.group(1)
                part.pos_x = result.group(2)
                part.pos_y = result.group(3)
                part.rotation = result.group(4)
                part.value = result.group(5)
                part.body = result.group(6)
                self.parts.append(part)
