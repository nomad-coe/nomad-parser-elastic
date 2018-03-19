# elastic-parser

## Main file

The main file is INFO\_ElaStic. The parsing starts from this one and it fails if it is not present.

## Other files

 The following files must be in the same folder as INFO\_ElaStic:

 * \*.xml (The name is chosen by the user, but it must be an exciting xml input file): data about the initial unit cell. 
 * Distorted\_Parameters: distortions used for the calculation.
 * ElaStic\_2nd.in(_3rd.out): maximum Lagrangian strain and fit order.
 * ElaStic\_2nd.out(_3rd.out): main output of the code.

 In the same folder as INFO\_ElaStic the must be a folder Energy\-vs\-Strain. Here there are the files:

 * \*\_CVe.dat: the Cross\-Validation Error.
 * \*\_d2E.dat: second\-derivative of the energy.
 * \*\-Energy.dat: energy\-vs\-strain.

