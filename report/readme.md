# Office Session 2020-02-27 at 2:00 PM

## Where did Dr. Koehl get the Lennard-Jones potential and Partial Charge parameters?
* Using OPLS Force Field, a competitor to AMBER Force Field.
* Solvation data is arbitrary, but easy to calculate. 
	* Discussion section: What is the assumptions for this method and why is it not good. What are better methods to calculate solvation energy. If the solvation energy is arbitrary then is the answer a real energy or just a score?

## What should be in the method section?
* Assumptions of your program
	* How is the input data formated. Be specific. Dr. Koehl will test your program with "dirty" data if input assumptions not specified.
* Flow chart if possible. Two main areas or less areas of substantial work.

## Result Section
* Compute time vs. Protein Length. Verify the algorithm is O(n^2) complexity. Analyze the graph.
* Why are the two proteins "energies" or scores magnitudes of difference apart? Is there a local area where the energy of one deviates from the other? Possible test would be to find substrings of the amino acids on the protein to see which local areas of the proteins differ the most.

## Are our calculations correct?
* Dr. Koehl said our calculated scores seemed about right.

## Misc
* Dr. Koehl says a picture is worth a thousand words
