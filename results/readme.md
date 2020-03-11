# Energy Score Comparison Data
## What is this data?
The energy score comparison data is LOCAL calculations for the energy score of a protein. This is different than the GLOBAL calculations for the entire protein. The local calculations are calculated as the energy score of different subarray ranges. Subarrays are contiguous atoms or residues on the protein chain. 

## What are the flaws of this data?
The energy score comparison data only factors nearby atoms or residues in the subarray range arbitrarily defined. This ignores atoms and residues that are proximally close, but not in the subarray range. The advantages of a subarray approach to calculating the local energy score is being simple to implement. A proximity based approach would give a better local energy score, but is harder to implement.

## How do I use this data?
Using the `proteinResidueScoreCompare` as an example, it contains the header:
| Atom Index Start | Atom Index End | Protein #1 Energy Score | Protein #2 Energy Score | Energy Score Difference |
| :-- | :-- | :-- | :-- | :-- |
| # | # | # | # | # |

This is an explanation:
| Header | Explanation |
| :-- | :-- |
| Atom Index Start | The residue index where the local calculation begins |
| Atom Index End  | The residue index where the local calculation ends. This field might not be as interesting if calculations are to be representated as points rather than ranges/intervals. |
| Protein #1 Energy Score | The local energy score for protein #1 using the subarray of residues in the range/interval specified |
| Protein #2 Energy Score | same as above for protein #2 |
| Energy Score Difference | The local energy score difference between the two proteins' subarrays. calculated as (protein1 - protein2). This field might be more useful as an absolute value. |

### proteinAtomScoreCompare10.csv

Atom Subarray Range = 10

### proteinAtomScoreCompare50.csv

Atom Subarray Range = 50

### proteinAtomScoreCompare100.csv

Atom Subarray Range = 100
