from Bio.PDB import *

# Brad: This code is suppose to download the PDB file,
# but instead it gives me a .cif file
# pdbl = PDBList()
# pdbl.retrieve_pdb_file('1FAT')

# Brad: Prints each atom in the protein
p = PDBParser()
structure = p.get_structure('X', 'data/model1.pdb')
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print (atom)