\# Assignment 08



This folder contains my solution for the programming task about Count-Min Sketch.



The task is to estimate the number of occurrences of a character in a multiset using the Count-Min Sketch algorithm.



The input multiset is given as a string stored in a file.



input:



\* an input file with a string

\* number of hash functions r

\* table width w

\* hash parameter M

\* hash parameter N

\* character c



reports:



\* estimated number of occurrences of character c



\## Run



./program input.txt 3 5 3 11 A



This reads the string from `input.txt`, builds the Count-Min Sketch with `r = 3`, `w = 5`, `M = 3`, and `N = 11`, then reports the estimated count for character `A`.



Example input file:



ACCDBDBCBABAB



Example output:



3



