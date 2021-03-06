# Validating Protein Structure Models
Project for UC Davis ECS 129 2020

By: Branden Lee and Kimberly Kwan

https://web.cs.ucdavis.edu/~koehl/Teaching/ECS129/projects.html

# Final Report

[Final Report - paper_D20200313.pdf](/report/paper_D20200313.pdf)

# Abstract
This project implements a simplified method for scoring the quality of a protein structure using an internal energy calculation that includes Van der Waals, electrostatic, and solvation energy. Two protein structures with accompanying pre-processed atom data files are compared using our method. Structure #2 is found to have a higher structure quality because of its lower internal energy score.

# Folder Organization
The calculation as outlined by Dr. Koehl is implemented in both python and C++ for run time comparison purposes. The python source should be used for grading since it was used for comparison calculations and results.
* `/src_py/` protein internal energy calculation source written in python using the professor provided CRD files containing pre-processed atom data
* `/src_cpp/` protein internal energy calculation source written in C++

# `/src_py/` Python 3 Source
[Python Source Directory /src_py/](/src_py/)

See the report for input file format. Default input files of the protein structures to compare are `../data/model1.crd` and `../data/model2.crd`. Default output directory is `../results/`.

## Run
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
