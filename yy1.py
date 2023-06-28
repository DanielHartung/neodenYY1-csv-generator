import re

class nozzle:
    use = False
    component = 0
    head = 1
    drop_station = 0
    pick_station = 0

    def __init__(self):
        pass
class Feeder:
    id = 0
    part_name = str('None')
    part_value = str('None')
    part_package = str('None')
    part_height = str('None')
    part_nozzle = str('None')
    part_speed = str('None')
    part_mode = str('None')
    part_comment = str('None')

class Machine:
    '''
    File that contains all Feeder Information of the machine and all machine parameters
    '''
    feeders = []

    def __init__(self):
        self.read_machine_file('machine.csv')

    def read_machine_file(self, file):
        file1 = open(file, 'r')
        Lines = file1.readlines()

        for line in Lines:
            line = line.rstrip()
            result = re.split('[,;]', line)

            #if (result.len == 8):
            if result[0].isdigit():
                feeder = Feeder()
                feeder.id = result[0]
                feeder.part_name = result[1]
                feeder.part_value = result[2]
                feeder.part_package = result[3]
                feeder.part_height = result[4]
                feeder.part_nozzle = result[5]
                feeder.part_speed = result[6]
                feeder.part_mode = result[7]
                #feeder.part_comment = result[8]
                self.feeders.append(feeder)

    def write_machine_file(self):
        pass