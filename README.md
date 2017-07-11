# plotReadLengths

Python Script to create a histogram of the sequences lengths in a Fasta file 

## Motivation

Can be used to get the distribution of Pacbio Reads

## Tests

To run with a fasta file:
  python plotReadLengths.py -g <genomeSize> -f <sequences.fasta> -o <outputDir> -b <binSize in percentage of the longest read>

After the first run, a file called <sequence.fasta>\_lengthsFile.txt is created so you can run it again more quickly if you want to try a different bin size:
  python plotReadLengths.py -g <genomeSize> -l <sequences.fasta_lengthsFile.txt> -o <outputDir> -b <binSize in percentage of the longest read>

![alt text](https://raw.githubusercontent.com/MCorentin/plotReadLengths/master/image.png)

Because the bin size is in % of the longest read: 
- if you choose 20%, there will be 5 bins
- if you choose 1% there will be 100 bins
- etc...
