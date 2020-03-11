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
@brief methods for calculating energy score
"""

import math
import time
import random


"""
@name Atom
@brief atomic information
PYTHON: For some reason, changing an Atom from a dictionary to an object made the code
slightly slower.
__slots__ slightly sped up the code, but dictionary method still faster. 
representing Atom as an onject will still be done for semantics 
and consistency with C++ implementation.
"""
class Atom:
    __slots__ = ("index", "num", "x", "y", "z", "R", "Epsilon", "Sigma",
                 "Charge", "ASP", "atomName", "resName", "resNum", "exclude")

    def __init__(self):
        self.index = self.num = self.resNum = int(0)
        self.x = self.y = self.z = self.R = self.Epsilon = self.Sigma = self.Charge = self.ASP = float(
            0)
        self.atomName = self.resName = ""
        self.exclude = []

"""
@name RuntimeProfile
@brief A utility class passed along for function profiling for 
process time and operations performed
"""
class RuntimeProfile:
    processDuration = False

    def setDuration(self, start, stop):
        self.processDuration = stop - start

    def getDurationMS(self):
        return int(round(self.processDuration * 1000))

'''
Opens the .crd file and stores atom data into a python dictionary
'''
def atomMapFromCRD(filePath, runtimeProfile):
    processStart = time.process_time()
    # Initialize a python dictionary, which is implemented as a hash table
    # internally
    atomMap = {}
    with open(filePath) as fp:
        line = fp.readline()
        i = 0
        atomNumberMax = int(line)
        line = fp.readline()
        lastAtomFound = False
        # iterate through each atom
        while ((i < atomNumberMax) and not lastAtomFound):
            # Ignore commented out lines
            if(line.strip()[:1] == "#"):
                line = fp.readline()
                continue
            # Let"s map each column in the file to a variable
            dataArray = line.split()
            atomNum = int(dataArray[0])
            atomMap[atomNum] = Atom()
            atomMap[atomNum].index = i
            atomMap[atomNum].num = int(dataArray[0])
            atomMap[atomNum].x = float(dataArray[1])  # Angstroms
            atomMap[atomNum].y = float(dataArray[2])  # Angstroms
            atomMap[atomNum].z = float(dataArray[3])  # Angstroms
            # Van der Waals radius in Angstroms
            atomMap[atomNum].R = float(dataArray[4])
            atomMap[atomNum].Epsilon = float(dataArray[5])
            atomMap[atomNum].Sigma = float(dataArray[6])
            atomMap[atomNum].Charge = float(dataArray[7])
            atomMap[atomNum].ASP = float(dataArray[8])
            atomMap[atomNum].atomName = dataArray[9]
            atomMap[atomNum].resName = dataArray[10]
            atomMap[atomNum].resNum = int(dataArray[11])
            atomMap[atomNum].exclude = []
            # print (atomMap[i]["#"], atomMap[i]["x"], atomMap[i]["y"],
            # atomMap[i]["z"])
            if(atomNum >= atomNumberMax):
                # Last atom found prematurely so we will stop looking for atoms
                lastAtomFound = True
            else:
                line = fp.readline()
            i += 1

        # Now we get the exlude list
        line = fp.readline()
        while (line):
            # Ignore commented out lines
            if(line.strip()[:1] == "#"):
                line = fp.readline()
                continue
            # Let"s map each column in the file to a variable
            dataArray = line.split()
            i = int(dataArray[0])
            exludeNumber = int(dataArray[1])
            # iterate through the exclude list
            for j in range(0, exludeNumber):
                atomMap[i].exclude.append(int(dataArray[j + 2]))
                # print (i, j, exludeNumber, int(dataArray[j+2]))
            line = fp.readline()
    processEnd = time.process_time()
    runtimeProfile.setDuration(processStart, processEnd)
    return atomMap


def atomMapToCSV(atomMap, outputPath):
    n = len(atomMap) + 2
    with open(outputPath, "w") as outputFile:
        outputFile.write("i,X,Y,Z,R,Epsilon,Sigma,Charge,ASP,Atm name,Res name,Res #,Exclude List\n")
        for i in range(0, n):
            if i in atomMap:
                outputFile.write(str(atomMap[i].num) + ",")
                outputFile.write("{:.4f},".format(atomMap[i].x))
                outputFile.write("{:.4f},".format(atomMap[i].y))
                outputFile.write("{:.4f},".format(atomMap[i].z))
                outputFile.write("{:.4f},".format(atomMap[i].R))
                outputFile.write("{:.4f},".format(atomMap[i].Epsilon))
                outputFile.write("{:.4f},".format(atomMap[i].Sigma))
                outputFile.write("{:.4f},".format(atomMap[i].Charge))
                outputFile.write("{:.4f},".format(atomMap[i].ASP))
                outputFile.write(atomMap[i].atomName + ",")
                outputFile.write(atomMap[i].resName + ",")
                outputFile.write(str(atomMap[i].resNum) + ",")
                for atomNum in atomMap[i].exclude:
                    outputFile.write(str(atomNum) + " ")
                outputFile.write("\n")


'''
calculates the internal energy of a protein
atomMap = a map of atoms
'''
def calculateEnergyScore(atomMap, runtimeProfile):
    processStart = time.process_time()
    """ Brad:
    I"m just implementing the equation that was in the PDF here.
    I"m not exactly sure of the physical meaning though.
    """
    internalEnergy = 0
    # radius of a water molecule in angstroms
    radius_h2o = 1.4
    coulomb_constant = 83
    # Van der waal + Electrostatic Force
    # Go through each combination of two atoms once, order doesn"t matter
    n = len(atomMap) + 2
    for i in range(0, n - 1):
        if i in atomMap:
            for j in range(i + 1, n):
                # only non-bonded atoms are calculated
                if (j in atomMap and j not in atomMap[i].exclude):
                    epiilon_ij = math.sqrt(
                        atomMap[i].Epsilon * atomMap[j].Epsilon)
                    sigma_ij = 0.5 * (atomMap[i].Sigma + atomMap[j].Sigma)
                    r_ij = math.sqrt(math.pow(atomMap[i].x - atomMap[j].x, 2) + math.pow(
                        atomMap[i].y - atomMap[j].y, 2) + math.pow(atomMap[i].z - atomMap[j].z, 2))
                    van_der_waal_energy = epiilon_ij * \
                        (math.pow(sigma_ij / r_ij, 12) -
                         2 * math.pow(sigma_ij / r_ij, 6))
                    electrostatic_force = coulomb_constant * \
                        atomMap[i].Charge * atomMap[j].Charge / r_ij
                    # energy units are kcal/mol
                    internalEnergy += van_der_waal_energy
                    internalEnergy += electrostatic_force

    # Solvation Energy
    for i in range(0, n):
        if i in atomMap:
            ASA = 0.2 * 4 * 3.1415 * math.pow(atomMap[i].R + radius_h2o, 2)
            internalEnergy += atomMap[i].ASP * ASA
    processEnd = time.process_time()
    runtimeProfile.setDuration(processStart, processEnd)
    return internalEnergy

'''
@brief creates a sub-map of an atomMap from [startIndex, endIndex)
'''
def atomSubMap(atomMap, startIndex, endIndex):
    subMap = {}
    i=0
    for j in range(startIndex, endIndex):
        if j in atomMap:
            subMap[i] = atomMap[j]
        i+=1
    return subMap

'''
@brief creates a sub-map of an residueMap from [startIndex, endIndex)
'''
def residueSubMap(residueMap, startIndex, endIndex):
    subMap = {}
    i=0
    for j in range(startIndex, endIndex):
        if j in residueMap:
            subMap[i] = residueMap[j]
        i+=1
    return subMap

'''
@assumptions Uses integer index in order 0 ... N
@design Why traverse the map by iterating 0 ... N instead of iterating actual elements?
Because iterating by integer is computationally faster assuming only a few skips
'''
def atomMapToResidueMap(atomMap):
    residueMap = {}
    n = len(atomMap)
    for i in range(0, n):
        if i in atomMap:
            if atomMap[i].resNum not in residueMap:
                residueMap[atomMap[i].resNum] = []
            residueMap[atomMap[i].resNum].append(atomMap[i])
    return residueMap

'''
@assumptions Uses integer index in order 0 ... N
@design Why traverse the map by iterating 0 ... N instead of iterating actual elements?
Because iterating by integer is computationally faster assuming only a few skips
'''
def residueMapToAtomMap(residueMap):
    atomMap = {}
    index = 0
    n = len(residueMap) + 2 # The +2 is for tolerating numbering skips
    for i in range(0, n):
        if i in residueMap:
            n2 = len(residueMap[i])
            for j in range(0, n2):
                atomMap[index] = residueMap[i][j];
                index += 1
    return atomMap

def randomRange(min, max, precision):
    randFloat = min + (random.random() * (max - min))
    return round(randFloat,precision)


'''
@brief creates an amino acid
@param x0,y0,z0 coordinates the last amino acid was centered around
@param x1,y1,z1 new coordinates the amino acid is centered around
'''
def createRandomLysine(x0,y0,z0,x1,y1,z1):
    # the residue moves away and its atoms are randomly centered around it
    x1 = x0 + randomRange(-3, 3, 3)
    y1 = y0 + randomRange(-3, 3, 3)
    z1 = z0 + randomRange(-3, 3, 3)
    # lysine data
    atomNames = ["N","HN","CA","CB","C","O","CG","CD","CE","NZ","HZ1","HZ2","HZ3"]
    excludeLists = [[145,146,147,148],[146],[147,148,149,150,157],[148,150,151],[149,157,158,159],[157],[151,152],[152,153],[153,154,155,156],[154,155,156],[155,156],[156],[]]
    atomMap = {}
    n = len(atomNames)
    for atomNum in range(0,n):
        atomMap[atomNum] = Atom()
        atomMap[atomNum].index = atomNum
        atomMap[atomNum].num = atomNum+1
        atomMap[atomNum].x = x1 + randomRange(-3, 3, 3)
        atomMap[atomNum].y = y1 + randomRange(-3, 3, 3)
        atomMap[atomNum].z = z1 + randomRange(-3, 3, 3)
        atomMap[atomNum].R = randomRange(1, 2, 3)
        atomMap[atomNum].Epsilon = randomRange(0.1, 0.3, 3)
        atomMap[atomNum].Sigma = randomRange(0, 4, 3)
        atomMap[atomNum].Charge = randomRange(-0.7, 0.7, 3)
        atomMap[atomNum].ASP = randomRange(-0.035, 0.035, 3)
        atomMap[atomNum].atomName = atomNames[atomNum]
        atomMap[atomNum].resName = "LYS"
        atomMap[atomNum].resNum = 0
        atomMap[atomNum].exclude = excludeLists[atomNum]
    return atomMap

'''
@brief push lysine to end
'''
def pushRandomLysine(atomMap, x0,y0,z0,x1,y1,z1):
    lysAtomMap = createRandomLysine(x0,y0,z0,x1,y1,z1)
    n = len(lysAtomMap)
    n1 = len(atomMap)
    for i in range(0,n):
        atomMap[n1] = lysAtomMap[i]
        n1+=1

'''
@brief random chain
'''
def createRandomProteinChain(n):
    atomMap = {}
    x0 = y0 = z0 = x1 = y1 = z1 = 0
    for i in range(0,n):
        pushRandomLysine(atomMap,x0,y0,z0,x1,y1,z1)
        x0 = x1
        y0 = y1
        z0 = z1
    return atomMap