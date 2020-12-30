import os
import pint
import numpy as np
from ase import Atoms

from nomad.parsing.file_parser import Quantity, TextParser


class InfoParser(TextParser):
    def __init__(self):
        super().__init__(None)

    def init_quantities(self):
        self._quantities = [
            Quantity(
                'order', r'\s*Order of elastic constants\s*=\s*([0-9]+)', repeats=False,
                dtype=int),
            Quantity(
                'calculation_method', r'\s*Method of calculation\s*=\s*([-a-zA-Z]+)\s*',
                repeats=False),
            Quantity(
                'code_name', r'\s*DFT code name\s*=\s*([-a-zA-Z]+)', repeats=False),
            Quantity(
                'space_group_number', r'\s*Space-group number\s*=\s*([0-9]+)', repeats=False),
            Quantity(
                'equilibrium_volume', r'\s*Volume of equilibrium unit cell\s*=\s*([0-9.]+)\s*',
                unit='angstrom ** 3'),
            Quantity(
                'max_strain', r'\s*Maximum Lagrangian strain\s*=\s*([0-9.]+)', repeats=False),
            Quantity(
                'n_strains', r'\s*Number of distorted structures\s*=\s*([0-9]+)', repeats=False)]


class StructureParser(TextParser):
    def __init__(self):
        super().__init__(None)

    def init_quantities(self):
        def get_sym_pos(val):
            val = val.strip().replace('\n', '').split()
            sym = []
            pos = []
            for i in range(0, len(val), 4):
                sym.append(val[i + 3].strip())
                pos.append([float(val[j]) for j in range(i, i + 3)])
            sym_pos = dict(symbols=sym, positions=pos)
            return sym_pos

        self._quantities = [
            Quantity(
                'cellpar', r'a\s*b\s*c\n([\d\.\s]+)\n\s*alpha\s*beta\s*gamma\n([\d\.\s]+)\n+',
                repeats=False),
            Quantity(
                'sym_pos', r'Atom positions:\n\n([\s\d\.A-Za-z]+)\n\n',
                str_operation=get_sym_pos, repeats=False, convert=False)]


class DistortedParametersParser(TextParser):
    def __init__(self):
        super().__init__(None)

    def init_quantities(self):
        self._quantities = [Quantity(
            'deformation', r'Lagrangian strain\s*=\s*\(([eta\s\d\.,]+)\)',
            str_operation=lambda x: x.replace(',', '').split(), repeats=True, dtype=str)]


class FitParser(TextParser):
    def __init__(self):
        super().__init__(None)

    def init_quantities(self):

        def split_eta_val(val):
            order, val = val.strip().split(' order fit.')
            val = [float(v) for v in val.strip().split()]
            return order, val[0::2], val[1::2]

        self._quantities = [Quantity(
            'fit', r'(\w+ order fit\.\n[\d.\s\neE\-\+]+)\n', repeats=True, convert=False,
            str_operation=split_eta_val)]


class ElasticConstant2Parser(TextParser):
    def __init__(self):
        super().__init__(None)

    def init_quantities(self):
        self._quantities = [
            Quantity(
                'voigt', r'Symmetry[\s\S]+\n\s*\n([C\d\s\n\(\)\-\+\/\*]+)\n',
                shape=(6, 6), dtype=str, repeats=False),
            Quantity(
                'elastic_constant', r'Elastic constant[\s\S]+in GPa\s*:\s*\n\n([\-\d\.\s\n]+)\n',
                shape=(6, 6), dtype=float, unit='GPa', repeats=False),
            Quantity(
                'compliance', r'Elastic compliance[\s\S]+in 1/GPa\s*:\s*\n\n([\-\d\.\s\n]+)\n',
                shape=(6, 6), dtype=float, unit='1/GPa', repeats=False)]

        def str_to_modulus(val_in):
            val_in = val_in.strip().split()
            key = val_in[0]
            unit = val_in[-1] if len(val_in) == 3 else None
            val = float(val_in[1])
            val = pint.Quantity(val, unit) if unit is not None else val
            return key, val

        self._quantities.append(Quantity(
            'modulus', r',\s*(\w+)\s*=\s*([\-\+\w\. ]+?)\n', str_operation=str_to_modulus,
            repeats=True))

        self._quantities.append(Quantity(
            'eigenvalues',
            r'Eigenvalues of elastic constant \(stiffness\) matrix:\s*\n+([\-\d\.\n\s]+)\n',
            unit='GPa', repeats=False))


class ElasticConstant3Parser(TextParser):
    def __init__(self):
        super().__init__(None)

    def init_quantities(self):
        def arrange_matrix(val):
            val = val.strip().split('\n')
            matrix = [v.strip().split() for v in val if v.strip()]
            matrix = np.array(matrix).reshape((12, 18))
            arranged = []
            for i in range(2):
                for j in range(3):
                    arranged.append(
                        matrix[i * 6: (i + 1) * 6, j * 6: (j + 1) * 6].tolist())
            return arranged

        self._quantities = [
            Quantity(
                'elastic_constant', r'\%\s*\n([\s0-6A-L]*)[\n\s\%1-6\-ij]*([\s0-6A-L]*)\n',
                str_operation=arrange_matrix, dtype=str, repeats=False, convert=False),
            Quantity(
                'cijk', r'(C\d\d\d)\s*=\s*([\-\d\.]+)\s*GPa', repeats=True, convert=False)]


class ElasticProperties:
    def __init__(self):
        self._mainfile = None
        self.logger = None
        self._deform_dirs = None
        self._deform_dir_prefix = 'Dst'
        self.info = InfoParser()
        self.structure = StructureParser()
        self.distorted_parameters = DistortedParametersParser()
        self.fit = FitParser()
        self.elastic_constant_2 = ElasticConstant2Parser()
        self.elastic_constant_3 = ElasticConstant3Parser()

    @property
    def mainfile(self):
        return self._mainfile

    @mainfile.setter
    def mainfile(self, val):
        self._deform_dirs = None
        self._mainfile = val
        self.maindir = os.path.dirname(val) if val is not None else None
        self.info.mainfile = val

    @property
    def deformation_dirs(self):
        if self._deform_dirs is None:
            dirs = os.listdir(self.maindir)
            self._deform_dirs = [
                os.path.join(self.maindir, d) for d in dirs if d.startswith(self._deform_dir_prefix)]

        return self._deform_dirs

    def get_references_to_calculations(self):
        def output_file(dirname):
            code = self.info.get('code_name', '').lower()
            if code == 'exciting':
                return os.path.join(dirname, 'INFO.OUT')
            elif code == 'wien':
                return os.path.join(dirname, '%s_Converged.scf' % os.path.basename(dirname))
            elif code == 'quantum':
                return os.path.join(dirname, '%s.out' % os.path.basename(dirname))
            else:
                return None

        references = []
        for deform_dir in self.deformation_dirs:
            sub_dirs = os.listdir(deform_dir)
            for sub_dir in sub_dirs:
                calc_dir = os.path.join(deform_dir, sub_dir)
                out_file = output_file(calc_dir)
                if out_file is not None and os.path.isfile(out_file):
                    references.append(out_file)

        return references

    def get_structure_info(self):
        path = os.path.join(self.maindir, 'sgroup.out')
        if not os.path.isfile(path):
            return

        self.structure.mainfile = path

        cellpar = self.structure.get('cellpar', None)
        sym_pos = self.structure.get('sym_pos', {})

        sym = sym_pos.get('symbols', None)
        pos = sym_pos.get('positions', None)

        if cellpar is None or sym is None or pos is None:
            return

        structure = Atoms(cell=cellpar, scaled_positions=pos, symbols=sym, pbc=True)

        positions = structure.get_positions()
        positions = pint.Quantity(positions, 'angstrom')
        cell = structure.get_cell()
        cell = pint.Quantity(cell, 'angstrom')

        return sym, positions, cell

    def get_strain_energy(self):
        strains, energies = [], []

        for deform_dir in self.deformation_dirs:
            filenames = [d for d in os.listdir(deform_dir) if d.endswith('Energy.dat')]
            if not filenames:
                continue

            path = os.path.join(deform_dir, filenames[-1])
            data = np.loadtxt(path).T
            strains.append(list(data[0]))
            # the peculiarity of the x_elastic_strain_diagram_values metainfo that it does
            # not have the energy unit
            energies.append(list(pint.Quantity(data[1], 'hartree').to('J').magnitude))

        return strains, energies

    def get_strain_stress(self):
        strains = {'Lagrangian-stress': [], 'Physical-stress': []}
        stresses = {'Lagrangian-stress': [], 'Physical-stress': []}

        for deform_dir in self.deformation_dirs:
            filenames = [d for d in os.listdir(deform_dir) if d.endswith('stress.dat')]

            for filename in filenames:
                path = os.path.join(deform_dir, filename)
                if not os.path.isfile(path):
                    continue

                with open(path) as f:
                    lines = f.readlines()

                strain, stress = [], []
                for line in lines:
                    val = line.strip().split()
                    if not val[0].strip().replace('.', '').isdecimal():
                        continue

                    strain.append(float(val[0]))
                    stress.append([float(v) for v in val[1:7]])

                stype = filename.rstrip('.dat').split('_')[-1]
                strains[stype].append(strain)
                stresses[stype].append(stress)

        return strains, stresses

    def get_deformation_types(self):
        path = os.path.join(self.maindir, 'Distorted_Parameters')
        self.distorted_parameters.mainfile = path
        return self.distorted_parameters.get('deformation')

    def _get_fit(self, path_dir, file_ext):
        path_dir = os.path.join(self.maindir, path_dir)

        if not os.path.isdir(path_dir):
            return

        paths = [p for p in os.listdir(path_dir) if p.endswith(file_ext)]
        paths.sort()

        if not paths:
            return

        eta, val = {}, {}
        for path in paths:
            self.fit.mainfile = os.path.join(path_dir, path)
            fit_results = self.fit.get('fit', [])
            for result in fit_results:
                eta.setdefault(result[0], [])
                val.setdefault(result[0], [])
                eta[result[0]].append(result[1])
                val[result[0]].append(result[2])

        return eta, val

    def get_energy_fit(self):
        energy_fit = dict()

        for file_ext in ['d2E.dat', 'd3E.dat', 'ddE.dat']:
            result = self._get_fit('Energy-vs-Strain', file_ext)
            if result is None:
                continue

            result = list(result)
            result[1] = {
                key: pint.Quantity(
                    val, 'GPa').to('Pa').magnitude for key, val in result[1].items()}
            energy_fit['d2e'] = result

        result = self._get_fit('Energy-vs-Strain', 'CVe.dat')
        if result is not None:
            result = list(result)
            result[1] = {
                key: pint.Quantity(
                    val, 'hartree').to('J').magnitude for key, val in result[1].items()}
            energy_fit['cross-validation'] = result

        return energy_fit

    def get_stress_fit(self):
        stress_fit = dict()
        stress_fit['dtn'] = [[]] * 6
        stress_fit['cross-validation'] = [[]] * 6

        for strain_index in range(1, 7):
            result = self._get_fit('Stress-vs-Strain', '%d_dS.dat' % strain_index)
            if result is not None:
                result[1] = {key: pint.Quantity(val, 'GPa') for key, val in result[1].items()}
                stress_fit['dtn'][strain_index - 1] = result

            result = self._get_fit('Stress-vs-Strain', '%d_CVe.dat' % strain_index)
            if result is not None:
                result[1] = {key: pint.Quantity(val, 'hartree') for key, val in result[1].items()}
                stress_fit['cross-validation'][strain_index - 1] = result

        return stress_fit

    def get_input(self):
        paths = os.listdir(self.maindir)
        path = None
        order = self.info.get('order', 2)
        for p in paths:
            if 'ElaStic_' in p and p.endswith('.in') and str(order) in p:
                path = p
                break

        if path is None:
            return

        calc_method = self.info.get('calculation_method')

        eta_ec = []
        fit_ec = []

        def _is_number(var):
            try:
                float(var)
                return True
            except Exception:
                return False

        path = os.path.join(self.maindir, path)

        with open(path) as f:
            while True:
                line = f.readline()
                if not line:
                    break

                if calc_method.lower() == 'energy':
                    _, eta, fit = line.strip().split()
                    eta_ec.append(float(eta))
                    fit_ec.append(int(fit))

                elif calc_method.lower() == 'stress':
                    val = line.strip().split()
                    if not _is_number(val[0]):
                        eta_ec.append([float(val[i + 1]) for i in range(6)])
                    else:
                        fit_ec.append([int(val[i]) for i in range(6)])

                else:
                    pass

        return eta_ec, fit_ec

    def get_elastic_constants_order2(self):
        path = os.path.join(self.maindir, 'ElaStic_2nd.out')

        self.elastic_constant_2.mainfile = path

        matrices = dict()
        for key in ['voigt', 'elastic_constant', 'compliance']:
            val = self.elastic_constant_2.get(key, None)
            if val is not None:
                matrices[key] = val

        moduli = dict()
        for modulus in self.elastic_constant_2.get('modulus', []):
            moduli[modulus[0]] = modulus[1]

        eigenvalues = self.elastic_constant_2.get('eigenvalues')

        return matrices, moduli, eigenvalues

    def get_elastic_constants_order3(self):
        path = os.path.join(self.maindir, 'ElaStic_3rd.out')
        self.elastic_constant_3.mainfile = path

        elastic_constant_str = self.elastic_constant_3.get('elastic_constant')
        if elastic_constant_str is None:
            return

        cijk = dict()
        for element in self.elastic_constant_3.get('cijk', []):
            cijk[element[0]] = float(element[1])

        # formulas for the coefficients
        coeff_A = cijk.get('C111', 0) + cijk.get('C112', 0) - cijk.get('C222', 0)
        coeff_B = -(cijk.get('C115', 0) + 3 * cijk.get('C125', 0)) / 2
        coeff_C = (cijk.get('C114', 0) + 3 * cijk.get('C124', 0)) / 2
        coeff_D = -(2 * cijk.get('C111', 0) + cijk.get('C112', 0) - 3 * cijk.get('C222', 0)) / 4
        coeff_E = -cijk.get('C114', 0) - 2 * cijk.get('C124', 0)
        coeff_F = -cijk.get('C115', 0) - 2 * cijk.get('C125', 0)
        coeff_G = -(cijk.get('C115', 0) - cijk.get('C125', 0)) / 2
        coeff_H = (cijk.get('C114', 0) - cijk.get('C124', 0)) / 2
        coeff_I = (2 * cijk.get('C111', 0) - cijk.get('C112', 0) - cijk.get('C222', 0)) / 4
        coeff_J = (cijk.get('C113', 0) - cijk.get('C123', 0)) / 2
        coeff_K = -(cijk.get('C144', 0) - cijk.get('C155', 0)) / 2

        space_group_number = self.info.get('space_group_number')

        if space_group_number <= 148:  # rhombohedral II
            coefficients = dict(
                A=coeff_A, B=coeff_B, C=coeff_C, D=coeff_D, E=coeff_E, F=coeff_F, G=coeff_G,
                H=coeff_H, I=coeff_I, J=coeff_J, K=coeff_K)
        elif space_group_number <= 167:  # rhombohedral I
            coefficients = dict(
                A=coeff_A, B=coeff_C, C=coeff_D, D=coeff_E, E=coeff_H, F=coeff_I, G=coeff_J,
                H=coeff_K)
        elif space_group_number <= 176:  # hexagonal II
            coefficients = dict(
                A=coeff_A, B=coeff_D, C=coeff_I, D=coeff_J, E=coeff_K)
        elif space_group_number <= 194:  # hexagonal I
            coefficients = dict(
                A=coeff_A, B=coeff_D, C=coeff_I, D=coeff_J, E=coeff_K)
        else:
            coefficients = dict()

        # assign values to the elastic constant matrix from the independent ec and coefficients
        elastic_constant = np.zeros((6, 6, 6))
        for i in range(6):
            for j in range(6):
                for k in range(6):
                    val = elastic_constant_str[i][j][k]
                    if val == '0':
                        elastic_constant[i][j][k] = 0
                    elif val.isdigit():
                        elastic_constant[i][j][k] = cijk['C%s' % val]
                    else:
                        elastic_constant[i][j][k] = coefficients.get(val, 0)

        return elastic_constant
