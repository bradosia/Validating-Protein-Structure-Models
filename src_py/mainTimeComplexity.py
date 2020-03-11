"""
Author: Branden Lee
Date: 2020-01-24 to 2020-03-06
Github: https://github.com/GoodProtein/ProScore

PLAGIARISM NOTICE
This project was created for ECS 129 course at UC Davis
and is publically hosted in a github repository. Other students
may find this repository and attempt to copy all or portions of this project.
"""

'''
@brief compares the local scores of two proteins
'''

import math
import time
import EnergyScoreMethods

def timeComplexity():
    rangeN = 100
    outputPath = "../results/algorithmTimeComplexity" + str(rangeN) + ".csv"
    # begin
    resultMap = {}
    for i in range(1, rangeN+1):
        atomMap = EnergyScoreMethods.createRandomProteinChain(i)
        runtimeProfile = EnergyScoreMethods.RuntimeProfile()
        energyScore = EnergyScoreMethods.calculateEnergyScore(atomMap, runtimeProfile)
        resultMap[i] = {}
        resultMap[i]["length"] = i
        resultMap[i]["duration"] = runtimeProfile.getDurationMS()
        print("computed chain", i, "at", int(round(energyScore)),"in",runtimeProfile.getDurationMS(),"milliseconds")

    # write to file
    n = len(resultMap)+1
    with open(outputPath, "w") as outputFile:
        outputFile.write("Protein Chain Length,Run Duration (milliseconds)\n")
        for i in range(1, n):
            outputFile.write(str(resultMap[i]["length"]) + ",")
            outputFile.write(str(resultMap[i]["duration"]) + "\n")

if __name__ == "__main__":
    timeComplexity()
