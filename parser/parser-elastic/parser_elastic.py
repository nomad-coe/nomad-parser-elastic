# Copyright 2016-2018 The NOMAD Developers Group
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
#
# Main author and maintainer: Lorenzo Pardini <loren.pard@gmail.com>
from builtins import object
import setup_paths
import numpy as np
from nomadcore.unit_conversion.unit_conversion import convert_unit
from nomadcore.parser_backend import JsonParseEventsWriterBackend
from nomadcore.simple_parser import mainFunction
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
import os, sys, json, elastic_parser_input_exciting, elastic_parser_input_wien2k
#from pathlib import Path

class SampleContext(object):

    def __init__(self): 
#        self.mainFileUri = sys.argv[1]  #exciting !!!!!!LOCAL HOME!!!!!!!!             OKOKOKOK
        self.mainFileUri = sys.argv[2]  #exciting !!! FOR NOMAD URI nmd:// or sbt -> zip file!!!!!!!!   OKOKKOOK
        self.parser = None
        self.mainFilePath = None
        self.mainFile = None
        self.etaEC = []
        self.fitEC = []
        self.SGN = 0
        self.secMethodIndex = None
        self.secSystemIndex = None

    def initialize_values(self):
        """allows to reset values if the same superContext is used to parse different files"""
        pass

    def onOpen_section_system(self, backend, gIndex, section):
        self.secSystemIndex = gIndex

    def startedParsing(self, path, parser):
        """called when parsing starts"""
        self.parser = parser
        self.initialize_values()

    def onOpen_section_method(self, backend, gIndex, section):
        if self.secMethodIndex is None:
            self.secMethodIndex = gIndex

    def onClose_section_run(self, backend, gIndex, section):        
        backend.addValue('program_name', 'elastic')
        backend.addValue('program_version', '1.0')

    def onClose_section_system(self, backend, gIndex, section):
        backend.addArrayValues('configuration_periodic_dimensions', np.asarray([True, True, True]))
        self.SGN = int(section["x_elastic_space_group_number"][0])
        mainFile = self.parser.fIn.fIn.name
#        dirPath = os.path.dirname(mainFile)           #####exciting sbt -> zip file####     YES ?????????? sure???? check first    OKOKOKKO
        self.mainFile = self.parser.fIn.name              #####exciting sbt -> zip file####     YES
        self.mainFilePath = self.mainFile[0:-12]    #####exciting sbt -> zip file####           YES
#        print("self.mainFileUri=",self.mainFileUri)
        dirPath = self.mainFileUri[0:-12]   #####exciting LOCAL HOME or from NOMAD URI nmd://  #######   YES                      OKOKOKOK
#        print("dirPath=",dirPath)
#        for files in os.listdir(self.mainFilePath):
        for files in os.listdir(dirPath):
            if files[-3:] == "xml":
                inputFile = files
                os.chdir(self.mainFilePath)
                with open(inputFile) as f:
                    elastic_parser_input_exciting.parseInput(f, backend)
            elif files[-6:] == "struct":
                inputFile = files
                os.chdir(self.mainFilePath)
#                structSuperContext = elastic_parser_input_wien2k.Wien2kStructContext()
#                structParser = AncillaryParser(
#                    fileDescription = elastic_parser_input_wien2k.buildStructureMatchers(),
#                    parser = self.parser,
#                    cachingLevelForMetaName = elastic_parser_input_wien2k.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.PreOpenedIgnore),
#                    superContext = structSuperContext)
                with open(inputFile) as g:
                    while 1:
                        s = g.readline()
                        if not s: break
                        s = s.strip()
#                        print("s===",s)
#                    structParser.parseFile(fIn)
#                    elastic_parser_input_wien2k.parseInput(f, backend)
#
#        if os.path.exists(fName):
#            structSuperContext = wien2k_parser_struct.Wien2kStructContext()
#            structParser = AncillaryParser(
#                fileDescription = wien2k_parser_struct.buildStructureMatchers(),
#                parser = self.parser,
#                cachingLevelForMetaName = wien2k_parser_struct.get_cachingLevelForMetaName(self.metaInfoEnv, CachingLevel.PreOpenedIgnore),
#                superContext = structSuperContext)
#
#            with open(fName) as fIn:
#                structParser.parseFile(fIn)
#####come era prima di wien                pass
#####come era prima di wien        os.chdir(self.mainFilePath)
#        os.chdir(dirPath)
#####come era prima di wien        with open(inputFile) as f:
#####come era prima di wien            elastic_parser_input.parseInput(f, backend)
#        print(os.listdir(dirPath))
#        if os.path.exist([-3:]) == "xml":
#            inputFile = os.path.exist()
#        inputFile = os.path.join(dirPath, "input.xml")
#        print("inputFile=",inputFile)

    def onClose_section_method(self, backend, gIndex, section):
        ha_per_joule = convert_unit(1, "hartree", "J")
        giga = 10**9
        elCode = section['x_elastic_code']
        elasticGIndex = backend.openSection("section_single_configuration_calculation")
#        self.mainFile = self.parser.fIn.name              #####exciting sbt -> zip file####     NO
#        self.mainFilePath = self.mainFile[0:-12]    #####exciting sbt -> zip file####           NO
        self.mainFilePath = self.mainFileUri[0:-12]   #####exciting LOCAL HOME or from NOMAD URI nmd://  #######      NO
        mdr = float(section['x_elastic_max_lagrangian_strain'][0])
        ordr = int(section['x_elastic_elastic_constant_order'][0])
        nds = int(section['x_elastic_number_of_distorted_structures'][0])
        polFit2 = (nds-1)/2
        polFit4 = polFit2 - 1
        polFit6 = polFit2 - 2
        polFit2Cross = polFit2 - 1
        polFit4Cross = polFit4 - 1
        polFit6Cross = polFit6 - 1
        ext_uri = []
    #    os.chdir(self.mainFilePath)

###################NEW###################
#        for def_str in os.listdir():
#            print("def_str=", def_str)

##################END NEW################
        i = 1
        while 1:
            if (i<10):
                Dstn = 'Dst0'+ str(i)
                if (os.path.exists(Dstn) == True):
                   i += 1
                else:
                   break
            else:
                Dstn = 'Dst' + str(i)
                if (os.path.exists(Dstn) == True):
                   i += 1
                else:
                   break

        defNum = i - 1
        ECs = defNum

###############ADDED BELOW###################
        for j in range(1, ECs+1):
            for i in range(1,nds+1):
                if (j<10):
                    if (i<10):
                        if elCode[0] == 'exciting':
                            ext_uri.append(self.mainFilePath + 'Dst0' + str(j) + '/Dst0' + str(j) + '_0' + str(i) + '/INFO.OUT')
                        elif elCode[0] == 'WIEN':
                            ext_uri.append(self.mainFilePath + 'Dst0' + str(j) + '/Dst0' + str(j) + '_0' + str(i) + '/Dst0'+ str(j) + '_0' + str(i) + '_Converged.scf')
#                            pass
                        elif elCode[0] == 'ESPRESSO':
                            pass
#####################above: to be repeated below for the wien2k and QE################
                    else:
                        if elCode[0] == 'exciting':
                            ext_uri.append(self.mainFilePath + 'Dst0' + str(j) +  '/Dst0' + str(j) + '_' + str(i) + '/INFO.OUT')
                        elif elCode[0] == 'WIEN':
                            ext_uri.append(self.mainFilePath + 'Dst0' + str(j) +  '/Dst0' + str(j) + '_' + str(i) + '/Dst0' + str(j) + '_' + str(i) + '_Converged.scf')
                else:
                    if (i<10):
                        if elCode[0] == 'exciting':
                            ext_uri.append(self.mainFilePath + 'Dst' + str(j) + '/Dst' + str(j)  + '_0' + str(i) + '/INFO.OUT')
                        elif elCode[0] == 'WIEN':
                            ext_uri.append(self.mainFilePath + 'Dst' + str(j) + '/Dst' + str(j)  + '_0' + str(i) + '/Dst' + str(j)  + '_0' + str(i) + '_Converged.scf')
                    else:
                        if elCode[0] == 'exciting':
                            ext_uri.append(self.mainFilePath + 'Dst' + str(j) + '/Dst' + str(j)  + '_' + str(i) + '/INFO.OUT')
                        elif elCode[0] == 'WIEN':
                            ext_uri.append(self.mainFilePath + 'Dst' + str(j) + '/Dst' + str(j)  + '_' + str(i) +'/Dst' + str(j)  + '_' + str(i) + '_Converged.scf')
        for ref in ext_uri:
            refGindex = backend.openSection("section_calculation_to_calculation_refs")
            backend.addValue("calculation_to_calculation_external_url", ref)
            backend.addValue("calculation_to_calculation_kind", "source_calculation")
            backend.closeSection("section_calculation_to_calculation_refs", refGindex)

#        backend.closeSection("section_run")
#        backend.closeSection("section_calculation_to_calculation_refs", refGindex)
#        backend.closeSection("section_single_configuration_calculation", singlGindex)

##############ADDED ABOVE####################

        energy = []
        eta = []

        for j in range(1, ECs+1):
            if (j<10):
                Dstn = 'Dst0'+ str(j)
                eta.append([])
                energy.append([])
            else:
                Dstn = 'Dst' + str(j)
                eta.append([])
                energy.append([])

###############ADDED BELOW###################
#
            cur_dir = os.getcwd() 
#            print("cur_dir=", cur_dir)
#
##############ADDED ABOVE####################

            os.chdir(Dstn)

            cur_dir = os.getcwd() 
#            print("cur_dir=", cur_dir)

#            my_file_exc = '/' + Dstn+'-Energy.dat'
#            my_file_wien = '/' +Dstn+'_Energy.dat'
#            my_file_exciting = Path('my_file_exc')
#            my_file_wien2k = Path('my_file_wien')

#            print("my_file_exc=",my_file_exc)
#            print("my_file_wien=",my_file_wien)
#            print("my_file_exciting=",my_file_exciting)
#            print("my_file_wien2k=",my_file_wien2k)
#            cur_dir = os.getcwd()
#            print("cur_dir=", cur_dir)
#            print(my_file_exciting.exists())
#            print(my_file_wien2k.exists())

#            print("elCode[0]=",elCode[0])
            if elCode[0] == 'exciting':
#                print("ooooooooooexciting")
                f = open(Dstn+'-Energy.dat', 'r')
                while 1:
                   s = f.readline()
                   if not s: break
                   s = s.strip()
                   dummy_eta, dummy_energy = s.split()
#                   print("dummy_eta=",dummy_eta)
#                   print("dummy_energy=",dummy_energy)
                   eta[-1].append(float(dummy_eta))
                   energy[-1].append(float(dummy_energy)*ha_per_joule)
                os.chdir('../')

            elif elCode[0] == 'WIEN': 
#                print("oooooooooooowien2k")
                f = open(Dstn+'_Energy.dat', 'r')
                while 1:
                   s = f.readline()
                   if not s: break
                   s = s.strip()
                   dummy_eta, dummy_energy = s.split()
#                   print("dummy_eta=",dummy_eta)
#                   print("dummy_energy=",dummy_energy)
                   eta[-1].append(float(dummy_eta))
                   energy[-1].append(float(dummy_energy)*ha_per_joule)
                os.chdir('../')

            else:
                os.chdir('../')

#            try:              # WIEN2k
#                f = open(Dstn+'_Energy.dat', 'r')
#                while 1:
#                   s = f.readline()
#                   if not s: break
#                   s = s.strip()
#                   dummy_eta, dummy_energy = s.split()
#                   print("dummy_eta=",dummy_eta)
#                   print("dummy_energy=",dummy_energy)
#                   eta[-1].append(float(dummy_eta))
#                   energy[-1].append(float(dummy_energy)*ha_per_joule)
#                os.chdir('../')
#            except FileNotFoundError:
#                os.chdir('../')

 #           try:              # exciting
 #               f = open(Dstn+'-Energy.dat', 'r')
 #               while 1:
 #                  s = f.readline()
 #                  if not s: break
#                   s = s.strip()
#                   dummy_eta, dummy_energy = s.split()
 #                  print("dummy_eta=",dummy_eta)
 #                  print("dummy_energy=",dummy_energy)
 #                  eta[-1].append(float(dummy_eta))
 #                  energy[-1].append(float(dummy_energy)*ha_per_joule)
 #               os.chdir('../')
 #           except FileNotFoundError:
 #               os.chdir('../')
#            os.chdir('../')
#            print("and now?",os.getcwd()) 
        defTyp = []

        f = open('Distorted_Parameters','r')

        while 1:
            s = f.readline()
            if not s: break
            s = s.strip()
            if 'Lagrangian' in s:
                defTyp.append([])
                s = s.split("(")
                s = s[-1].split(")")
                s = s[0].split(",")
                for i in range(0,6):
                    s[i] = s[i].strip()
                    defTyp[-1].append(s[i])

        f.close()
#        backend.addValue("x_elastic_deformation_types", defTyp)
#        backend.addValue("x_elastic_number_of_deformations", defNum)
#        backend.addValue("x_elastic_energy_strain_eta_values", eta)
#        backend.addValue("x_elastic_energy_strain_energy_values", energy)
#        backend.closeSection("x_elastic_section_single_configuration_calculation", elasticGIndex)

#        my_file = Path("Energy-vs-Strain")
#        print("ooooo",my_file.exists())
#        print("oooooooo ", os.listdir())
        if 'Energy-vs-Strain' in os.listdir():
#        if my_file.is_dir():
#            print("esiste! :-)")
#        else:
#            print("non esiste :-(")
            os.chdir('Energy-vs-Strain')

            d2E6_val = []
            d2E4_val = []
            d2E2_val = []
            d2E6_eta = []
            d2E4_eta = []
            d2E2_eta = []
            d2E_val_tot = []
            d2E_eta_tot = []

            for i in range(1, ECs+1):
                d2E_val_tot.append([])
                d2E_eta_tot.append([])
                if (i<10):
                    if ordr == 2:
                        Dstn = 'Dst0'+ str(i) + '_d2E.dat'
                    elif ordr == 3:
                        Dstn = 'Dst0'+ str(i) + '_d3E.dat'
                    f = open (Dstn,'r')
                    while 1:
                        s = f.readline()
                        if not s: break
                        s = s.strip()
                        if "order" in s.split():
                            d2E_val_tot[-1].append([])
                            d2E_eta_tot[-1].append([])
                        elif len(s) >= 30:
                            d2E_eta, d2E_values = s.split()
                            d2E_val_tot[-1][-1].append(float(d2E_values)*giga)
                            d2E_eta_tot[-1][-1].append(float(d2E_eta))
                    f.close()
                else:
                    if ordr == 2:
                        Dstn = 'Dst' + str(i) + '_d2E.dat'
                    elif ordr == 3:
                        Dstn = 'Dst'+ str(i) + '_d3E.dat'
                    f = open (Dstn,'r')
                    while 1:
                        s = f.readline()
                        if not s: break
                        s = s.strip()
                        if "order" in s.split():
                            d2E_val_tot[-1].append([])
                            d2E_eta_tot[-1].append([])
                        elif len(s) >= 30:
                            d2E_eta, d2E_values = s.split()
                            d2E_val_tot[-1][-1].append(float(d2E_values)*giga)
                            d2E_eta_tot[-1][-1].append(float(d2E_eta))
                    f.close()
                d2E6_val.append(d2E_val_tot[i-1][0])
                d2E4_val.append(d2E_val_tot[i-1][1])
                d2E2_val.append(d2E_val_tot[i-1][2])
                d2E6_eta.append(d2E_eta_tot[i-1][0])
                d2E4_eta.append(d2E_eta_tot[i-1][1])
                d2E2_eta.append(d2E_eta_tot[i-1][2])
            CrossVal6_val = []
            CrossVal4_val = []
            CrossVal2_val = []
            CrossVal_val_tot = []

            CrossVal6_eta = []
            CrossVal4_eta = []
            CrossVal2_eta = []
            CrossVal_eta_tot = []

            for i in range(1, ECs+1):
                CrossVal_val_tot.append([])
                CrossVal_eta_tot.append([])
                if (i<10):
                    DstnCV = 'Dst0'+ str(i) + '_CVe.dat'
                    f = open (DstnCV,'r')
                    while 1:
                        s = f.readline()
                        if not s: break
                        s = s.strip()
                        if "order" in s.split():
                            CrossVal_val_tot[-1].append([])
                            CrossVal_eta_tot[-1].append([])
                        elif len(s) >= 20 and s.split()[0] != '#':
                            CrossVal_eta, CrossVal_values = s.split()
                            CrossVal_val_tot[-1][-1].append(float(CrossVal_values)*ha_per_joule)
                            CrossVal_eta_tot[-1][-1].append(float(CrossVal_eta))
                    f.close()
                else:
                    DstnCV = 'Dst' + str(i) + '_CVe.dat'
                    f = open (Dstn,'r')
                    while 1:
                        s = f.readline()
                        if not s: break
                        s = s.strip()
                        if "order" in s.split():
                            CrossVal_val_tot[-1].append([])
                            CrossVal_eta_tot[-1].append([])
                        elif len(s) >= 20 and s.split()[0] != '#':
                            CrossVal_eta, CrossVal_values = s.split()
                            CrossVal_val_tot[-1][-1].append(float(CrossVal_values)*ha_per_joule)
                            CrossVal_eta_tot[-1][-1].append(float(CrossVal_eta))
                    f.close()
                CrossVal6_val.append(CrossVal_val_tot[i-1][0])
                CrossVal4_val.append(CrossVal_val_tot[i-1][1])
                CrossVal2_val.append(CrossVal_val_tot[i-1][2])
                CrossVal6_eta.append(CrossVal_eta_tot[i-1][0])
                CrossVal4_eta.append(CrossVal_eta_tot[i-1][1])
                CrossVal2_eta.append(CrossVal_eta_tot[i-1][2])

            os.chdir('../')
        else:
            pass

        if ordr == 2:
            f = open ('ElaStic_'+str(ordr)+'nd.in','r')
        elif ordr == 3:
            f = open ('ElaStic_'+str(ordr)+'rd.in','r')

        EC_eigen = []

        for i in range(1, ECs+1):
            s = f.readline()
            s = s.strip()
            dummy, etaEC_dummy, fitEC_dummy = s.split()
            self.etaEC.append(float(etaEC_dummy))
            self.fitEC.append(int(fitEC_dummy))

        f.close()

        if ordr == 2:
            f = open ('ElaStic_'+str(ordr)+'nd.out','r')

            allMat = [[],[],[],[],[],[]]
            voigtMat = [[],[],[],[],[],[]]
            ECMat = [[],[],[],[],[],[]]
            complMat = [[],[],[],[],[],[]]

            while 1:
                s = f.readline()
                if not s: break
                s = s.strip()
                s = s.split()
                if len(s) == 1:
                    try: float(s[0])
                    except ValueError:
                        continue
                    else:
                        EC_eigen.append(float(s[0])*giga)
                elif "B_V" in s:
                    B_V = float(s[5])*giga
                elif "G_V" in s:
                    G_V = float(s[5])*giga
                elif "B_R" in s:
                    B_R = float(s[5])*giga
                elif "G_R" in s:
                    G_R = float(s[5])*giga
                elif "B_H" in s:
                    B_H = float(s[5])*giga
                elif "G_H" in s:
                    G_H = float(s[5])*giga
                elif "E_V" in s:
                    E_V = float(s[5])*giga
                elif "nu_V" in s:
                    nu_V = float(s[5])
                elif "E_R" in s:
                    E_R = float(s[5])*giga
                elif "nu_R" in s:
                    nu_R = float(s[5])
                elif "E_H" in s:
                    E_H = float(s[5])*giga
                elif "nu_H" in s:
                    nu_H = float(s[5])
                elif len(s) == 6 and s[0] != "Elastic" and s[0] != "Eigenvalues":
                    for i in range(0,6):
                        allMat[i].append(s[i])
                elif "AVR" in s:
                    AVR = float(s[6])

            f.close()

            for i in range(0,6):
                voigtMat[i] = allMat[i][0:6]
                ECMat[i] = allMat[i][6:12]
                complMat[i] = allMat[i][12:18]

            for i in range(0,6):
                for j in range(0,6):
                    voigtMat[i][j] = voigtMat[j][i]
                    ECMat[i][j] = float(ECMat[j][i])*giga
                    complMat[i][j] = float(complMat[j][i])/giga

#            backend.addValue("x_elastic_deformation_types", defTyp)
#            backend.addValue("x_elastic_number_of_deformations", defNum)
            elasticSIndex = backend.openSection("x_elastic_section_strain_diagrams")
            backend.addValue("x_elastic_strain_diagram_type", "energy")
            backend.addValue("x_elastic_strain_diagram_number_of_eta", len(eta[0]))
            backend.addValue("x_elastic_strain_diagram_eta_values", eta)
            backend.addValue("x_elastic_strain_diagram_values", energy)
            backend.closeSection("x_elastic_section_strain_diagrams", elasticSIndex)

            elasticSIndex = backend.openSection("x_elastic_section_strain_diagrams")
            backend.addValue("x_elastic_strain_diagram_type", "cross-validation")
            backend.addValue("x_elastic_strain_diagram_polinomial_fit_order", 2)
            backend.addValue("x_elastic_strain_diagram_number_of_eta", polFit2Cross)
            backend.addValue("x_elastic_strain_diagram_eta_values", CrossVal2_eta)
            backend.addValue("x_elastic_strain_diagram_values", CrossVal2_val)
            backend.closeSection("x_elastic_section_strain_diagrams", elasticSIndex)

            elasticSIndex = backend.openSection("x_elastic_section_strain_diagrams")
            backend.addValue("x_elastic_strain_diagram_type", "cross-validation")
            backend.addValue("x_elastic_strain_diagram_polinomial_fit_order", 4)
            backend.addValue("x_elastic_strain_diagram_number_of_eta", polFit4Cross)
            backend.addValue("x_elastic_strain_diagram_eta_values", CrossVal4_eta)
            backend.addValue("x_elastic_strain_diagram_values", CrossVal4_val)
            backend.closeSection("x_elastic_section_strain_diagrams", elasticSIndex)

            elasticSIndex = backend.openSection("x_elastic_section_strain_diagrams")
            backend.addValue("x_elastic_strain_diagram_type", "cross-validation")
            backend.addValue("x_elastic_strain_diagram_polinomial_fit_order", 6)
            backend.addValue("x_elastic_strain_diagram_number_of_eta", polFit6Cross)
            backend.addValue("x_elastic_strain_diagram_eta_values", CrossVal6_eta)
            backend.addValue("x_elastic_strain_diagram_values", CrossVal6_val)
            backend.closeSection("x_elastic_section_strain_diagrams", elasticSIndex)

            elasticSIndex = backend.openSection("x_elastic_section_strain_diagrams")
            backend.addValue("x_elastic_strain_diagram_type", "d2E")
            backend.addValue("x_elastic_strain_diagram_polinomial_fit_order", 2)
            backend.addValue("x_elastic_strain_diagram_number_of_eta", polFit2)
            backend.addValue("x_elastic_strain_diagram_eta_values", d2E2_eta)
            backend.addValue("x_elastic_strain_diagram_values", d2E2_val)
            backend.closeSection("x_elastic_section_strain_diagrams", elasticSIndex)

            elasticSIndex = backend.openSection("x_elastic_section_strain_diagrams")
            backend.addValue("x_elastic_strain_diagram_type", "d2E")
            backend.addValue("x_elastic_strain_diagram_polinomial_fit_order", 4)
            backend.addValue("x_elastic_strain_diagram_number_of_eta", polFit4)
            backend.addValue("x_elastic_strain_diagram_eta_values", d2E4_eta)
            backend.addValue("x_elastic_strain_diagram_values", d2E4_val)
            backend.closeSection("x_elastic_section_strain_diagrams", elasticSIndex)

            elasticSIndex = backend.openSection("x_elastic_section_strain_diagrams")
            backend.addValue("x_elastic_strain_diagram_type", "d2E")
            backend.addValue("x_elastic_strain_diagram_polinomial_fit_order", 6)
            backend.addValue("x_elastic_strain_diagram_number_of_eta", polFit6)
            backend.addValue("x_elastic_strain_diagram_eta_values", d2E6_eta)
            backend.addValue("x_elastic_strain_diagram_values", d2E6_val)
            backend.closeSection("x_elastic_section_strain_diagrams", elasticSIndex)

            backend.addValue('x_elastic_2nd_order_constants_notation_matrix',voigtMat)
            backend.addValue('x_elastic_2nd_order_constants_matrix',ECMat)
            backend.addValue('x_elastic_2nd_order_constants_compliance_matrix',complMat)
            backend.addValue('x_elastic_Voigt_bulk_modulus',B_V)
            backend.addValue('x_elastic_Voigt_shear_modulus',G_V)
            backend.addValue('x_elastic_Reuss_bulk_modulus',B_R)
            backend.addValue('x_elastic_Reuss_shear_modulus',G_R)
            backend.addValue('x_elastic_Hill_bulk_modulus',B_H)
            backend.addValue('x_elastic_Hill_shear_modulus',G_H)
            backend.addValue('x_elastic_Voigt_Young_modulus',E_V)
            backend.addValue('x_elastic_Voigt_Poisson_ratio',nu_V)
            backend.addValue('x_elastic_Reuss_Young_modulus',E_R)
            backend.addValue('x_elastic_Reuss_Poisson_ratio',nu_R)
            backend.addValue('x_elastic_Hill_Young_modulus',E_H)
            backend.addValue('x_elastic_Hill_Poisson_ratio',nu_H)
            backend.addValue('x_elastic_eigenvalues',EC_eigen)
            backend.closeSection("section_single_configuration_calculation", elasticGIndex)
            backend.addValue("x_elastic_deformation_types", defTyp)
            backend.addValue("x_elastic_number_of_deformations", defNum)
            elasticPIndex = backend.openSection("x_elastic_section_fitting_parameters")
            backend.addValue("x_elastic_fitting_parameters_eta", self.etaEC)
            backend.addValue("x_elastic_fitting_parameters_polinomial_order", self.fitEC)
            backend.closeSection("x_elastic_section_fitting_parameters", elasticPIndex)

        elif ordr == 3:
            f = open ('ElaStic_'+str(ordr)+'rd.out','r')

            ECmat = []
            for i in range(0,6):
                ECmat.append([])
                for j in range(0,6):
                    ECmat[i].append([])
                    for k in range(0,6):
                        ECmat[i][j].append([])
                        ECmat[i][j][k] = int(0)

            while 1:
                s = f.readline()
                if not s: break
                s = s.strip()
                s = s.split()
                if len(s) == 4:
                    if s[0] == 'C111':
                        C111 = float(s[2])
                    elif s[0] == 'C112':
                        C112  = float(s[2])
                    elif s[0] == 'C123':
                        C123  = float(s[2])
                    elif s[0] == 'C144':
                        C144  = float(s[2])
                    elif s[0] == 'C155':
                        C155  = float(s[2])
                    elif s[0] == 'C456':
                        C456  = float(s[2])
                    elif s[0] == 'C113':
                        C113  = float(s[2])
                    elif s[0] == 'C166':
                        C166  = float(s[2])
                    elif s[0] == 'C133':
                        C133  = float(s[2])
                    elif s[0] == 'C222':
                        C222  = float(s[2])
                    elif s[0] == 'C333':
                        C333  = float(s[2])
                    elif s[0] == 'C344':
                        C344  = float(s[2])
                    elif s[0] == 'C116':
                        C116  = float(s[2])
                    elif s[0] == 'C145':
                        C145  = float(s[2])
                    elif s[0] == 'C114':
                        C114  = float(s[2])
                    elif s[0] == 'C124':
                        C124  = float(s[2])
                    elif s[0] == 'C134':
                        C134  = float(s[2])
                    elif s[0] == 'C444':
                        C444  = float(s[2])


            if(149 <= self.SGN and self.SGN <= 167): # Rhombohedral I
                LC = 'RI'
                ECs= 14

                A = C111-C222+C112                                     
                B = float(3/4)*C222-float(1/2)*C111-float(1/4)*C112   
                C = float(1/2)*C111-float(1/4)*C222-float(1/4)*C112 
                D = float(1/2)*(C113-C123)      
                E = float(1/2)*(C155-C144)         
                F = float(1/2)*(C114+float(3)*C124)   
                G =-C114-float(2)*C124           
                H = float(1/2)*(C114-C124)

                ECmat[0][0][0] = C111
                ECmat[0][0][1] = C112
                ECmat[0][0][2] = C113
                ECmat[0][0][3] = C114
                ECmat[0][1][0] = C112
                ECmat[0][1][1] = A
                ECmat[0][1][2] = C123
                ECmat[0][1][3] = C124
                ECmat[0][2][0] = C113
                ECmat[0][2][1] = C123
                ECmat[0][2][2] = C133
                ECmat[0][2][3] = C134
                ECmat[0][3][0] = C114
                ECmat[0][3][1] = C124
                ECmat[0][3][2] = C134
                ECmat[0][3][3] = C144
                ECmat[0][4][4] = C155
                ECmat[0][4][5] = F
                ECmat[0][5][4] = F
                ECmat[0][5][5] = B

                ECmat[1][0][0] = C112
                ECmat[1][0][1] = A
                ECmat[1][0][2] = C123
                ECmat[1][0][3] = C124
                ECmat[1][1][0] = A
                ECmat[1][1][1] = C222
                ECmat[1][1][2] = C113
                ECmat[1][1][3] = G
                ECmat[1][2][0] = C123
                ECmat[1][2][1] = C113
                ECmat[1][2][2] = C133
                ECmat[1][2][3] = -C134
                ECmat[1][3][0] = C124
                ECmat[1][3][1] = G
                ECmat[1][3][2] = -C134
                ECmat[1][3][3] = C155
                ECmat[1][4][4] = C144
                ECmat[1][4][5] = H
                ECmat[1][5][4] = H
                ECmat[1][5][5] = C

                ECmat[2][0][0] = C113
                ECmat[2][0][1] = C123
                ECmat[2][0][2] = C133
                ECmat[2][0][3] = C134
                ECmat[2][1][0] = C123
                ECmat[2][1][1] = C113
                ECmat[2][1][2] = C133
                ECmat[2][1][3] = -C134
                ECmat[2][2][0] = C133
                ECmat[2][2][1] = C133
                ECmat[2][2][2] = C133
                ECmat[2][3][0] = C134
                ECmat[2][3][1] = -C134
                ECmat[2][3][3] = C344
                ECmat[2][4][4] = C344
                ECmat[2][4][5] = C134
                ECmat[2][5][4] = C134
                ECmat[2][5][5] = D

                ECmat[3][0][0] = C114
                ECmat[3][0][1] = C124
                ECmat[3][0][2] = C134
                ECmat[3][0][3] = C144
                ECmat[3][1][0] = C12
                ECmat[3][1][1] = G
                ECmat[3][1][2] = -C134
                ECmat[3][1][3] = C155
                ECmat[3][2][0] = C134
                ECmat[3][2][1] = -C134
                ECmat[3][2][3] = C344
                ECmat[3][3][0] = C144
                ECmat[3][3][1] = C155
                ECmat[3][3][2] = C344
                ECmat[3][3][3] = C444
                ECmat[3][4][4] = -C444
                ECmat[3][4][5] = E
                ECmat[3][5][4] = E
                ECmat[3][5][5] = C124

                ECmat[4][0][4] = C155
                ECmat[4][0][5] = F
                ECmat[4][1][4] = C144
                ECmat[4][1][5] = H
                ECmat[4][2][4] = C344
                ECmat[4][2][5] = C134
                ECmat[4][3][5] = E
                ECmat[4][4][0] = C155
                ECmat[4][4][1] = C144
                ECmat[4][4][2] = C344
                ECmat[4][5][0] = F
                ECmat[4][5][1] = H
                ECmat[4][5][2] = C134
                ECmat[4][5][3] = E

                ECmat[5][0][4] = F
                ECmat[5][0][5] = B
                ECmat[5][1][4] = H
                ECmat[5][1][5] = C
                ECmat[5][2][4] = C134
                ECmat[5][2][5] = D
                ECmat[5][3][4] = E
                ECmat[5][3][5] = C124
                ECmat[5][4][0] = F
                ECmat[5][4][1] = H
                ECmat[5][4][2] = C134
                ECmat[5][4][3] = E
                ECmat[5][5][0] = B
                ECmat[5][5][1] = C
                ECmat[5][5][2] = D
                ECmat[5][5][3] = C124


            elif(168 <= self.SGN and self.SGN <= 176): # Hexagonal II
                LC = 'HII'
                ECs= 12

                A = C111-C222+C112                
                B = float(3/4)*C222-float(1/2)*C111-float(1/4)*C112   
                C = float(1/2)*C111-float(1/4)*C222-float(1/4)*C112     
                D = float(1/2)*(C113-C123)          
                E = float(1/2)*(C155-C144)

                ECmat[0][0][0] = C111
                ECmat[0][0][1] = C112
                ECmat[0][0][2] = C113
                ECmat[0][0][5] = C116
                ECmat[0][1][0] = C112
                ECmat[0][1][1] = A
                ECmat[0][1][2] = C123
                ECmat[0][1][5] = -C116
                ECmat[0][2][0] = C113
                ECmat[0][2][1] = C123
                ECmat[0][2][2] = C133
                ECmat[0][3][3] = C144
                ECmat[0][3][4] = C145
                ECmat[0][4][3] = C145
                ECmat[0][4][4] = C155
                ECmat[0][5][0] = C116
                ECmat[0][5][1] = -C116
                ECmat[0][5][5] = B

                ECmat[1][0][0] = C112
                ECmat[1][0][1] = A
                ECmat[1][0][2] = C123
                ECmat[1][1][0] = A
                ECmat[1][1][1] = A222
                ECmat[1][1][2] = C113
                ECmat[1][1][5] = C116
                ECmat[1][2][0] = C123
                ECmat[1][2][1] = C113
                ECmat[1][2][2] = C133
                ECmat[1][3][3] = C155
                ECmat[1][3][4] = -C145
                ECmat[1][4][3] = -C145
                ECmat[1][4][4] = C144
                ECmat[1][5][1] = C116
                ECmat[1][5][5] = C

                ECmat[2][0][0] = C113
                ECmat[2][0][1] = C123
                ECmat[2][0][2] = C133
                ECmat[2][1][0] = C123
                ECmat[2][1][1] = C113
                ECmat[2][1][2] = C133
                ECmat[2][2][0] = C133
                ECmat[2][2][1] = C133
                ECmat[2][2][2] = C133
                ECmat[2][3][3] = C344
                ECmat[2][4][4] = C344
                ECmat[2][5][5] = D

                ECmat[3][0][3] = C144
                ECmat[3][1][3] = C155
                ECmat[3][2][3] = C344
                ECmat[3][3][0] = C144
                ECmat[3][3][1] = C155
                ECmat[3][3][2] = C344
                ECmat[3][3][5] = C145
                ECmat[3][4][5] = E
                ECmat[3][5][3] = C145
                ECmat[3][5][4] = E

                ECmat[4][0][3] = C155
                ECmat[4][1][3] = C144
                ECmat[4][2][3] = C344
                ECmat[4][3][5] = E
                ECmat[4][4][0] = C155
                ECmat[4][4][1] = C144
                ECmat[4][4][2] = C344
                ECmat[4][4][5] = -C145
                ECmat[4][5][3] = E
                ECmat[4][5][4] = -C145

                ECmat[5][0][5] = B
                ECmat[5][1][5] = C
                ECmat[5][2][5] = D
                ECmat[5][3][4] = E
                ECmat[5][4][3] = E
                ECmat[5][5][0] = B
                ECmat[5][5][1] = C
                ECmat[5][5][2] = D
                ECmat[5][5][5] = -C116

            elif(177 <= self.SGN and self.SGN <= 194): # Hexagonal I
                LC = 'HI'
                ECs= 10

                A = C111-C222+C112         
                B = float(3/4)*C222-float(1/2)*C111-float(1/4)*C112   
                C = float(1/2)*C111-float(1/4)*C222-float(1/4)*C112   
                D = float(1/2)*(C113-C123)   
                E = float(1/2)*(C155-C144)

                ECmat[0][0][0] = C111
                ECmat[0][0][1] = C112
                ECmat[0][0][2] = C113
                ECmat[0][1][0] = C112
                ECmat[0][1][1] = A
                ECmat[0][1][2] = C123
                ECmat[0][2][0] = C113
                ECmat[0][2][1] = C123
                ECmat[0][2][2] = C133
                ECmat[0][3][3] = C144
                ECmat[0][4][4] = C155
                ECmat[0][5][5] = B

                ECmat[1][0][0] = C112
                ECmat[1][0][1] = A
                ECmat[1][0][2] = C123
                ECmat[1][1][0] = A
                ECmat[1][1][1] = C222
                ECmat[1][1][2] = C113
                ECmat[1][2][0] = C123
                ECmat[1][2][1] = C113
                ECmat[1][2][2] = C133
                ECmat[1][3][3] = C155
                ECmat[1][4][4] = C144
                ECmat[1][5][5] = C

                ECmat[2][0][0] = C113
                ECmat[2][0][1] = C123
                ECmat[2][0][2] = C133
                ECmat[2][1][0] = C123
                ECmat[2][1][1] = C113
                ECmat[2][1][2] = C133
                ECmat[2][2][0] = C133
                ECmat[2][2][1] = C133
                ECmat[2][2][2] = C133
                ECmat[2][3][3] = C344
                ECmat[2][4][4] = C344
                ECmat[2][5][5] = D

                ECmat[3][0][3] = C144
                ECmat[3][1][3] = C155
                ECmat[3][2][3] = C344
                ECmat[3][3][0] = C144
                ECmat[3][3][1] = C155
                ECmat[3][3][2] = C344
                ECmat[3][4][5] = E
                ECmat[3][5][4] = E

                ECmat[4][0][4] = C155
                ECmat[4][1][4] = C144
                ECmat[4][2][4] = C344
                ECmat[4][3][5] = E
                ECmat[4][4][0] = C155
                ECmat[4][4][1] = C144
                ECmat[4][4][2] = C344
                ECmat[4][5][3] = E

                ECmat[5][0][5] = B
                ECmat[5][1][5] = C
                ECmat[5][2][5] = D
                ECmat[5][3][4] = E
                ECmat[5][4][3] = E
                ECmat[5][5][0] = B
                ECmat[5][5][1] = C
                ECmat[5][5][2] = D

            elif(195 <= self.SGN and self.SGN <= 206): # Cubic II
                LC = 'CII'
                ECs=  8

                ECmat[0][0][0] = C111
                ECmat[0][0][1] = C112
                ECmat[0][0][2] = C113
                ECmat[0][1][0] = C112
                ECmat[0][1][1] = C113
                ECmat[0][1][2] = C123
                ECmat[0][2][0] = C113
                ECmat[0][2][1] = C123
                ECmat[0][2][2] = C112
                ECmat[0][3][3] = C144
                ECmat[0][4][4] = C155
                ECmat[0][5][5] = C166

                ECmat[1][0][0] = C112
                ECmat[1][0][1] = C112
                ECmat[1][0][2] = C113
                ECmat[1][1][0] = C112
                ECmat[1][1][1] = C111
                ECmat[1][1][2] = C112
                ECmat[1][2][0] = C123
                ECmat[1][2][1] = C112
                ECmat[1][2][2] = C113
                ECmat[1][3][3] = C166
                ECmat[1][4][4] = C144
                ECmat[1][5][5] = C155

                ECmat[2][0][0] = C112
                ECmat[2][0][1] = C123
                ECmat[2][0][2] = C112
                ECmat[2][1][0] = C123
                ECmat[2][1][1] = C112
                ECmat[2][1][2] = C112
                ECmat[2][2][0] = C112
                ECmat[2][2][1] = C112
                ECmat[2][2][2] = C111
                ECmat[2][3][3] = C155
                ECmat[2][4][4] = C166
                ECmat[2][5][5] = C144

                ECmat[3][0][3] = C144
                ECmat[3][1][3] = C155
                ECmat[3][2][3] = C155
                ECmat[3][3][0] = C144
                ECmat[3][3][1] = C155
                ECmat[3][3][2] = C155
                ECmat[3][4][5] = C456
                ECmat[3][5][4] = C456

                ECmat[4][0][3] = C155
                ECmat[4][1][3] = C144
                ECmat[4][2][3] = C155
                ECmat[4][3][5] = C456
                ECmat[4][4][0] = C155
                ECmat[4][4][1] = C144
                ECmat[4][4][2] = C155
                ECmat[4][5][3] = C456

                ECmat[5][0][5] = C155
                ECmat[5][1][5] = C155
                ECmat[5][2][5] = C144
                ECmat[5][3][4] = C456
                ECmat[5][4][3] = C456
                ECmat[5][5][0] = C155
                ECmat[5][5][1] = C155
                ECmat[5][5][2] = C144

            elif(207 <= self.SGN and self.SGN <= 230): # Cubic I
                LC = 'CI'
                ECs=  6

                ECmat[0][0][0] = C111
                ECmat[0][0][1] = C112 
                ECmat[0][0][2] = C112 
                ECmat[0][1][0] = C112
                ECmat[0][1][1] = C112
                ECmat[0][1][2] = C113
                ECmat[0][2][0] = C112     
                ECmat[0][2][1] = C123     
                ECmat[0][2][2] = C112    
                ECmat[0][3][3] = C144    
                ECmat[0][4][4] = C155    
                ECmat[0][5][5] = C155

                ECmat[1][0][0] = C112
                ECmat[1][0][1] = C112
                ECmat[1][0][2] = C123
                ECmat[1][1][0] = C112            
                ECmat[1][1][1] = C111
                ECmat[1][1][2] = C112
                ECmat[1][2][0] = C123
                ECmat[1][2][1] = C112
                ECmat[1][2][2] = C112
                ECmat[1][3][3] = C155
                ECmat[1][4][4] = C144
                ECmat[1][5][5] = C155

                ECmat[2][0][0] = C112
                ECmat[2][0][1] = C123
                ECmat[2][0][2] = C112
                ECmat[2][1][0] = C123
                ECmat[2][1][1] = C112
                ECmat[2][1][2] = C112
                ECmat[2][2][0] = C112
                ECmat[2][2][1] = C112
                ECmat[2][2][2] = C111
                ECmat[2][3][3] = C155
                ECmat[2][4][4] = C155
                ECmat[2][5][5] = C144

                ECmat[3][0][3] = C144
                ECmat[3][1][3] = C155
                ECmat[3][2][3] = C155
                ECmat[3][3][0] = C144
                ECmat[3][3][1] = C155
                ECmat[3][3][2] = C155
                ECmat[3][4][5] = C456
                ECmat[3][5][4] = C456

                ECmat[4][0][3] = C155
                ECmat[4][1][3] = C144
                ECmat[4][2][3] = C155
                ECmat[4][3][5] = C456
                ECmat[4][4][0] = C155
                ECmat[4][4][1] = C144
                ECmat[4][4][2] = C155
                ECmat[4][5][3] = C456
    
                ECmat[5][0][5] = C155
                ECmat[5][1][5] = C155
                ECmat[5][2][5] = C144
                ECmat[5][3][4] = C456
                ECmat[5][4][3] = C456
                ECmat[5][5][0] = C155
                ECmat[5][5][1] = C155
                ECmat[5][5][2] = C144

            elasticSIndex = backend.openSection("x_elastic_section_strain_diagrams")
            backend.addValue("x_elastic_strain_diagram_type", "energy")
            backend.addValue("x_elastic_strain_diagram_number_of_eta", len(eta))
            backend.addValue("x_elastic_strain_diagram_eta_values", eta)
            backend.addValue("x_elastic_strain_diagram_values", energy)
            backend.closeSection("x_elastic_section_strain_diagrams", elasticSIndex)
            backend.addValue('x_elastic_3rd_order_constants_matrix',ECmat)
            backend.closeSection("section_single_configuration_calculation", elasticGIndex)
            backend.addValue("x_elastic_deformation_types", defTyp)
            backend.addValue("x_elastic_number_of_deformations", defNum)
            elasticPIndex = backend.openSection("x_elastic_section_fitting_parameters")
            backend.addValue("x_elastic_fitting_parameters_eta", self.etaEC)
            backend.addValue("x_elastic_fitting_parameters_polinomial_order", self.fitEC)
            backend.closeSection("x_elastic_section_fitting_parameters", elasticPIndex)

    def onClose_section_single_configuration_calculation(self, backend, gIndex, section):
#    logging.error("BASE onClose_section_single_configuration_calculation")
        backend.addValue('single_configuration_to_calculation_method_ref', self.secMethodIndex)
        backend.addValue('single_configuration_calculation_to_system_ref', self.secSystemIndex)

mainFileDescription = \
           SM(name = 'root',
              weak = False,
              startReStr = "",
              subMatchers = [
              SM(name = 'input',
#                weak = True,
                startReStr = r"\s*Order of elastic constants\s*=\s*(?P<x_elastic_elastic_constant_order>[0-9]+)",
#                startReStr = "",
#                endReStr = r"\*sNumber of distorted structures\*s=\s*(?P<x_elastic_number_of_disordered_structures>[0-9]+)",
                repeats = False,
                required = False,
                forwardMatch = False,
                sections   = ['section_run', 'section_method'],
                subMatchers = [
#                  SM(r"\s*Order of elastic constants\s*=\s*(?P<x_elastic_elastic_constant_order>[0-9]+)"),
                  SM(r"\s*Method of calculation\s*=\s*(?P<x_elastic_calculation_method>[-a-zA-Z]+)"),
                  SM(r"\s*DFT code name\s*=\s*(?P<x_elastic_code>[-a-zA-Z]+)"),
                  SM(name = 'system',
                  startReStr = r"\s*Space-group number\s*=\s*(?P<x_elastic_space_group_number>[0-9]+)",
                  sections = ['section_system'],
                  subMatchers = [
#                  SM(r"\s*Space-group number\s*=\s*(?P<x_elastic_space_group_number>[0-9]+)"),
                  SM(r"\s*Volume of equilibrium unit cell\s*=\s*(?P<x_elastic_unit_cell_volume__bohr3>[-0-9.]+)\s*\[a.u\^3\]")
                  ]),
                  SM(r"\s*Maximum Lagrangian strain\s*=\s*(?P<x_elastic_max_lagrangian_strain>[0-9.]+)"),
                  SM(r"\s*Number of distorted structures\s*=\s*(?P<x_elastic_number_of_distorted_structures>[0-9]+)")
               ] )
              ])


parserInfo = {
  "name": "elastic_parser",
  "version": "1.0"
}

metaInfoPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../../nomad-meta-info/meta_info/nomad_meta_info/elastic.nomadmetainfo.json"))
metaInfoEnv, warnings = loadJsonFile(filePath = metaInfoPath, dependencyLoader = None, extraArgsHandling = InfoKindEl.ADD_EXTRA_ARGS, uri = None)

if __name__ == "__main__":
    superContext = SampleContext()
    mainFunction(mainFileDescription, metaInfoEnv, parserInfo, superContext = superContext)
#    mainFileUri = sys.argv[1]
