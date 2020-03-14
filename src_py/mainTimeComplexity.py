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
@brief Compute time complexity.
'''

import argparse, sys # getopt, exit
import os # makedirs
import math
import time
import EnergyScoreMethods

def timeComplexity():
    # default options
    rangeN = 100
    outputFileDir = "../results/"
    # Parse Arguments
    parser = argparse.ArgumentParser(description='Compute time complexity.')
    parser.add_argument('range', type=int, help='range')
    parser.add_argument('-v', '--output', action='store_true', default=False,
                    dest='v',
                    help='set verbose to true')
    parser.add_argument('-d', '--dir', help='output directory')
    args = parser.parse_args()
    if args.dir:
        outputFileDir = args.dir
    if args.range:
        rangeN = args.range
    # print options for user confirmation and debugging
    outputFileName = "algorithmTimeComplexity" + str(rangeN) + ".csv"
    outputFilePath = os.path.join(outputFileDir, outputFileName)
    try:
        os.makedirs(outputFileDir)
    except OSError:
        if args.v:
            print ("Creation of the directory \"%s\" failed. Directory may already exist!" % outputFileDir)
    else:
        if args.v:
            print ("Successfully created the directory \"%s\"" % outputFileDir)
    print("Output Directory:", outputFileDir)
    print("Output File:", outputFilePath)
    print("Running... this make take a minute.")
    # begin
    resultMap = {}
    for i in range(1, rangeN+1):
        atomMap = EnergyScoreMethods.createRandomProteinChain(i)
        runtimeProfile = EnergyScoreMethods.RuntimeProfile()
        energyScore = EnergyScoreMethods.calculateEnergyScore(atomMap, runtimeProfile)
        resultMap[i] = {}
        resultMap[i]["length"] = i
        resultMap[i]["duration"] = runtimeProfile.getDurationMS()
        if args.v:
            print("computed chain", i, "at", int(round(energyScore)),"in",runtimeProfile.getDurationMS(),"milliseconds")

    # write to file
    n = len(resultMap)+1
    with open(outputFilePath, "w") as outputFile:
        outputFile.write("Protein Chain Length,Run Duration (milliseconds)\n")
        for i in range(1, n):
            outputFile.write(str(resultMap[i]["length"]) + ",")
            outputFile.write(str(resultMap[i]["duration"]) + "\n")
    print("Output written to", outputFilePath)

if __name__ == "__main__":
    timeComplexity()
