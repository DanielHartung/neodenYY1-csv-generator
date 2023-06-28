# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from generator import *
from Part import *
from yy1 import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #generate machine class with all Feeders
    machine = Machine()
    #generate Parts class with all Parts
    eaglef = EagleFile("SmartCity.mnt")
    #check if machine has the related parts


    partlist = []
    for p in eaglef.parts:
        part = YY1Part()
        part.designator = p.partname
        part.comment = p.value
        part.footprint = p.body
        part.mid_x = p.pos_x
        part.mid_y = p.pos_y
        part.rotation = p.rotation
        part.head = 1
        part.feeder = 1
        part.speed = 100
        part.pick_high = 0
        part.place_high = 0
        part.mode = 1
        part.skip = False
        partlist.append(part)

    g = Generator(partlist)
    g.verify_parts(machine, eaglef)
    #g.generate("","SmartBin")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
