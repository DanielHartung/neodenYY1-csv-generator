# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import Part
from generator import *
from Part import *
from yy1 import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #generate machine class with all Feeders
    machine = Machine()
    #generate Parts class with all Parts
    fusionfile = FusionFile("SmartBin v22.mnt")
    #check if machine has the related parts
    machine.generate_placeable_partlist(fusionfile.part_list())

    placeable_parts = machine.get_placeable_parts()
    nozzle_changes = machine.get_nozzle_changes()

    print('No parts: '+str(len(fusionfile.parts)))
    print('placeable parts: '+str(len(placeable_parts)))

    print('Following parts are not placeable:')
    for part in fusionfile.part_list():
        if not part.placeable:
            print(part.name +' '+part.value+' '+part.package)

    g = Generator(placeable_parts, nozzle_changes)
    g.generate("","SmartBin")
    #print("Generation completed")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
