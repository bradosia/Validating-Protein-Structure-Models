# Validating Protein Structure Models
Project for UC Davis ECS 129 2020

By: Branden Lee and Kimberly Kwan

https://web.cs.ucdavis.edu/~koehl/Teaching/ECS129/projects.html

# PLEASE DO NOT GRADE UNTIL AFTER MARCH 13 DUE DATE
# PLEASE DO NOT GRADE UNTIL AFTER MARCH 13 DUE DATE
# PLEASE DO NOT GRADE UNTIL AFTER MARCH 13 DUE DATE

# Final Report
[Report Directory /report/](/report/)

# Folder Organization
The calculation as outlined by Dr. Koehl is implemented in both python and C++ for run time comparison purposes. The python source should be used for grading since it was used for comparison calculations and results.
* `/src_py/` protein internal energy calculation source written in python using the professor provided CRD files containing pre-processed atom data
* `/src_cpp/` protein internal energy calculation source written in C++

# `/src_py/` Python Source Run
Use python 3
```shell
cd src_py
python mainEnergyScore.py
```

![python](https://github.com/UC-Davis-ECS-129-Project/Protein-Internal-Energy/blob/master/share/console-run-py_D20200227.png)

# `/src_cpp/` C++ Source Run
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

## Run
```shell
./protein-internal-energy.exe
```

![cpp](https://raw.githubusercontent.com/UC-Davis-ECS-129-Project/Protein-Internal-Energy/master/share/console-run-cpp_D20200227.png)