#from Part import parts
from yy1 import nozzle, Machine

class Generator:
    def __init__(self, partlist, nozzle_changes):
        self.machine = 'YY1'

        self.panelized_length = 0
        self.panelized_width = 0
        self.panelized_rows = 1
        self.panelized_columns = 1

        self.fiducial_x = 5.0
        self.fiducial_y = 5.0
        self.overall_offset_x = 0
        self.overall_offset_y = 0

        self.parts = partlist

        self.NozzleChange = nozzle_changes

        while len(self.NozzleChange) < 4:
            c1 = nozzle()
            c1.use = False
            c1.component = 1
            c1.drop_station = 1
            c1.pick_station = 1
            self.NozzleChange.append(c1)

    def generate(self, filepath):
        """
        Generates a CSV file for the Neoden YY1 pick-and-place machine configuration.
        The generated file includes header information, panelized PCB settings, fiducial data,
        nozzle change instructions, and a list of parts with their placement parameters.
        Args:
            filepath (str): The path to the output CSV file.
        The function writes the following sections to the file:
            - General header and empty lines for formatting.
            - Panelized PCB configuration (length, width, rows, columns).
            - Fiducial and overall offset information.
            - Nozzle change instructions (up to 4 changes; prints a warning if exceeded).
            - Parts list with placement details for each part.
        Raises:
            Prints a warning if more than 4 nozzle changes are specified.
        """
        with open(filepath, "w") as f:
            f.write("NEODEN,YY1,P&P FILE,,,,,,,,,,,\n")
            f.write(",,,,,,,,,,,,,\n")
            f.write(f"PanelizedPCB,UnitLength,{self.panelized_length},UnitWidth,{self.panelized_width},Rows,{self.panelized_rows},Columns,{self.panelized_columns},\n")
            f.write(",,,,,,,,,,,,,\n")
            f.write(f"Fiducial,1-X,{self.fiducial_x},1-Y,{self.fiducial_y},OverallOffsetX,{self.overall_offset_x},OverallOffsetY,{self.overall_offset_y},\n")
            f.write(",,,,,,,,,,,,,\n")

        ####################################
        # Nozzle Change                    #
        ####################################
            if len(self.NozzleChange) > 4:
                print("Too many nozzle changes")

            for change in self.NozzleChange:
                status = "ON" if change.use else "OFF"
                line = [
                "NozzleChange",
                status,
                f"BeforeComponent,{change.component}",
                f"Head{change.head}",
                f"Drop,Station{change.drop_station}",
                f"PickUp,Station{change.pick_station}",
                ""
                ]
                f.write(",".join(line) + "\n")

            f.write(",,,,,,,,,,,,,\n")
        ####################################
        # Parts                            #
        ####################################
            f.write("Designator,Comment,Footprint,Mid X(mm),Mid Y(mm) ,Rotation,Head ,FeederNo,Mount Speed(%),Pick Height(mm),Place Height(mm),Mode,Skip\n")
            for part in self.parts:
                fields = [
                part.designator,
                part.comment,
                part.footprint,
                part.mid_x,
                part.mid_y,
                part.rotation,
                part.head,
                part.feeder,
                part.speed,
                part.pick_high,
                part.place_high,
                part.mode,
                "0" if part.skip else "1"
                ]
                f.write(",".join(str(field) for field in fields) + "\n")

            f.close()