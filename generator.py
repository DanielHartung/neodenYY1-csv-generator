from Part import *

class nozzle:
    use = False
    component = 0
    head = 1
    drop_station = 0
    pick_station = 0

    def __init__(self):
        pass

class Generator:
    def __init__(self, partlist):
        self.machine = 'YY1'

        self.panelized_length = 0
        self.panelized_width = 0
        self.panelized_rows = 1
        self.panelized_columns = 1

        self.fiducial_x = 5.0
        self.fiducial_y = 5.0
        self.overall_offset_x = 0
        self.overall_offset_y = 0

        self.NozzleChange = []
        self.parts = partlist

        c1 = nozzle()
        c1.use = False
        c1.component = 1
        c1.drop_station = 1
        c1.pick_station = 1
        self.NozzleChange.append(c1)
        self.NozzleChange.append(c1)
        self.NozzleChange.append(c1)
        self.NozzleChange.append(c1)

    def generate(self, path, name):
        f = open(name+".csv", "w")
        f.write("NEODEN,YY1,P&P FILE,,,,,,,,,,,\n")
        f.write(",,,,,,,,,,,,,\n")
        f.write("PanelizedPCB,UnitLength,"+str(self.panelized_length)+",")
        f.write("UnitWidth,"+str(self.panelized_width)+",")
        f.write("Rows,"+str(self.panelized_rows)+",")
        f.write("Columns,"+str(self.panelized_columns)+",\n")
        f.write(",,,,,,,,,,,,,\n")
        f.write("Fiducial,")
        f.write("1-X,"+str(self.fiducial_x)+",")
        f.write("1-Y,"+str(self.fiducial_y)+",")
        f.write("OverallOffsetX,"+str(self.overall_offset_x)+",")
        f.write("OverallOffsetY,"+str(self.overall_offset_y)+",\n")
        f.write(",,,,,,,,,,,,,\n")

        ####################################
        # Nozzle Change                    #
        ####################################
        if len(self.NozzleChange) > 4:
            print("Too much nozzle changes")

        for change in self.NozzleChange:
            f.write("NozzleChange,")
            if change.use:
                f.write("ON,")
            else:
                f.write("OFF,")

            f.write("BeforeComponent,"+str(change.component)+",")
            f.write("Head"+str(change.head)+",")
            f.write("Drop,Station"+str(change.drop_station)+",")
            f.write("PickUp,Station"+str(change.pick_station)+",")
            f.write("\n")

        f.write(",,,,,,,,,,,,,\n")
        ####################################
        # Parts                            #
        ####################################
        f.write("Designator,Comment,Footprint,Mid X(mm),Mid Y(mm) ,Rotation,Head ,FeederNo,Mount Speed(%),Pick Height(mm),Place Height(mm),Mode,Skip\n")
        for part in self.parts:
            f.write(str(part.designator) + ",")
            f.write(str(part.comment) + ",")
            f.write(str(part.footprint) + ",")
            f.write(str(part.mid_x) + ",")
            f.write(str(part.mid_y) + ",")
            f.write(str(part.rotation) + ",")
            f.write(str(part.head) + ",")
            f.write(str(part.feeder) + ",")
            f.write(str(part.speed) + ",")
            f.write(str(part.pick_high) + ",")
            f.write(str(part.place_high) + ",")
            f.write(str(part.mode) + ",")
            if(part.skip):
                f.write("0")
            else:
                f.write("1")

            f.write("\n")


        f.close()