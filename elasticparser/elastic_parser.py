import os
import numpy as np
import logging

from nomadcore.unit_conversion import unit_conversion
from nomad.datamodel.metainfo.public import section_run, section_system,\
    section_single_configuration_calculation, section_method, section_calculation_to_calculation_refs,\
    Workflow, Elastic

from elasticparser.metainfo.elastic import x_elastic_section_strain_diagrams,\
    x_elastic_section_fitting_parameters

from elasticparser.elastic_properties import ElasticProperties

a_to_m = unit_conversion.convert_unit_function('angstrom', 'meter')
ha_to_J = unit_conversion.convert_unit(1, 'hartree', 'J')
giga = 10 ** 9


class ElasticParserInterface:
    def __init__(self, filepath, archive, logger=None):
        self.filepath = os.path.abspath(filepath)
        self.archive = archive
        self.logger = logger if logger is not None else logging
        self.properties = ElasticProperties(self.filepath)

    def parse_strain(self):
        sec_scc = self.archive.section_run[-1].section_single_configuration_calculation[-1]
        method = self.properties.info['calculation_method'].lower()

        if method == 'energy':
            strain, energy = self.properties.get_strain_energy()
            if not strain:
                self.logger.warn('Error getting strain and energy data')
                return

            n_strains = self.properties.info['n_strains']

            sec_strain_diagram = sec_scc.m_create(x_elastic_section_strain_diagrams)
            sec_strain_diagram.x_elastic_strain_diagram_type = 'energy'
            sec_strain_diagram.x_elastic_strain_diagram_number_of_eta = len(strain[0])
            sec_strain_diagram.x_elastic_strain_diagram_eta_values = strain
            sec_strain_diagram.x_elastic_strain_diagram_values = np.array(energy) * ha_to_J

            poly_fit_2 = int((n_strains - 1) / 2)

            poly_fit = {
                '2nd': poly_fit_2, '3rd': poly_fit_2 - 1, '4th': poly_fit_2 - 1,
                '5th': poly_fit_2 - 2, '6th': poly_fit_2 - 2, '7th': poly_fit_2 - 3}

            energy_fit = self.properties.get_energy_fit()
            if not energy_fit:
                self.logger.warn('Error getting energy fit data')
                return

            for diagram_type in ['cross-validation', 'd2e']:
                for fit_order in energy_fit[diagram_type][0].keys():
                    sec_strain_diagram = sec_scc.m_create(x_elastic_section_strain_diagrams)
                    sec_strain_diagram.x_elastic_strain_diagram_type = diagram_type
                    sec_strain_diagram.x_elastic_strain_diagram_polynomial_fit_order = int(fit_order[:-2])
                    sec_strain_diagram.x_elastic_strain_diagram_number_of_eta = poly_fit.get(fit_order, None)
                    sec_strain_diagram.x_elastic_strain_diagram_eta_values = energy_fit[diagram_type][0][fit_order]
                    convert = giga if diagram_type == 'd2e' else ha_to_J
                    sec_strain_diagram.x_elastic_strain_diagram_values = np.array(energy_fit[diagram_type][1][fit_order]) * convert

        elif method == 'stress':
            strain, stress = self.properties.get_strain_stress()
            for diagram_type in ['Lagrangian-stress', 'Physical-stress']:
                strain_i = strain[diagram_type]
                stress_i = np.transpose(np.array(stress[diagram_type]), axes=(2, 0, 1))
                if not strain_i:
                    continue

                for si in range(6):
                    sec_strain_diagram = sec_scc.m_create(x_elastic_section_strain_diagrams)
                    sec_strain_diagram.x_elastic_strain_diagram_type = diagram_type
                    sec_strain_diagram.x_elastic_strain_diagram_stress_Voigt_component = si + 1
                    sec_strain_diagram.x_elastic_strain_diagram_number_of_eta = len(strain_i[0])
                    sec_strain_diagram.x_elastic_strain_diagram_eta_values = strain_i
                    sec_strain_diagram.x_elastic_strain_diagram_values = stress_i[si]

            stress_fit = self.properties.get_stress_fit()
            for diagram_type in ['cross-validation', 'dtn']:
                if stress_fit.get(diagram_type, None) is None:
                    continue

                for si in range(6):
                    for fit_order in stress_fit[diagram_type][si][0].keys():
                        sec_strain_diagram = sec_scc.m_create(x_elastic_section_strain_diagrams)
                        sec_strain_diagram.x_elastic_strain_diagram_type = diagram_type
                        sec_strain_diagram.x_elastic_strain_diagram_stress_Voigt_component = si + 1
                        sec_strain_diagram.x_elastic_strain_diagram_polynomial_fit_order = int(fit_order[:-2])
                        sec_strain_diagram.x_elastic_strain_diagram_number_of_eta = poly_fit.get(fit_order, None)
                        sec_strain_diagram.x_elastic_strain_diagram_eta_values = stress_fit[diagram_type][si][0][fit_order]
                        convert = giga if diagram_type == 'dtn' else ha_to_J
                        sec_strain_diagram.x_elastic_strain_diagram_values = np.array(stress_fit[diagram_type][si][1][fit_order]) * convert

    def parse_elastic_constant(self):
        sec_scc = self.archive.section_run[-1].section_single_configuration_calculation[-1]

        order = self.properties.info['order']

        if order == 2:
            matrices, moduli, eigenvalues = self.properties.get_elastic_constants_order2()

            sec_scc.x_elastic_2nd_order_constants_notation_matrix = matrices['voigt']
            sec_scc.x_elastic_2nd_order_constants_matrix = matrices['elastic_constant'] * giga
            sec_scc.x_elastic_2nd_order_constants_compliance_matrix = matrices['compliance'] / giga

            sec_scc.x_elastic_Voigt_bulk_modulus = moduli.get('B_V', moduli.get('K_V')) * giga
            sec_scc.x_elastic_Voigt_shear_modulus = moduli['G_V'] * giga

            sec_scc.x_elastic_Reuss_bulk_modulus = moduli.get('B_R', moduli.get('K_R')) * giga
            sec_scc.x_elastic_Reuss_shear_modulus = moduli['G_R'] * giga

            sec_scc.x_elastic_Hill_bulk_modulus = moduli.get('B_H', moduli.get('K_H')) * giga
            sec_scc.x_elastic_Hill_shear_modulus = moduli['G_H'] * giga

            sec_scc.x_elastic_Voigt_Young_modulus = moduli['E_V'] * giga
            sec_scc.x_elastic_Voigt_Poisson_ratio = moduli['nu_V']
            sec_scc.x_elastic_Reuss_Young_modulus = moduli['E_R'] * giga
            sec_scc.x_elastic_Reuss_Poisson_ratio = moduli['nu_R']
            sec_scc.x_elastic_Hill_Young_modulus = moduli['E_H'] * giga
            sec_scc.x_elastic_Hill_Poisson_ratio = moduli['nu_H']

            sec_scc.x_elastic_eigenvalues = eigenvalues * giga

        elif order == 3:
            elastic_constant = self.properties.get_elastic_constants_order3()

            sec_scc.x_elastic_3rd_order_constants_matrix = elastic_constant

    def parse(self):

        sec_run = self.archive.m_create(section_run)

        sec_run.program_name = 'elastic'
        sec_run.program_version = '1.0'

        sec_system = sec_run.m_create(section_system)

        symbols, positions, cell = self.properties.get_structure_info()
        volume = self.properties.info['equilibrium_volume']
        volume = a_to_m(a_to_m(a_to_m(volume)))

        sec_system.atom_labels = symbols
        sec_system.atom_positions = a_to_m(positions)
        sec_system.simulation_cell = a_to_m(cell)
        sec_system.configuration_periodic_dimensions = [True, True, True]
        sec_system.x_elastic_space_group_number = self.properties.info['space_group_number']
        sec_system.x_elastic_unit_cell_volume = volume

        sec_method = sec_run.m_create(section_method)
        sec_method.x_elastic_elastic_constant_order = self.properties.info['order']
        sec_method.x_elastic_calculation_method = self.properties.info['calculation_method']
        sec_method.x_elastic_code = self.properties.info['code_name']
        sec_method.x_elastic_max_lagrangian_strain = self.properties.info['max_strain']
        sec_method.x_elastic_number_of_distorted_structures = self.properties.info['n_strains']

        deformation_types = self.properties.get_deformation_types()
        sec_method.x_elastic_deformation_types = deformation_types
        sec_method.x_elastic_number_of_deformations = len(self.properties.deformation_dirs)

        references = self.properties.get_references_to_calculations()
        sec_scc = sec_run.m_create(section_single_configuration_calculation)
        for reference in references:
            sec_calc_ref = sec_scc.m_create(section_calculation_to_calculation_refs)
            sec_calc_ref.calculation_to_calculation_external_url = reference
            sec_calc_ref.calculation_to_calculation_kind = 'source_calculation'

        fit_input = self.properties.get_input()
        sec_fit_par = sec_method.m_create(x_elastic_section_fitting_parameters)
        sec_fit_par.x_elastic_fitting_parameters_eta = fit_input[0]
        sec_fit_par.x_elastic_fitting_parameters_polynomial_order = fit_input[1]

        self.parse_strain()

        self.parse_elastic_constant()

        sec_scc.single_configuration_to_calculation_method_ref = sec_method
        sec_scc.single_configuration_calculation_to_system_ref = sec_system

        sec_workflow = self.archive.m_create(Workflow)
        sec_workflow.workflow_type = 'elastic'
        sec_elastic = sec_workflow.m_create(Elastic)
        sec_elastic.elastic_calculation_method = self.properties.info['calculation_method'].lower()
        sec_elastic.elastic_constants_order = self.properties.info['order']
        sec_elastic.strain_maximum = self.properties.info['max_strain']
