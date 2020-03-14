"""
Author: Branden Lee
Date: 2020-01-24 to 2020-03-06
Github: https://github.com/bradosia/Validating-Protein-Structure-Models

PLAGIARISM NOTICE
This project was created for ECS 129 course at UC Davis
and is publically hosted in a github repository. Other students
may find this repository and attempt to copy all or portions of this project.
"""

'''
@brief Compares the local scores of two proteins with residues.
'''

import argparse, sys # getopt, exit
import os # makedirs
import math
import time
import EnergyScoreMethods

def residueScoreCompare():
    # default options
    rangeN = 20
    inputFilePath1 = "../data/model1.crd"
    inputFilePath2 = "../data/model2.crd"
    outputFileDir = "../results/"
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('inputFiles', metavar='N', type=str, nargs='*',
                    help='two input file paths to compare')
    parser.add_argument('range', type=int, help='range')
    parser.add_argument('-v', '--output', action='store_true', default=False,
                    dest='v',
                    help='set verbose to true')
    parser.add_argument('-d', '--dir', help='output directory')
    args = parser.parse_args()
    if len(args.inputFiles) > 0:
        inputFilePath1 = args.inputFiles[0]
    if len(args.inputFiles) > 1:
        inputFilePath2 = args.inputFiles[1]
    if args.dir:
        outputFileDir = args.dir
    if args.range:
        rangeN = args.range
    # print options for user confirmation and debugging
    outputFileName = "proteinResidueScoreCompare" + str(rangeN) + ".csv"
    outputFilePath = os.path.join(outputFileDir, outputFileName)
    try:
        os.makedirs(outputFileDir)
    except OSError:
        if args.v:
            print ("Creation of the directory \"%s\" failed. Directory may already exist!" % outputFileDir)
    else:
        if args.v:
            print ("Successfully created the directory \"%s\"" % outputFileDir)
    print("Input File 1:", inputFilePath1)
    print("Input File 2:", inputFilePath2)
    print("Output Directory:", outputFileDir)
    print("Output File:", outputFilePath)
    # process protein #1
    runtimeProfile1 = EnergyScoreMethods.RuntimeProfile()
    atomMap1 = EnergyScoreMethods.atomMapFromCRD(inputFilePath1, runtimeProfile1)
    if args.v:
        print("Protein #1 file processing time:",
          runtimeProfile1.getDurationMS(), "milliseconds")
    # process protein #2
    runtimeProfile2 = EnergyScoreMethods.RuntimeProfile()
    atomMap2 = EnergyScoreMethods.atomMapFromCRD(inputFilePath2, runtimeProfile2)
    if args.v:
        print("Protein #2 file processing time:",
          runtimeProfile2.getDurationMS(), "milliseconds")
    residueMap1 = EnergyScoreMethods.atomMapToResidueMap(atomMap1);
    residueMap2 = EnergyScoreMethods.atomMapToResidueMap(atomMap2);
    differenceMap = {}
    n = len(residueMap1) -rangeN
    print("Running... this make take a minute.")
    for i in range(0, n):
        if args.v:
            print("Beginning Iteration", i, "to", i+rangeN)
        # find submap
        subMap1 = EnergyScoreMethods.residueSubMap(residueMap1, i, i+rangeN)
        subMap2 = EnergyScoreMethods.residueSubMap(residueMap2, i, i+rangeN)
        #print(subMap1)
        #print(subMap2)
        # calculate protein #1
        runtimeProfile3 = EnergyScoreMethods.RuntimeProfile()
        energyScore1 = EnergyScoreMethods.calculateEnergyScore(EnergyScoreMethods.residueMapToAtomMap(subMap1), runtimeProfile3)
        if args.v:
            print("Protein #1 calculate internal energy processing time:",
              runtimeProfile3.getDurationMS(), "milliseconds")
        if args.v:
            print("The internal energy of the protein #1 is",
              int(round(energyScore1)), "kcal/mol")
        # calculate protein #2
        runtimeProfile4 = EnergyScoreMethods.RuntimeProfile()
        energyScore2 = EnergyScoreMethods.calculateEnergyScore(EnergyScoreMethods.residueMapToAtomMap(subMap2), runtimeProfile4)
        if args.v:
            print("Protein #2 calculate internal energy processing time:",
              runtimeProfile4.getDurationMS(), "milliseconds")
        if args.v:
            print("The internal energy of the protein #2 is",
              int(round(energyScore2)), "kcal/mol")
        # difference map data
        differenceMap[i] = {}
        differenceMap[i]["residueIndexStart"] = i
        differenceMap[i]["residueIndexEnd"] = i+rangeN
        differenceMap[i]["protein1"] = energyScore1
        differenceMap[i]["protein2"] = energyScore2
        differenceMap[i]["difference"] = energyScore1-energyScore2
    # write to file
    n = len(differenceMap)
    with open(outputFilePath, "w") as outputFile:
        outputFile.write("Residue Index Start,Residue Index End,Protein #1 Energy Score,Protein #2 Energy Score,Energy Score Difference\n")
        for i in range(0, n):
            if i in differenceMap:
                outputFile.write(str(differenceMap[i]["residueIndexStart"]) + ",")
                outputFile.write(str(differenceMap[i]["residueIndexEnd"]) + ",")
                outputFile.write(str(int(round(differenceMap[i]["protein1"]))) + ",")
                outputFile.write(str(int(round(differenceMap[i]["protein2"]))) + ",")
                outputFile.write(str(int(round(differenceMap[i]["difference"]))) + "\n")
    print("Output written to", outputFilePath)

if __name__ == "__main__":
    residueScoreCompare()
