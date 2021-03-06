#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
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

import pytest
import numpy as np

from nomad.datamodel import EntryArchive
from elasticparser import ElasticParser


def approx(value, abs=0, rel=1e-6):
    return pytest.approx(value, abs=abs, rel=rel)


@pytest.fixture(scope='module')
def parser():
    return ElasticParser()


def test_2nd(parser):
    archive = EntryArchive()
    parser.parse('tests/data/2nd/INFO_ElaStic', archive, None)

    sec_system = archive.section_run[0].section_system[0]
    assert np.shape(sec_system.atom_positions) == (8, 3)
    assert sec_system.atom_positions[3][1].magnitude == approx(2.5186875e-10)
    assert sec_system.lattice_vectors[2][2].magnitude == approx(6.7165e-10)
    assert sec_system.x_elastic_space_group_number == 227

    sec_method = archive.section_run[0].section_method[0]
    assert sec_method.x_elastic_code == 'exciting'
    assert sec_method.x_elastic_deformation_types[2][5] == '2eta'
    sec_fit_parameters = sec_method.x_elastic_section_fitting_parameters[0]
    assert sec_fit_parameters.x_elastic_fitting_parameters_eta[0] == 0.05

    sec_scc = archive.section_run[0].section_single_configuration_calculation[0]
    sec_strain = sec_scc.x_elastic_section_strain_diagrams
    assert len(sec_strain) == 7
    assert sec_strain[0].x_elastic_strain_diagram_eta_values[1][3] == -0.02
    assert sec_strain[0].x_elastic_strain_diagram_values[2][5] == approx(-3.30877062e-16)
    assert sec_strain[3].x_elastic_strain_diagram_type == 'cross-validation'
    assert sec_strain[2].x_elastic_strain_diagram_eta_values[1][2] == 0.03
    assert sec_strain[6].x_elastic_strain_diagram_values[2][4] == approx(6.8708895e+12)
    assert sec_strain[4].x_elastic_strain_diagram_polynomial_fit_order == 6

    assert sec_scc.x_elastic_2nd_order_constants_notation_matrix[1][2] == 'C12'
    assert sec_scc.x_elastic_2nd_order_constants_matrix[0][2].magnitude == approx(1.008e+11)
    assert sec_scc.x_elastic_2nd_order_constants_compliance_matrix[3][3].magnitude == approx(1.75e-12)
    assert sec_scc.x_elastic_Voigt_bulk_modulus.magnitude == approx(4.4937e+11)
    assert sec_scc.x_elastic_Voigt_shear_modulus.magnitude == approx(5.3074e+11)
    assert sec_scc.x_elastic_Reuss_bulk_modulus.magnitude == approx(4.4937e+11)
    assert sec_scc.x_elastic_Reuss_shear_modulus.magnitude == approx(5.2574e+11)
    assert sec_scc.x_elastic_Hill_bulk_modulus.magnitude == approx(4.4937e+11)
    assert sec_scc.x_elastic_Hill_shear_modulus.magnitude == approx(5.2824e+11)
    assert sec_scc.x_elastic_Voigt_Young_modulus.magnitude == approx(1.14245e+12)
    assert sec_scc.x_elastic_Voigt_Poisson_ratio == 0.08
    assert sec_scc.x_elastic_Reuss_Young_modulus.magnitude == approx(1.1347e+12)
    assert sec_scc.x_elastic_Reuss_Poisson_ratio == 0.08
    assert sec_scc.x_elastic_Hill_Young_modulus.magnitude == approx(1.13858e+12)
    assert sec_scc.x_elastic_Hill_Poisson_ratio == 0.08
    assert sec_scc.x_elastic_eigenvalues[1].magnitude == approx(1.3481e+12)

    assert len(sec_scc.section_calculation_to_calculation_refs) == 33


def test_3rd(parser):
    archive = EntryArchive()
    parser.parse('tests/data/3rd/INFO_ElaStic', archive, None)

    sec_scc = archive.section_run[0].section_single_configuration_calculation[0]
    sec_strain = sec_scc.x_elastic_section_strain_diagrams
    assert len(sec_strain) == 7
    assert len(sec_strain[1].x_elastic_strain_diagram_eta_values) == 10
    assert sec_strain[2].x_elastic_strain_diagram_eta_values[1][3] == 0.07
    assert sec_strain[3].x_elastic_strain_diagram_values[8][7] == approx(2.06899957e-23)

    assert sec_scc.x_elastic_3rd_order_constants_matrix[3][1][3].magnitude == approx(1.274e+10)
    assert sec_scc.x_elastic_3rd_order_constants_matrix[5][2][5].magnitude == approx(1.2825e+10)
    assert sec_scc.x_elastic_3rd_order_constants_matrix[0][0][1].magnitude == approx(-1.18334e+12)


def test_stress(parser):
    # TODO no example found
    pass
