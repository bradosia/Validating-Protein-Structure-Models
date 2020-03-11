"""
Author: Branden Lee
Date: 2020-01-24 to 2020-03-06
Github: https://github.com/GoodProtein/ProScore

PLAGIARISM NOTICE
This project was created for ECS 129 course at UC Davis
and is publically hosted in a github repository. Other students
may find this repository and attempt to copy all or portions of this project.
"""

"""
@brief compares the local scores of two proteins
"""

import math
import time
import EnergyScoreMethods

def atomScoreCompare():
    rangeN = 100
    inputFilePath1 = "../data/model1.crd"
    inputFilePath2 = "../data/model2.crd"
    outputPath = "../results/proteinAtomScoreCompare" + str(rangeN) + ".csv"
    # process protein #1
    runtimeProfile1 = EnergyScoreMethods.RuntimeProfile()
    atomMap1 = EnergyScoreMethods.atomMapFromCRD(inputFilePath1, runtimeProfile1)
    print("Protein #1 file processing time:",
          runtimeProfile1.getDurationMS(), "milliseconds")
    # process protein #2
    runtimeProfile2 = EnergyScoreMethods.RuntimeProfile()
    atomMap2 = EnergyScoreMethods.atomMapFromCRD(inputFilePath2, runtimeProfile2)
    print("Protein #2 file processing time:",
          runtimeProfile2.getDurationMS(), "milliseconds")
    differenceMap = {}
    n = len(atomMap1) + 2 -rangeN
    for i in range(0, n):
        print("Beginning Iteration", i, "to", i+rangeN)
        # find submap
        subMap1 = EnergyScoreMethods.atomSubMap(atomMap1, i, i+rangeN)
        subMap2 = EnergyScoreMethods.atomSubMap(atomMap2, i, i+rangeN)
        #print(subMap1)
        #print(subMap2)
        # calculate protein #1
        runtimeProfile3 = EnergyScoreMethods.RuntimeProfile()
        energyScore1 = EnergyScoreMethods.calculateEnergyScore(subMap1, runtimeProfile3)
        print("Protein #1 calculate internal energy processing time:",
              runtimeProfile3.getDurationMS(), "milliseconds")
        print("The internal energy of the protein #1 is",
              int(round(energyScore1)), "kcal/mol")
        # calculate protein #2
        runtimeProfile4 = EnergyScoreMethods.RuntimeProfile()
        energyScore2 = EnergyScoreMethods.calculateEnergyScore(subMap2, runtimeProfile4)
        print("Protein #2 calculate internal energy processing time:",
              runtimeProfile4.getDurationMS(), "milliseconds")
        print("The internal energy of the protein #2 is",
              int(round(energyScore2)), "kcal/mol")
        # difference map data
        differenceMap[i] = {}
        differenceMap[i]["atomIndexStart"] = i
        differenceMap[i]["atomIndexEnd"] = i+rangeN
        differenceMap[i]["protein1"] = energyScore1
        differenceMap[i]["protein2"] = energyScore2
        differenceMap[i]["difference"] = energyScore1-energyScore2
    # write to file
    n = len(differenceMap)
    with open(outputPath, "w") as outputFile:
        outputFile.write("Atom Index Start,Atom Index End,Protein #1 Energy Score,Protein #2 Energy Score,Energy Score Difference\n")
        for i in range(0, n):
            if i in differenceMap:
                outputFile.write(str(differenceMap[i]["atomIndexStart"]) + ",")
                outputFile.write(str(differenceMap[i]["atomIndexEnd"]) + ",")
                outputFile.write(str(int(round(differenceMap[i]["protein1"]))) + ",")
                outputFile.write(str(int(round(differenceMap[i]["protein2"]))) + ",")
                outputFile.write(str(int(round(differenceMap[i]["difference"]))) + "\n")

if __name__ == "__main__":
    atomScoreCompare()
