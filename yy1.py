#from main import DEBUG
from Part import unit_norminal, YY1Part, prenum, Part
import re

DEBUG = True

typing_list = ['resistor',
               'capacitor']

class nozzle:
    'use'
    use = False
    component = 0
    'Head of yy1 1 or 2'
    head = 1
    drop_station = 0
    pick_station = 0

    def __init__(self):
        pass

class Feeder:
    id = 0
    part_name = str('None')
    part_value = str('None')
    part_nvalue = 0.0
    part_package = str('None')
    part_height = str('None')
    part_nozzle = str('None')
    part_speed = str('None')
    part_mode = str('None')
    part_comment = str('None')

class Machine:
    '''
    File that contains all Feeder Information of the machine and all machine parameters
    Tape Feeders: 1 - 52
    Flexible Feeders: 53 - 80
    Bulk Feeders: 81 - 99
    '''
    feeders = []
    placeable_parts = []
    nozzle_changes = []

    def __init__(self, filename):
        self.read_machine_file(filename)

    def get_placeable_parts(self):
        return self.placeable_parts

    def get_nozzle_changes(self):
        return self.nozzle_changes

    def read_machine_file(self, file):
        if DEBUG:
            print('######### Read Machine file ###############')
        file1 = open(file, 'r')
        Lines = file1.readlines()

        for line in Lines:
            line = line.rstrip()
            result = re.split('[,;]', line)

            if result[0].isdigit():
                feeder = Feeder()
                feeder.id = result[0]
                feeder.part_name = result[1]
                feeder.part_value = result[2]
                if feeder.part_name in typing_list:
                    feeder.part_nvalue = prenum(feeder.part_value)
                else:
                    feeder.part_nvalue = feeder.part_value
                feeder.part_package = result[3]
                feeder.part_height = result[4]
                feeder.part_nozzle = result[5]
                feeder.part_speed = result[6]
                feeder.part_mode = result[7]
                #feeder.part_comment = result[8]
                if feeder.part_name:
                    if DEBUG == True:
                        print(f'add Feeder: {feeder.id} Part: {feeder.part_name} Value: {feeder.part_value}')
                    self.feeders.append(feeder)

        if DEBUG:
            print('######### Machine file readed ###############')

    def write_machine_file(self):
        pass

    def create_placement(self, part, feeder, placeable):
        yy1part = YY1Part(part.name)
        yy1part.designator = part.name
        yy1part.comment = part.nvalue
        yy1part.footprint = feeder.part_package
        yy1part.mid_x = part.pos_x
        yy1part.mid_y = part.pos_y
        yy1part.rotation = part.rotation
        yy1part.nozzle = feeder.part_nozzle
        yy1part.head = 1
        yy1part.feeder = feeder.id
        yy1part.speed = feeder.part_speed
        yy1part.pick_high = feeder.part_height
        yy1part.place_high = feeder.part_height
        yy1part.mode = feeder.part_mode
        yy1part.skip = placeable

        self.placeable_parts.append(yy1part)

    def find_feeder(self, value, package):
        for feeder in self.feeders:
            #check value and package
            if str(feeder.part_nvalue) == str(value) and feeder.part_package == package:
                return feeder        
        
        return None

    def generate_placeable_partlist(self, parts):
        '''
        1. Generate placeable parts according the value and the package.
        2. Order the placeable parts that all parts with the same needle are behind each other for less
           nozzle switches (have only limited).
        3. Order parts with the same component so that the both heads can be used for quick placement
        4. Set the used head alternately for double the placing for the first nozzle
        5. Set the switch for the nozzle for the part that uses other nozzels
        '''
        dummy_nozzle_change = False
        #check each part
        #1
        for part in parts:
            generated = False
            #self.create_placement(part, self.feeders[0])
            #check value
            for feeder in self.feeders:
                #check value and package
                if str(feeder.part_nvalue) == str(part.nvalue) and feeder.part_package == part.package:
                    self.create_placement(part,feeder, True)
                    part.placeable = True
                    break

        #2 Sort for Feeder
        self.placeable_parts.sort(key=lambda x: x.feeder)
        #3 Sort for Nozzle
        self.placeable_parts.sort(key=lambda x: x.nozzle)

        #4
        current_head = 1
        for part in self.placeable_parts:
            if part.nozzle == '1':
                part.head = str(current_head)
                current_head = current_head + 1

                if current_head > 2:
                    current_head = 1

        #5 Switch nozzle if required
        current_nozzle = 1
        current_component = 0
        for part in self.placeable_parts:
            current_component = current_component + 1
            if part.nozzle != str(current_nozzle):
                dummy_nozzle_change = True

                nz = nozzle()
                nz.use = True
                nz.head = 1
                nz.drop_station = current_nozzle
                nz.pick_station = part.nozzle
                nz.component = current_component
                self.nozzle_changes.append(nz)
                current_nozzle = part.nozzle

        if dummy_nozzle_change:
            dummypart = Part()
            dummyfeeder = Feeder()

            dummypart.name = "Dummy"
            dummypart.pos_x = 50.0
            dummypart.pos_y = 10.0
            dummypart.value = 0

            dummyfeeder.id = 99
            dummyfeeder.part_height = 10
            dummyfeeder.part_value = 0
            dummyfeeder.part_nozzle = 1
            dummyfeeder.part_speed = 50
            dummyfeeder.part_mode = 0
            self.create_placement(dummypart, dummyfeeder, True)

            ## create nozzle change for dummy
            nz = nozzle()
            nz.use = True
            nz.head = 1
            nz.drop_station = current_nozzle
            nz.pick_station = 1 #TODO: Nozzle change check correct position
            nz.component = current_component
            self.nozzle_changes.append(nz)