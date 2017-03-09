from builtins import object
import setup_paths
import numpy as np
from nomadcore.simple_parser import mainFunction
from nomadcore.simple_parser import SimpleMatcher as SM
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
import os, sys, json

class SampleContext(object):
    """context for the sample parser"""

    def __init__(self):
        self.parser = None

    def initialize_values(self):
        """allows to reset values if the same superContext is used to parse different files"""
        pass

    def startedParsing(self, path, parser):
        """called when parsing starts"""
        self.parser = parser
        # allows to reset values if the same superContext is used to parse different files
        self.initialize_values()

    def onClose_section_method(self, backend, gIndex, section):
        elasticGIndex = backend.openSection("x_elastic_section_single_configuration_calculation")
        mainFile = self.parser.fIn.name
        mainFilePath = mainFile[0:-12]
        mdr = float(section['x_elastic_max_lagrangian_strain'][0])
        ordr = int(section['x_elastic_elastic_constant_order'][0])
        nds = int(section['x_elastic_number_of_distorted_structures'][0])
        polFit2 = (nds-1)/2
        polFit4 = polFit2 - 1
        polFit6 = polFit2 - 2
        polFit2Cross = polFit2 - 1
        polFit4Cross = polFit4 - 1
        polFit6Cross = polFit6 - 1
#        print('ordr=',nds)
        os.chdir(mainFilePath)
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

        energy = []
        eta = []

        for j in range(1, ECs+1):
            if (j<10):
                Dstn = 'Dst0'+ str(j)
                eta.append([])
                energy.append([])
            else:
                Dstn = 'Dst' + str(i)
                eta.append([])
                energy.append([])
            os.chdir(Dstn)

            f = open(Dstn+'-Energy.dat', 'r')
            while 1:
               s = f.readline()
               if not s: break
               s = s.strip()
               dummy_eta, dummy_energy = s.split()
               eta[-1].append(float(dummy_eta))
               energy[-1].append(float(dummy_energy))
            os.chdir('../')
        
        defTyp = []

        f = open('Distorted_Parameters','r')

        while 1:
            s = f.readline()
            if not s: break
            s = s.strip()
#            print("s=",s)
            if 'Lagrangian' in s:
                defTyp.append([])
                s = s.split("(")
                s = s[-1].split(")")
                s = s[0].split(",")
#                print("esse=",s)
                for i in range(0,6):
                    s[i] = s[i].strip()
#                    print("s[i]=",s[i])
                    if s[i] == '0.0':
                        defTyp[-1].append(float(s[i]))
                    elif s[i] == 'eta':
                        defTyp[-1].append(mdr)
                    elif s[i] == '2eta':
                        defTyp[-1].append(2.0*mdr)
                    elif s[i] == '-eta':
                        defTyp[-1].append(-mdr)
                    elif s[i] == '.5eta':
                        defTyp[-1].append(0.5*mdr)
                    elif s[i] == '-2eta':
                        defTyp[-1].append(-2.0*mdr)
                    elif s[i] == '3eta':
                        defTyp[-1].append(3.0*mdr)
                    elif s[i] == '4eta':
                        defTyp[-1].append(4.0*mdr)
                    elif s[i] == '5eta':
                        defTyp[-1].append(5.0*mdr)
                    elif s[i] == '6eta':
                        defTyp[-1].append(6.0*mdr)
                    elif s[i] == '-3eta':
                        defTyp[-1].append(-3.0*mdr)
                    elif s[i] == '-5eta':
                        defTyp[-1].append(-5.0*mdr)
                    elif s[i] == '-6eta':
                        defTyp[-1].append(-6.0*mdr)
                    elif s[i] == '-4eta':
                        defTyp[-1].append(-4.0*mdr)

        f.close()
#        print("defTyp=",defTyp)
#        print('eta=',eta)
#        print('energy=',energy)
#        backend.addValue("x_elastic_deformation_types", defTyp)
#        backend.addValue("x_elastic_number_of_deformations", defNum)
#        backend.addValue("x_elastic_energy_strain_eta_values", eta)
#        backend.addValue("x_elastic_energy_strain_energy_values", energy)
#        backend.closeSection("x_elastic_section_single_configuration_calculation", elasticGIndex)
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
                Dstn = 'Dst0'+ str(i) + '_d2E.dat'
                f = open (Dstn,'r')
                while 1:
                    s = f.readline()
                    if not s: break
                    s = s.strip()
#                    print("esse=",s)
                    if "order" in s.split():
                        d2E_val_tot[-1].append([])
                        d2E_eta_tot[-1].append([])
                    elif len(s) >= 30:
                        d2E_eta, d2E_values = s.split()
                        d2E_val_tot[-1][-1].append(float(d2E_values))
                        d2E_eta_tot[-1][-1].append(float(d2E_eta))
                f.close()
            else:
                Dstn = 'Dst' + str(i) + '_d2E.dat'
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
                        d2E_val_tot[-1][-1].append(float(d2E_values))
                        d2E_eta_tot[-1][-1].append(float(d2E_eta))
                f.close()
            d2E6_val.append(d2E_val_tot[i-1][0])
            d2E4_val.append(d2E_val_tot[i-1][1])
            d2E2_val.append(d2E_val_tot[i-1][2])
            d2E6_eta.append(d2E_eta_tot[i-1][0])
            d2E4_eta.append(d2E_eta_tot[i-1][1])
            d2E2_eta.append(d2E_eta_tot[i-1][2])
#        print("d2E6_val=",d2E6_val)
#        print("d2E2_val=",d2E2_val)
#        print("d2E6_eta=",d2E6_eta)
#        print("d2E2_eta=",d2E2_eta)
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
                        CrossVal_val_tot[-1][-1].append(float(CrossVal_values))
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
                        CrossVal_val_tot[-1][-1].append(float(CrossVal_values))
                        CrossVal_val_tot[-1][-1].append(float(CrossVal_values))
                f.close()
            CrossVal6_val.append(CrossVal_val_tot[i-1][0])
            CrossVal4_val.append(CrossVal_val_tot[i-1][1])
            CrossVal2_val.append(CrossVal_val_tot[i-1][2])
            CrossVal6_eta.append(CrossVal_eta_tot[i-1][0])
            CrossVal4_eta.append(CrossVal_eta_tot[i-1][1])
            CrossVal2_eta.append(CrossVal_eta_tot[i-1][2])

        os.chdir('../')

        f = open ('ElaStic_'+str(ordr)+'nd.in','r')

        etaEC = []
        fitEC = []
        EC_eigen = []

        for i in range(1, ECs+1):
            s = f.readline()
            s = s.strip()
            dummy, etaEC_dummy, fitEC_dummy = s.split()
            etaEC.append(etaEC_dummy)
            fitEC.append(fitEC_dummy)

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
#                print("esse=",s)
                try: float(s[0])
                except ValueError:
                    continue
                else:
                    EC_eigen.append(float(s[0]))
            elif "B_V" in s:
                B_V = float(s[5])
            elif "G_V" in s:
                G_V = float(s[5])
            elif "B_R" in s:
                B_R = float(s[5])
            elif "G_R" in s:
                G_R = float(s[5])
            elif "B_H" in s:
                B_H = float(s[5])
            elif "G_H" in s:
                G_H = float(s[5])
            elif "E_V" in s:
                E_V = float(s[5])
            elif "nu_V" in s:
                nu_V = float(s[5])
            elif "E_R" in s:
                E_R = float(s[5])
            elif "nu_R" in s:
                nu_R = float(s[5])
            elif "E_H" in s:
                E_H = float(s[5])
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
                ECMat[i][j] = float(ECMat[i][j])
                complMat[i][j] = float(complMat[i][j])

        backend.addValue("x_elastic_deformation_types", defTyp)
        backend.addValue("x_elastic_number_of_deformations", defNum)
        backend.addValue("x_elastic_energy_strain_eta_values", eta)
        backend.addValue("x_elastic_energy_strain_energy_values", energy)
        backend.addValue('x_elastic_d2E_number_of_eta_polinomial_2nd',polFit2)
        backend.addValue('x_elastic_d2E_number_of_eta_polinomial_4th',polFit4)
        backend.addValue('x_elastic_d2E_number_of_eta_polinomial_6th',polFit6)
        backend.addValue('x_elastic_d2E_d2E_values_2nd',d2E2_val)
        backend.addValue('x_elastic_d2E_d2E_values_4th',d2E4_val)
        backend.addValue('x_elastic_d2E_d2E_values_6th',d2E6_val)
        backend.addValue('x_elastic_d2E_eta_values_2nd',d2E2_eta)
        backend.addValue('x_elastic_d2E_eta_values_4th',d2E4_eta)
        backend.addValue('x_elastic_d2E_eta_values_6th',d2E6_eta)
        backend.addValue('x_elastic_cross_number_of_eta_polinomial_2nd',polFit2Cross)
        backend.addValue('x_elastic_cross_number_of_eta_polinomial_4th',polFit4Cross)
        backend.addValue('x_elastic_cross_number_of_eta_polinomial_6th',polFit6Cross)
        backend.addValue('x_elastic_cross_cross_values_2nd',CrossVal2_val)
        backend.addValue('x_elastic_cross_cross_values_4th',CrossVal4_val)
        backend.addValue('x_elastic_cross_cross_values_6th',CrossVal6_val)
        backend.addValue('x_elastic_cross_eta_values_2nd',CrossVal2_eta)
        backend.addValue('x_elastic_cross_eta_values_4th',CrossVal4_eta)
        backend.addValue('x_elastic_cross_eta_values_6th',CrossVal6_eta)
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
        backend.closeSection("x_elastic_section_single_configuration_calculation", elasticGIndex)

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
                  SM(r"\s*Space-group number\s*=\s*(?P<x_elastic_space_group_number>[0-9]+)"),
                  SM(r"\s*Volume of equilibrium unit cell\s*=\s*(?P<x_elastic_unit_cell_volume>[-0-9.]+)\s*\[a.u\^3\]"),
                  SM(r"\s*Maximum Lagrangian strain\s*=\s*(?P<x_elastic_max_lagrangian_strain>[0-9.]+)"),
                  SM(r"\s*Number of distorted structures\s*=\s*(?P<x_elastic_number_of_distorted_structures>[0-9]+)")
                ])
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

