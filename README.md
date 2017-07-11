# plotReadLengths

Python Script to create a histogram of the sequences lengths in a Fasta file 

## Motivation

Can be used to get the distribution of Pacbio Reads

## Tests

python plotReadLengths.py -g <genomeSize> -f <sequences.fasta> -o <outputDir> -b <binSize in percentage of the longest read>

![alt text](https://raw.githubusercontent.com/MCorentin/plotReadLengths/master/image.png)

Because the bin size is in % of the longest read: 
- if you choose 20%, there will be 5 bins
- if you choose 1% there will be 100 bins
- etc...
