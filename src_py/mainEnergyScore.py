"""
Author: Branden Lee
Date: 2020-01-24 to 2020-03-06
Github: https://github.com/GoodProtein/ProScore

PLAGIARISM NOTICE
This project was created for ECS 129 course at UC Davis
and is publically hosted in a github repository. Other students
may find this repository and attempt to copy all or portions of this project.
"""

import argparse, sys # getopt, exit
import os
import math
import time
import EnergyScoreMethods

def energyScoreTest():
	# default paths and names
    inputFilePath1 = "../data/model1.crd"
    inputFilePath2 = "../data/model2.crd"
    outputFileDir = "../results/"
    outputFileName1 = "protein1Atoms.csv"
    outputFileName2 = "protein2Atoms.csv"
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('inputFiles', metavar='N', type=str, nargs='*',
                    help='two input file paths to compare')
    parser.add_argument('-o', '--output', action='store_true', default=False,
                    dest='o',
                    help='set file outputs to true')
    parser.add_argument('-d', '--dir', help='output directory')
    args = parser.parse_args()
    if len(args.inputFiles) > 0:
    	inputFilePath1 = args.inputFiles[0]
    if len(args.inputFiles) > 1:
    	inputFilePath2 = args.inputFiles[1]
    if args.dir:
        outputFileDir = args.dir
    # print options for user confirmation and debugging
    outputFilePath1 = os.path.join(outputFileDir, outputFileName1)
    outputFilePath2 = os.path.join(outputFileDir, outputFileName2)
    if args.o:
        try:
            os.makedirs(outputFileDir)
        except OSError:
            print ("Creation of the directory \"%s\" failed. Directory may already exist!" % outputFileDir)
        else:
            print ("Successfully created the directory \"%s\"" % outputFileDir)
    print("Input File 1:", inputFilePath1)
    print("Input File 2:", inputFilePath2)
    print("Output Directory:", outputFileDir)
    # print("Output File 1:", outputFilePath1)
    # print("Output File 2:", outputFilePath2)
    # process protein #1
    runtimeProfile1 = EnergyScoreMethods.RuntimeProfile()
    atomMap1 = EnergyScoreMethods.atomMapFromCRD(inputFilePath1, runtimeProfile1)
    print("Protein #1 file processing time:",
          runtimeProfile1.getDurationMS(), "milliseconds")
    if args.o:
        EnergyScoreMethods.atomMapToCSV(atomMap1, outputFilePath1)
    # process protein #2
    runtimeProfile2 = EnergyScoreMethods.RuntimeProfile()
    atomMap2 = EnergyScoreMethods.atomMapFromCRD(inputFilePath2, runtimeProfile2)
    print("Protein #2 file processing time:",
          runtimeProfile2.getDurationMS(), "milliseconds")
    if args.o:
        EnergyScoreMethods.atomMapToCSV(atomMap2, outputFilePath2)
    # calculate protein #1
    runtimeProfile3 = EnergyScoreMethods.RuntimeProfile()
    energyScore1 = EnergyScoreMethods.calculateEnergyScore(atomMap1, runtimeProfile3)
    print("Protein #1 calculate internal energy processing time:",
          runtimeProfile3.getDurationMS(), "milliseconds")
    print("The internal energy of the protein #1 is",
          int(round(energyScore1)), "kcal/mol")
    # calculate protein #2
    runtimeProfile4 = EnergyScoreMethods.RuntimeProfile()
    energyScore2 = EnergyScoreMethods.calculateEnergyScore(atomMap2, runtimeProfile4)
    print("Protein #2 calculate internal energy processing time:",
          runtimeProfile4.getDurationMS(), "milliseconds")
    print("The internal energy of the protein #2 is",
          int(round(energyScore2)), "kcal/mol")
    # Protein comparison
    if(energyScore1 < energyScore2):
        print(
            "The energy score of the protein #1 is less, so it is more likely to occur")
    else:
        print(
            "The energy score of the protein #2 is less, so it is more likely to occur")

if __name__ == "__main__":
    energyScoreTest()
