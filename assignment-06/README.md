\# Assignment 06



This folder contains my solution for the programming task about linear-space pair-wise sequence alignment.



The task is to compute a global alignment of two sequences using Hirschberg's algorithm.



The program uses linear space for the main alignment step and writes the final alignment to an output file in FASTA format.



input:



\* a FASTA file with two sequences

\* an output file name

\* a match score

\* a mismatch penalty

\* a gap penalty



reports:



\* alignment score printed to the console

\* aligned sequences written to the output file in FASTA format



\## Run



./program input.fa output.fa 5 -4 -5



This reads the two sequences from `input.fa`, computes the alignment with match score `5`, mismatch penalty `-4`, and gap penalty `-5`, then writes the alignment to `output.fa`.



Example output in console:



82



Example output file:



> 1

> ACCATGGCTGTCCGCCCGGCCGGCCGGAGACGAGAT

> 2

> ACCATCGCTGTCCGC--------CCGGAGACGAGGT



