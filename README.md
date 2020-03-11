# Protein-Structure-Energy
Project for UC Davis ECS 129 2020
https://web.cs.ucdavis.edu/~koehl/Teaching/ECS129/projects.html

# PLEASE DO NOT GRADE UNTIL AFTER MARCH 13 DUE DATE
# PLEASE DO NOT GRADE UNTIL AFTER MARCH 13 DUE DATE
# PLEASE DO NOT GRADE UNTIL AFTER MARCH 13 DUE DATE

# PROJECT PROGRESS
- [x] Open .PDB file
- [X] Parse .CRD file atom properties into an efficient data structure
- [X] Implement mathematical computation for total protein internal energy
- [X] Perform protein structure comparison
- [ ] `50%` Report - Introduction
  - [ ] `50%` Presentation of the problem
  - [ ] `50%` Previous work on the topic
- [ ] `90%` Report - Methods
  - [ ] `90%` Description of your algorithm
  - [ ] `90%` Brief analysis
- [ ] `90%` Report - Results
  - [ ] `90%` Presentation
  - [ ] `90%` Analysis
- [ ] `50%` Report - Discussion
- [ ] `60%` Report - Bibliography

# Folder Organization
* `/CRD_File_py_src/` protein internal energy calculation written in python using the professor provided CRD files containing pre-fetched atom variables
* `/PDB_File_py_src/` protein internal energy calculation written in python using self-provided atom variables
* `/cpp_src/` protein internal energy calculation written in C++

# Run time tests

Run with python:

![python](https://github.com/UC-Davis-ECS-129-Project/Protein-Internal-Energy/blob/master/share/console-run-py_D20200227.png)

Run with C++:

![cpp](https://raw.githubusercontent.com/UC-Davis-ECS-129-Project/Protein-Internal-Energy/master/share/console-run-cpp_D20200227.png)

# `/CRD_File_py_src/` Environment Set Up
Use python 3
```shell
cd CRD_File_py_src
python main.py
```

# `/PDB_File_py_src/` Environment Set Up
## Windows
download https://bootstrap.pypa.io/get-pip.py
```shell
python get-pip.py
```

## MSYS2
```shell
pacman -S python3-pip
```

## MacOS
```shell
sudo easy_install pip
sudo pip install --upgrade pip
```

## Get Libraries
```shell
pip install biopython
```

## Run Program
Use python 3
```shell
cd PDB_File_py_src
python main.py
```

# `/cpp_src/` Environment Set Up
Use cmake

Xcode
```shell
cmake -G"Xcode" -B build
```

MSYS
```shell
cmake -G"MSYS Makefiles" -B build
cd build
make
```
