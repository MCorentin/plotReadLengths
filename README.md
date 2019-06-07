# plotReadLengths

Python Script to create a histogram of the sequences length in a Fasta file.
The histogram will be saved as a file and also displayed on the screen.

## Motivation

Plot the distribution of the sequence length present in a fasta file. The main use cases are:
- To get the distribution of Pacbio reads.
- To get the distribution contig lengths in an assembly.

The N50 of the sequences is also calculated and added to the plot title.

If a genome size is given (-g / --genomeEstimate option), then the coverage is also estimated.

## Dependencies

plotReadLengths is supported on Linux.

You will need to have the following dependencies:

**Note**: The following python packages are already built-in from python2.7 and do not need to be installed:
```
getopt
sys
os 
```

- **Python v2 or v3**
- **The following python packages:** [numpy](http://www.numpy.org/ "Numpy Homepage"), [biopython](https://biopython.org/ "biopython Homepage"), [matplotlib.pyplot](https://matplotlib.org/ "Matplotlib Homepage"), getopt, sys, os.


## Usage

````
  python plotReadLengths.py -f [sequences.fasta] -b [binGranularity] -g [estimatedGenomeSize] -o [outputDirectory]
````

````
  Input:
          -f: the input fasta file
          -l: a length file, is created by this script. Can be used to run the script again more quickly.
                  /!\ If both -f and -l are specified, -l will have the priority.
          -g: the estimated genome size, will be used to compute the coverage. Optional
          -b: bin size based on the percentage of the longest sequence. Default: 5
  Output:
          -o: the output director. Default to ./
  Other:
          -v: verbose mode.
          -h: print the help and exit
````


The bin size (-b) is in % of the longest read, it means that: 
- if you choose 50%, there will be 2 bins
- if you choose 20%, there will be 5 bins
- if you choose 1% there will be 100 bins
- etc...

Example with -b 20

![alt text](https://raw.githubusercontent.com/MCorentin/plotReadLengths/master/image.png)

## Trying different bin sizes

After the first run, a file called <sequence.fasta>\_lengthsFile.txt is created. This file can be inputed to the script to avoid the computation of the sequences length.
```
  python plotReadLengths.py -g <genomeSize> -l <sequences.fasta_lengthsFile.txt> -o <outputDir> -b <binSize in percentage of the longest read>
```

## TO DO

 - Allow more than one fasta at a time
 - Add some plot personalization (color, size, format...)
 - Add support for fastq files