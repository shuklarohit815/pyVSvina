# pyVSvina
 pyVSvina is a python based tool for Virtual Screening of a library of ligands against a protein receptor using Autodock Vina.
 # Installation
 Download the contents of repository and add it to your $PATH variable or simply use the pyVSvina script with the python3.

$ export PATH=":$PATH"

You can add above line to your .bashrc file.

# Usage:

python3 pyVSvina.py --help

![Screenshot](pySDF2pdbqt_usage.png)

# What you need
1. [pyVSvina](https://github.com/shuklarohit815/pyVSvina) for virtual screening.
2. [pySDF2PDBQT](https://github.com/shuklarohit815/pySDF2PDBQT) for ligand conversion.
3. [Autodock Vina](http://vina.scripps.edu/) for docking.
4. [Autodock Tools](https://autodock.scripps.edu/) for receptor preparation.
5. [Chimera](https://www.cgl.ucsf.edu/chimera/) for visualising docked ligand complexes.

# Ligand preparation
Please use the [pySDF2PDBQT](https://github.com/shuklarohit815/pySDF2PDBQT) tool for ligand preparation. The tool will convert the sdf files in to the pdbqt files. We will use these pdbqt format ligands for virtual screening.

# Preparing receptor for docking
For docking the ligands to receptor, receptor pdb file must be converted to pdbqt file. Our receptor is glycogen synthase kinase 3 beta [PDBID : 1J1B](https://www.rcsb.org/structure/1J1B) from which the ligand AMPPNP has been removed. We want to dock ligands from our library in the same place where AMPPNP was originally bound. The AMPPNP is the analog of ATP.

