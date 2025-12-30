from generator import Generator
from Part import FusionFile
from yy1 import Machine
import sys
import argparse
import os

DEBUG = True

def config_parser():
    """
    Creates and returns an ArgumentParser for the Neodenyy1-CSV_Generator tool.
    The parser defines the following command-line arguments:
        - '-f' or '--file': Path to the source CSV/MNT file (required).
        - '-m' or '--machine': Path to the machine file (required).
        - '-g' or '--gui': Flag to start the GUI for the tool (optional).
    Returns:
        argparse.ArgumentParser: Configured argument parser for command-line options.
    """
    parser = argparse.ArgumentParser(prog='Neodenyy1-CSV_Generator')
    parser.add_argument('-f', '--file', type=str, required=True, help='Source CSV File')
    parser.add_argument('-m', '--machine', type=str, required=True, help='Machine file')
    parser.add_argument('-g', '--gui', action='store_true', help='starts the Gui for the tool')

    return parser

def generate_output_file(generator: Generator, filename: str):
    """
    Generates an output CSV file using the provided generator.

    Args:
        generator (Generator): An instance of a Generator class responsible for creating the output file.
        filename (str): The input filename.

    Side Effects:
        Writes a CSV file to the 'output/' directory, with the same base name as the input filename but with a '.csv' extension.
    """
    if not os.path.exists("output"):
        os.makedirs("output")
    
    base_name = os.path.basename(filename)
    if base_name.lower().endswith('.mnt'):
        output_filename = base_name[:-4] + '.csv'
    else:
        output_filename = os.path.splitext(base_name)[0] + '.csv'
        
    output_path = os.path.join("output", output_filename)
    generator.generate(output_path)
    print(f"Generated output file: {output_path}")

if __name__ == '__main__':
    parser = config_parser()
    args = parser.parse_args()

    if args.file is None:
        print("No file specified. Use -f or --file to specify the source file.")
        sys.exit(1)
    else:
        print(f"File: {args.file}")

    # Check if files exist
    if not os.path.exists(args.file):
        print(f"Error: Input file '{args.file}' not found.")
        sys.exit(1)

    if not os.path.exists(args.machine):
        print(f"Error: Machine file '{args.machine}' not found.")
        sys.exit(1)

    try:
        ##################################
        # prepare the machine and parts  #
        ##################################

        #generate machine class with all Feeders
        machine = Machine(args.machine)
        #generate Parts class with all Parts
        fusionfile = FusionFile(args.file)
        
        # Check if any parts were found
        if not fusionfile.part_list():
            print(f"Warning: No parts found in source file '{args.file}'. Please check the file format.")
            # We continue, but it might result in an empty CSV
            
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
        generate_output_file(g, args.file)
        
    except PermissionError:
        print(f"Error: Permission denied. Please close the input/output files and try again.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if DEBUG:
            raise e
        sys.exit(1)

    


