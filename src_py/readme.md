# Python 3 Source

See the report for input file format. Default input files of the protein structures to compare are `../data/model1.crd` and `../data/model2.crd`. Default output directory is `../results/`.

## Global Structure Comparison
```shell
cd src_py
python mainEnergyScore.py
```
![python](https://github.com/bradosia/Validating-Protein-Structure-Models/blob/master/share/console-run-py_D20200312.png)

Specify the input files using
```shell
python mainEnergyScore.py myProteinFile1.crd myProteinFile2.crd
```

Output data dump as .csv format. Used for debugging.
```shell
python mainEnergyScore.py myProteinFile1.crd myProteinFile2.crd -o -d outputDirectory
```

## Local Structure Comparison (By Atoms)

Computes the score difference between two protein structures locally by creating user-defined substrings of atoms of M length iterating atoms 0 to N. 

[Output Directory ../results/](../results/)
```shell
python mainAtomScoreCompare.py 50
```

Specify input files, range of 20, verbose, and outputDirectory
```shell
python mainAtomScoreCompare.py ../data/model1.crd ../data/model2.crd 20 -v -d outputDirectory
```

## Local Structure Comparison (By Residues)

Computes the score difference between two protein structures locally by creating user-defined substrings of residues of M length iterating atoms 0 to N. 

[Output Directory ../results/](../results/)
```shell
python mainResidueScoreCompare.py 10
```

Specify input files, range of 5, verbose, and outputDirectory
```shell
python mainResidueScoreCompare.py ../data/model1.crd ../data/model2.crd 5 -v -d outputDirectory
```

## Compute time complexity

```shell
python mainTimeComplexity.py 100
```