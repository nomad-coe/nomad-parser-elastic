# Copyright 2017-2018 Lorenzo Pardini
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        self.scale = 1.0
        self.cell = []
        self.cellDummy = []

    def endDocument(self):
        bohr_to_m = convert_unit(1, "bohr", "m")
        for i in range(0,len(self.cellDummy)):
            for j in range(0,3):
                self.cell[i].append(float(self.cellDummy[i][j])*self.scale*bohr_to_m)
        self.backend.addValue("lattice_vectors", self.cell)
        self.backend.addValue('atom_positions',self.atomCoor)
        for i in range(0,len(self.atomCoor)):
            self.speciesfile.append(self.speciesfileDummy)
        self.backend.addValue("atom_labels", self.speciesfile)
    def startElement(self, name, attrs):
        self.CurrentData = name
        if name == "crystal":
            try:
                self.scale = float(attrs.getValue('scale'))
            except:
                self.scale = 1.0
        elif name == 'species':
            self.speciesfileDummy = attrs.getValue('speciesfile')[:-4]
        elif name == 'atom':
            self.atomCoorDummy = attrs.getValue('coord').split()
            for j in range(0,3):
               self.atomCoorDummy[j]=float(self.atomCoorDummy[j])
            self.atomCoor.append(self.atomCoorDummy)
        else:
            pass

    def endElement(self, name):
        pass

    def characters(self, content):
        if self.CurrentData == 'basevect':
            self.latticeDummy = content
            lattice = self.latticeDummy.split()
            if lattice != []:
                self.cellDummy.append(lattice)
                self.cell.append([])
        else:
            pass

def parseInput(inF, backend):
    handler = InputHandler(backend)
    logging.error("will parse")
    xml.sax.parse(inF, handler)
    logging.error("did parse")
