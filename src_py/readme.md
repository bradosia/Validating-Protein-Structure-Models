# Python 3 Source Run

See the report for input file format. Default input files of the protein structures to compare are `../data/model1.crd` and `../data/model2.crd`
```shell
cd src_py
python mainEnergyScore.py
```
![python](https://github.com/bradosia/Validating-Protein-Structure-Models/blob/master/share/console-run-py_D20200312.png)

Specify the input files using
```shell
cd src_py
python mainEnergyScore.py myProteinFile1.crd myProteinFile2.crd
```

# mainAtomScoreCompare.py

Computes the score difference between two proteins locally by creating arbitrarily defined substrings of atoms of M length iterating atoms 0 to N.
