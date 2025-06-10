import re
DEBUG = True

class prenum:
    """
    Represents a number with an SI prefix (e.g., kilo, mega, milli).
    This class parses a string representing a number with an optional SI prefix,
    normalizes the number to a base value with an associated exponent (multiple of 3),
    and provides string representation and access to the numeric value and prefix.
    Attributes:
        num (int): The normalized base number (rounded to integer).
        multi (int): The exponent corresponding to the SI prefix (e.g., 3 for 'k', -3 for 'm').
    Methods:
        __init__(number: str):
            Initializes the prenum object by parsing and normalizing the input string.
        __str__():
            Returns a string representation of the number with its SI prefix.
        get_number():
            Returns the normalized base number.
        get_prefix():
            Returns the exponent corresponding to the SI prefix.
        simplyfiy(value: str):
            Parses and normalizes the input string, extracting the numeric value and SI prefix.
    """
    '''
    number with prefix
    '''
    num = 0
    multi = 0

    def __init__(self, number:str):
        self.simplify(number)

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
        """
        Returns the number associated with this part.

        Returns:
            int: The number of the part.
        """
        return self.num

    def get_prefix(self):
        """
        Returns the prefix associated with the part.

        Returns:
            str: The value of the 'multi' attribute, representing the prefix.
        """
        return self.multi
    
    def simplify(self, value: str):
        """
        Simplifies a string representation of a value with an optional SI unit prefix into a normalized numeric value and its corresponding exponent multiplier.
        The method parses the input string `value`, which may contain a number followed by an optional SI prefix (e.g., 'k', 'M', 'm', 'u', etc.), and normalizes the number to be within the range [1, 1000). It also calculates the exponent multiplier (`self.multi`) based on the SI prefix and normalization steps.
        Args:
            value (str): The string representation of the value to simplify (e.g., '4.7k', '100u', '0.01M').
        Side Effects:
            Sets `self.num` to the normalized integer value.
            Sets `self.multi` to the exponent multiplier corresponding to the SI prefix and normalization.
        Returns:
            float: The normalized numeric value if no SI prefix is present, otherwise None.
        Notes:
            - Recognized SI prefixes: G (giga), M (mega), k (kilo), m (milli), µ/u/Â (micro), n (nano), p (pico).
            - If the input cannot be parsed, prints an error message.
        """
        self.multi = 0

        result = re.search(r'^(\d+\.?,?\d*)(\D?)', value)

        if result:
            num = result[1]
            num = num.replace(',', '.')

            prefix = result[2]
            num = float(num)

            # normalize
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
            # pico
            elif 'p' in prefix:
                self.multi = self.multi - 12

        else:
            print("can't simplify " + value)

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
        if DEBUG:
            print('############ Start parsing Fusion File ##############')
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

        if DEBUG:
            print('############ parsing Fusion File done ##############')


class EagleFile:
    """
    The EagleFile class is responsible for parsing a file containing part information, 
    typically exported from EAGLE PCB design software. It reads the file line by line, 
    extracts part attributes using a regular expression, and stores each part as an 
    EaglePart object in the parts list.
    Attributes:
        parts (list): A list that stores EaglePart objects parsed from the file.
    Methods:
        __init__(path): Initializes the EagleFile object and parses the specified file.
        parse(file): Reads the file, parses each line for part information, and appends 
                     EaglePart objects to the parts list.
    """
    parts = []

    def __init__(self, path):
        self.parse(path)

    def parse(self, file):
        with open(file, 'r') as file1:
            for line in file1:
                # TODO Use a more robust regex to handle possible spaces and missing fields
                result = re.match(r"(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*)", line.strip())
                if result:
                    part = EaglePart()
                    part.partname = result.group(1)
                    part.pos_x = result.group(2)
                    part.pos_y = result.group(3)
                    part.rotation = result.group(4)
                    part.value = result.group(5)
                    part.body = result.group(6)
                    self.parts.append(part)
                else:
                    if DEBUG:
                        print(f"Line could not be parsed: {line.strip()}")
