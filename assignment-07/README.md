\# Assignment 07



This folder contains my solution for the programming task about Wavefront Alignment.



The task is to compute the optimal alignment score between two strings using the Wavefront Alignment algorithm.



The program uses mismatch and gap penalties and reports the final alignment score and the last wavefront.



input:



\* an input file with two strings

\* a mismatch penalty x

\* a gap penalty g



reports:



\* alignment score

\* last wavefront



\## Run



./wfa input.txt 2 3



This reads the two strings from `input.txt`, computes the alignment with mismatch penalty `2` and gap penalty `3`, then prints the alignment score and the last wavefront.



Example input file:



AATGATC

AGTATC



Example output:



Alignment score: 5

Last wavefront:

\-1: 6

0: 4

1: 4



