/**
 * Author: Branden Lee
 * Date: 2020-01-24 to 2020-03-06
 * Github: https://github.com/GoodProtein/ProScore
 * 
 * PLAGIARISM NOTICE
 * This project was created for ECS 129 course at UC Davis
 * and is publically hosted in a github repository. Other students
 * may find this repository and attempt to copy all or portions of this project.
 */

#include <algorithm>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>

/**
 * @brief atomic information
 */
class Atom {
public:
  Atom() {}
  ~Atom() {}
  int num;
  double x, y, z, R, Epsilon, Sigma, Charge, ASP;
  std::string Atm_name, Res_name, Res_num;
  std::unordered_map<int, bool> exclude;
};

/**
 * @brief A utility class passed along for function profiling for
 * process time and operations performed
 */
class RuntimeProfile {
public:
  std::chrono::duration<double, std::milli> processDuration;
  void setDuration(std::chrono::steady_clock::time_point start,
                   std::chrono::steady_clock::time_point stop) {
    processDuration = stop - start;
    processDuration = std::chrono::duration<double, std::milli>(
        std::round(processDuration.count()));
  }
  int getDurationMS() { return (int)processDuration.count(); }
};

typedef std::shared_ptr<std::unordered_map<int, std::shared_ptr<Atom>>>
    AtomMapT;

// Opens the .crd file and stores atom data into a python dictionary
AtomMapT atomMapFromCRD(std::string filePath, RuntimeProfile &runtimeProfile);
// calculates the internal energy of a protein
// atomMap = a map of atoms
double calculateInternalEnergy(AtomMapT atomMap,
                               RuntimeProfile &runtimeProfile);
void toFile(AtomMapT atomMap, std::string outputPath);

// compare two proteins
int main() {
  std::string filePath1 = "../data/model1.crd";
  std::string filePath2 = "../data/model2.crd";
  // process protein #1
  RuntimeProfile runtimeProfile1;
  auto atomMap1 = atomMapFromCRD(filePath1, runtimeProfile1);
  std::cout << "Protein #1 file processing time: "
            << runtimeProfile1.getDurationMS() << " milliseconds\n";
  toFile(atomMap1, "protein1.txt");
  // process protein #2
  RuntimeProfile runtimeProfile2;
  auto atomMap2 = atomMapFromCRD(filePath2, runtimeProfile2);
  std::cout << "Protein #2 file processing time: "
            << runtimeProfile2.getDurationMS() << " milliseconds\n";
  toFile(atomMap2, "protein2.txt");
  // calculate protein #1
  RuntimeProfile runtimeProfile3;
  double internalEnergy1 = calculateInternalEnergy(atomMap1, runtimeProfile3);
  std::cout << "Protein #1 calculate internal energy processing time: "
            << runtimeProfile3.getDurationMS() << " milliseconds\n";
  std::cout << "The internal energy of the protein #1 is "
            << (long long int)(std::round(internalEnergy1)) << " kcal/mol\n";
  // calculate protein #2
  RuntimeProfile runtimeProfile4;
  double internalEnergy2 = calculateInternalEnergy(atomMap2, runtimeProfile4);
  std::cout << "Protein #2 calculate internal energy processing time: "
            << runtimeProfile4.getDurationMS() << " milliseconds\n";
  std::cout << "The internal energy of the protein #2 is "
            << (long long int)(std::round(internalEnergy2)) << " kcal/mol\n";
  // Protein comparison
  if (internalEnergy1 < internalEnergy2) {
    printf("The internal energy of the protein #1 is less, so it is more "
           "likely to occur\n");
  } else {
    printf("The internal energy of the protein #2 is less, so it is more "
           "likely to occur\n");
    return 0;
  }
}

AtomMapT atomMapFromCRD(std::string filePath, RuntimeProfile &runtimeProfile) {
  auto processStart = std::chrono::steady_clock::now();
  auto atomMap =
      std::make_shared<std::unordered_map<int, std::shared_ptr<Atom>>>();
  atomMap->reserve(5000);
  std::fstream fp;
  fp.open(filePath, std::ios_base::in);
  if (fp.is_open()) {
    std::string line, word;
    std::getline(fp, line);
    int i = 0;
    int atomNumber = std::stoi(line);
    bool lastAtomFound = false;
    // iterate through each atom
    while ((i < atomNumber) && !lastAtomFound) {
      // Ignore commented out lines
      fp >> word;
      if (word.substr(0, 1) == "#") {
        // get rest of line
        std::getline(fp, line);
        continue;
      }
      // Let's map each column in the file to a variable
      std::shared_ptr<Atom> atom = std::make_shared<Atom>();
      atom->num = std::stoi(word);
      fp >> word;
      atom->x = std::stof(word); // Angstroms
      fp >> word;
      atom->y = std::stof(word); // Angstroms
      fp >> word;
      atom->z = std::stof(word); // Angstroms
      // Van der Waals radius in Angstroms
      fp >> word;
      atom->R = std::stof(word);
      fp >> word;
      atom->Epsilon = std::stof(word);
      fp >> word;
      atom->Sigma = std::stof(word);
      fp >> word;
      atom->Charge = std::stof(word);
      fp >> word;
      atom->ASP = std::stof(word);
      fp >> atom->Atm_name;
      fp >> atom->Res_name;
      fp >> atom->Res_num;
      atomMap->insert({atom->num, atom});
      // printf("%d %f %f %f\n", atom->num, atom->x, atom->y, atom->z);
      if (atom->num >= atomNumber) {
        // Last atom found prematurely so we will stop looking for atoms
        lastAtomFound = true;
      }
      i++;
    }

    // Now we get the exlude list

    while (std::getline(fp, line)) {
      // Ignore commented out lines
      fp >> word;
      if (word.substr(0, 1) == "#") {
        std::getline(fp, line);
        continue;
      }
      // Let's map each column in the file to a variable
      int atomNumber = std::stoi(word);
      fp >> word;
      int exludeNumber = std::stoi(word);
      // iterate through the exclude list
      for (int j = 0; j < exludeNumber; j++) {
        fp >> word;
        atomMap->at(atomNumber)->exclude.insert({std::stoi(word), true});
        // printf("%d %d %d %d\n", i, j, exludeNumber, std::stoi(word));
      }
    }
  }
  auto processEnd = std::chrono::steady_clock::now();
  runtimeProfile.setDuration(processStart, processEnd);
  return atomMap;
}

double calculateInternalEnergy(AtomMapT atomMap,
                               RuntimeProfile &runtimeProfile) {
  auto processStart = std::chrono::steady_clock::now();
  /* Brad:
   * I'm just implementing the equation that was in the PDF here.
   * I'm not exactly sure of the physical meaning though.
   */
  double internalEnergy = 0;
  // radius of a water molecule in angstroms
  double radius_h2o = 1.4;
  double coulomb_constant = 83;
  // Van der waal + Electrostatic Force
  // Go through each combination of two atoms once, order doesn't matter
  std::unordered_map<int, bool> atomExists;
  int n = atomMap->size();
  for (int i = 0; i < n - 1; i++) {
    auto it_i = atomMap->find(i);
    if (it_i == atomMap->end()) {
      atomExists.insert({i, false});
    } else {
      atomExists.insert({i, true});
      auto &atom_i = it_i->second;
      // printf("%d %f %f %f\n", atom_i->num, atom_i->x, atom_i->y, atom_i->z);
      for (int j = i + 1; j < n; j++) {
        auto it_j = atomMap->find(j);
        if (it_j != atomMap->end()) {
          auto &atom_j = it_j->second;
          // only non-bonded atoms are calculated
          auto it1 = atom_i->exclude.find(j);
          if (it1 == atom_i->exclude.end()) {
            double epiilon_ij = std::sqrt(atom_i->Epsilon * atom_j->Epsilon);
            double sigma_ij = 0.5 * (atom_i->Sigma + atom_j->Sigma);
            double r_ij = std::sqrt(std::pow(atom_i->x - atom_j->x, 2) +
                                    std::pow(atom_i->y - atom_j->y, 2) +
                                    std::pow(atom_i->z - atom_j->z, 2));
            double van_der_waal_energy =
                epiilon_ij * (std::pow(sigma_ij / r_ij, 12) -
                              2 * std::pow(sigma_ij / r_ij, 6));
            double electrostatic_force =
                coulomb_constant * atom_i->Charge * atom_j->Charge / r_ij;
            // energy units are kcal/mol
            internalEnergy += van_der_waal_energy;
            internalEnergy += electrostatic_force;
          }
        }
      }
    }
  }

  // Solvation Energy
  for (int i = 0; i < n - 1; i++) {
    if (atomExists.at(i)) {
      auto &atom_i = atomMap->at(i);
      double ASA = 0.2 * 4 * 3.1415 * std::pow(atom_i->R + radius_h2o, 2);
      internalEnergy += atom_i->ASP * ASA;
    }
  }
  auto processEnd = std::chrono::steady_clock::now();
  runtimeProfile.setDuration(processStart, processEnd);
  return internalEnergy;
}

void toFile(AtomMapT atomMap, std::string outputPath) {
  int n = atomMap->size() + 1;
  std::fstream outputFile;
  outputFile.open(outputPath, std::ios_base::out);
  if (outputFile.is_open()) {
    for (int i = 0; i < n; i++) {
      auto it_i = atomMap->find(i);
      if (it_i != atomMap->end()) {
        outputFile << atomMap->at(i)->num << " ";
        outputFile << std::fixed << std::setprecision(4) << atomMap->at(i)->x
                   << " ";
        outputFile << atomMap->at(i)->y << " ";
        outputFile << atomMap->at(i)->z << " ";
        outputFile << atomMap->at(i)->R << " ";
        outputFile << atomMap->at(i)->Epsilon << " ";
        outputFile << atomMap->at(i)->Sigma << " ";
        outputFile << atomMap->at(i)->Charge << " ";
        outputFile << atomMap->at(i)->ASP << " ";
        outputFile << atomMap->at(i)->Atm_name << " ";
        outputFile << atomMap->at(i)->Res_name << " ";
        outputFile << atomMap->at(i)->Res_num << " ";
        outputFile << std::endl;
        for (int j = 0; j < n; j++) {
          auto it_j = atomMap->at(i)->exclude.find(j);
          if (it_j != atomMap->at(i)->exclude.end()) {
            outputFile << j << " ";
          }
        }
        outputFile << std::endl;
      }
    }
  }
}
