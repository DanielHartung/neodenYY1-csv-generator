import re

class prenum:
    '''
    number wit prefix
    '''
    num = 0
    multi = 0

    def __init__(self, number:str):
        self.simplyfiy(number)

    def __str__(self):
        prefix = ''

        if self.multi == 9:
            prefix = 'G'
        elif self.multi == 6:
            prefix = 'M'
        elif self.multi == 3:
            prefix = 'k'
        elif self.multi == -3:
            prefix = 'm'
        elif self.multi == -6:
            prefix = 'u'
        elif self.multi == -9:
            prefix = 'n'
        elif self.multi == -12:
            prefix = 'p'

        return(str(self.num)+prefix)

    def get_number(self):
        return self.num

    def get_prefix(self):
        return self.multi
    def simplyfiy(self, value:str):
        self.multi = 0

        result = re.search('^(\d+\.?,?\d*)(\D?)', value)

        if result:
            num = result[1]
            num = num.replace(',', '.')

            prefix = result[2]
            num = float(num)

            #nominize
            if num != 0:
                while num < 1:
                    num = num * 1000
                    self.multi = self.multi - 3

                while num >= 1000:
                    num = num / 1000
                    self.multi = self.multi + 3

            self.num = int(num)

            if prefix == '':
                return num
            # giga
            elif 'G' in prefix:
                self.multi = self.multi + 9
            # mega
            elif 'M' in prefix:
                self.multi = self.multi + 6
            # kilo
            elif 'k' in prefix:
                self.multi = self.multi + 3

            # milli
            elif 'm' in prefix:
                self.multi = self.multi - 3
            # micro
            elif 'µ' in prefix or 'Â' in prefix or 'u' in prefix:
                self.multi = self.multi - 6
            # nano
            elif 'n' in prefix:
                self.multi = self.multi - 9
            # piko
            elif 'p' in prefix:
                self.multi = self.multi - 12

        else:
            print("can't simplyfiy "+value)

def unit_norminal(value:str):

    print('Nominal called')

    #num = 0
    #separate number from multiplier
    result = re.search('^(\d+\.?,?\d*)(\D?)', value)

    if result:
        num = result[1]
        if ',' in num:
            num = num.replace(',','.')

        num = float(num)
        mp = result[2]

        multi = 0

        #Empty
        if mp == '':
            return num
        #giga
        elif 'G' in mp:
            num = num * 1000000000
        #mega
        elif 'M' in mp:
            num = num * 1000000
        #kilo
        elif 'k' in mp:
            num = num * 1000

        #milli
        elif 'm' in mp:
            num = num / 1000
        #micro
        elif 'µ' in mp or 'Â' in mp or 'u' in mp:
            multi = -6
        #nano
        elif 'n' in mp:
            num = num / 1000000000
        #piko
        elif 'p' in mp:
            num = num / 1000000000000
        else:
            print('unit_norminal: '+mp+" not found")
            return "not placeable"

        if multi > 0:
            pass
        elif multi < 0:
            multi = multi * -1
            for x in range(multi):
                num = num / 10

        return num
    else:
        print("Error unit_norminal")

    return "not placeable"

typing_list = ['resistor',
               'capacitor']

def typing(name:str):
    if name.startswith('R'):
        return 'resistor'
    elif name.startswith('C'):
        return 'capacitor'
    elif name.startswith('IC'):
        return 'ic'
    else:
        return 'Unknown'

class YY1Part:
    designator = str("R1")
    comment = str("1k")
    footprint = str("0603D")
    mid_x = 30.93
    mid_y = 17.68
    rotation = -90.0
    head = 1
    nozzle = 1
    feeder = 0      #0 = no feeder assigned
    speed = 100
    pick_high = 0
    place_high = 0
    mode = 1
    skip = False

    def __init__(self, name):
        self.name = name

    def get_head(self):
        return self.head

    def get_comment(self):
        return self.comment

    def get_footprint(self):
        return self.footprint

class Part:
    '''
    Class that represents a part
    Following types are available:
    resistor
    capacitor
    diode
    ic
    '''
    name = str('')
    typ = str('')
    value = str('')
    nvalue = 0.0
    package = str('')
    pos_x = 0.0
    pos_y = 0.0
    rotation = 0
    placeable = False

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


class FusionFile:
    parts = []

    def __init__(self, path):
        self.parse(path)

    def part_list(self):
        '''
        gets the part list
        '''
        return self.parts

    def parse(self, path):
        file1 = open(path, 'r')
        Lines = file1.readlines()

        for line in Lines:
            result = re.search(r"(.+);(.+);(.+);(.+);(.+);(.+);", line)

            if (result):
                part = Part()
                part.name = result.group(1).replace(',','.')
                part.typ = typing(part.name)
                part.value = result.group(2).replace(',','.')
                if part.typ in typing_list:
                    part.nvalue = prenum(part.value)
                else:
                    part.nvalue = part.value
                part.package = result.group(3).replace(',','.')
                part.pos_x = result.group(4).strip()
                part.pos_y = result.group(5).strip()
                part.rotation = result.group(6).strip()
                self.parts.append(part)
            else:
                print('Part: '+line+' information missing')


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
