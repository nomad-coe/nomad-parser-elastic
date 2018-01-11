import xml.sax
import logging
import numpy as np
from nomadcore.unit_conversion.unit_conversion import convert_unit_function
from nomadcore.unit_conversion.unit_conversion import convert_unit
from nomadcore.unit_conversion import unit_conversion

class InputHandler(xml.sax.handler.ContentHandler):

    def __init__(self, backend):
        self.backend = backend
        self.inputSectionGIndex = -1
        self.basevect = []
        self.latticeDummy = ''
        self.CurrentData = ''
        self.atomCoor = []
        self.atomCoorDummy = []
        self.speciesfileDummy = ''
        self.speciesfile = []
        self.scale = 1
        self.cell = []
        self.cellDummy = []

    def endDocument(self):
        bohr_to_m = convert_unit(1, "bohr", "m")
        for i in range(0,len(self.cellDummy)):
            for j in range(0,3):
                self.cell[i].append(float(self.cellDummy[i][j])*self.scale*bohr_to_m)
#        print("cell=",self.cell)
        self.backend.addValue("lattice_vectors", self.cell)
        self.backend.addValue('atom_positions',self.atomCoor)
        for i in range(0,len(self.atomCoor)):
            self.speciesfile.append(self.speciesfileDummy)
 #       print("len(self.atomCoor)=",len(self.atomCoor))
 #       print("self.atomCoor=",self.atomCoor)
 #       print("self.speciesfile=",self.speciesfile)
        self.backend.addValue("atom_labels", self.speciesfile)
    def startElement(self, name, attrs):
        self.CurrentData = name
        if name == "crystal":
            self.scale = float(attrs.getValue('scale'))
        elif name == 'species':
            self.speciesfileDummy = attrs.getValue('speciesfile')[:-4]
#            self.backend.addValue("atom_labels", self.speciesfile[:-4])
#            print("self.speciesfile=",self.speciesfile)
        elif name == 'atom':
            self.atomCoorDummy = attrs.getValue('coord').split()
            for j in range(0,3):
               self.atomCoorDummy[j]=float(self.atomCoorDummy[j])
            self.atomCoor.append(self.atomCoorDummy)
#            print("self.atomCoor=",self.atomCoor) 
        else:
            pass

    def endElement(self, name):
        pass

    def characters(self, content):
#        cell = []
        if self.CurrentData == 'basevect':
            self.latticeDummy = content
            lattice = self.latticeDummy.split()
            if lattice != []:
                self.cellDummy.append(lattice)
                self.cell.append([])
#            if lattice[i] != []:
#                cell.append(lattice)
#                for i in range(0,2):                   
#                print("lattice=",cell)
        else:
            pass
#        print("cell=",cell)
#        for i in range(0,len(lattice)):
#            if lattice[i] != []:
#                cell.append(lattice)
#                for i in range(0,2):                   
#                print("lattice=",cell)
#        else:
#            pass

#        for i in range(0,len(lattice)):
#            if lattice[i] != []:
#                cell.append(lattice)
#            print("lattice=",cell)
#                for i in range(0,2):
#    def endElement(self, name):
#        pass

def parseInput(inF, backend):
    handler = InputHandler(backend)
    logging.error("will parse")
    xml.sax.parse(inF, handler)
    logging.error("did parse")
