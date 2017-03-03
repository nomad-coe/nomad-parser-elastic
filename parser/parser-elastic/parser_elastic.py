from builtins import object
import setup_paths
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

# description of the input
mainFileDescription = \
           SM(name = 'root',
              weak = False,
              startReStr = "",
              subMatchers = [
              SM(name = 'input',
#                weak = True,
#                startReStr = r"\s*Order of elastic constants\s*=\s*[0-9]",
                startReStr = "",
#                endReStr = r"\*sNumber of distorted structures\*s=\s*(?P<x_elastic_number_of_disordered_structures>[0-9]+)",
                repeats = False,
                required = False,
                forwardMatch = False,
                sections   = ['section_run'],
                subMatchers = [
                  SM(r"\s*Order of elastic constants\s*=\s*(?P<x_elastic_elastic_constant_order>[0-9]+)"),
                  SM(r"\s*Method of calculation\s*=\s*(?P<x_elastic_calculation_method>[-a-zA-Z]+)"),
                  SM(r"\s*DFT code name\s*=\s*(?P<x_elastic_code>[-a-zA-Z]+)"),
                  SM(r"\s*Space-group number\s*=\s*(?P<x_elastic_space_group_number>[0-9]+)"),
                  SM(r"\s*Volume of equilibrium unit cell\s*=\s*(?P<x_elastic_unit_cell_volume>[-0-9.]+)\s*\[a.u\^3\]"),
                  SM(r"\s*Maximum Lagrangian strain\s*=\s*(?P<x_elastic_max_lagrangian_strain>[0-9.]+)"),
                  SM(r"\s*Number of distorted structures\s*=\s*(?P<x_elastic_number_of_disordered_structures>[0-9]+)")
                ])
              ])

#mainFileDescription = SM(name = 'root',
#              startReStr = Order of elastic constants\*s=\s*(?P<x_elastic_elastic_constant_order>[0-9]+)"",
#              subMatchers = [
#  SM(name = 'newRun',
#                startReStr = "",
#                sections   = ['section_run'],
#                subMatchers = [
#                  SM(r"\*sOrder of elastic constants\*s=\s*(?P<x_elastic_elastic_constant_order>[0-9]+)"),
#                  SM(r"\*sMethod of calculation\*s=\s*(?P<x_elastic_calculation_method>[-a-zA-Z]+)"),
#                  SM(r"\*sDFT code name\*s=\s*(?P<x_elastic_code>[-a-zA-Z]+)"),
#                  SM(r"\*sSpace-group number\*s=\s*(?P<x_elastic_space_group_number>[0-9]+)"),
#                  SM(r"\*sVolume of equilibrium unit cell\*s=\s*(?P<x_elastic_unit_cell_volume>[-0-9]+)\*s\[a.u\^3\]"),
#                  SM(r"\*sMaximum Lagrangian strain\*s=\s*(?P<x_elastic_max_lagrangian_strain>[0-9.]+)"),
#                  SM(r"\*sNumber of distorted structures\*s=\s*(?P<x_elastic_number_of_disordered_structures>[0-9]+)")
#                ])
#    ])

# loading metadata from nomad-meta-info/meta_info/nomad_meta_info/fhi_aims.nomadmetainfo.json

parserInfo = {
  "name": "elastic_parser",
  "version": "1.0"
}

metaInfoPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../../nomad-meta-info/meta_info/nomad_meta_info/elastic.nomadmetainfo.json"))
metaInfoEnv, warnings = loadJsonFile(filePath = metaInfoPath, dependencyLoader = None, extraArgsHandling = InfoKindEl.ADD_EXTRA_ARGS, uri = None)

if __name__ == "__main__":
    superContext = SampleContext()
    mainFunction(mainFileDescription, metaInfoEnv, parserInfo, superContext = superContext)
