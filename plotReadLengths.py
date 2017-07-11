#!/bin/python

import numpy as np
from matplotlib import pyplot as plt
import getopt
import sys
from subprocess import call, Popen, PIPE
import os

# Variable initialisation
outputDir = None
fastq = None
lengthsFile = None
expectedGenomeSize = None
percent = None

def usage():
	print("-h for help\n\nInput:\n\t-g for estimated genome size\n\t-f for fasta\n\t-l a file with the lengths of the reads (can be created from this script with a fasta)\n\t-b size of the bins (in % of total length)\n/!\ if both -f and -l are given -l will have the priority\n\noutput:\n\t-o for output directory\n")

try:
	opts, args = getopt.getopt(sys.argv[1:], "ho:f:l:g:b:", ["help", "output=", "fasta=", "lengthsFile=", "genomeEstimate=", "binSize="])
except getopt.GetoptError as err:
	print str(err)  # will print "option -a not recognized"
	usage()
	sys.exit(2)
    

for o, a in opts:
	if o in ("-f", "--fasta"):
		fastq = a
	elif o in ("-g", "--genomeSize"):
		expectedGenomeSize = int(a)
	elif o in ("-b", "--binSize"):
		percent = int(a)
	elif o in ("-o", "--output"):
		outputDir = a
	elif o in ("-l", "--output"):
		lengthsFile = a
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	else:
		assert False, "unhandled option"


if(fastq == None and lengthsFile == None):
	usage()
   	print("Please provide either a fastq file as input (option -f / --fastq) or a lengthsFile (option -l / --lengthsFile)")
   	sys.exit()

if(fastq != None and not(os.path.isfile(fastq))):
	print(fastq + " is not detected as a file... abort")
	sys.exit()

if(lengthsFile != None and not(os.path.isfile(lengthsFile))):
	print(lengthsFile + " is not detected as a file... abort")
	sys.exit()

if(outputDir == None):
	usage()
	print("Please provide output directory (option -o / --output)")
	sys.exit()

if(expectedGenomeSize == None):
	usage()
	print("Please provide expected Genome Size (option -g / --genomeSize)")
	sys.exit()

if(percent == None):
	percent = 20
	print("defaulting bin size to " + str(percent) + "% of Longest Read")


# If there is no file with lengths available, we use the fastq (slower)
if lengthsFile == None:
	# Command to get reads length :
	# awk '/^>/ {if (seqlen){print seqlen};seqlen=0;next; } { seqlen += length($0)}END{print seqlen}' pacbio.fasta
	cmd = ["awk", '/^>/ {if (seqlen){print seqlen};seqlen=0;next; } { seqlen += length($0)}END{print seqlen}', fastq]
	print cmd
	lengths = Popen(cmd, stdout=PIPE).communicate()[0]
	
	# Create lengths file
	filename = os.path.basename(fastq) + "_lengthsFile.txt"
	print("Writing lengths to: " + filename + "...")
	file = open(filename, "w")
	file.write(lengths)
	file.close()
	print("Done")

	outputName = os.path.basename(fastq)

# the "with" command ensure that the file is closed, even when an error occurs
else:
	with open(lengthsFile, 'r') as content_file:
    		lengths = content_file.read()

	outputName = os.path.basename(lengthsFile)


# Read the lengths
readLengths = lengths.split("\n")
lengths = ""
# Filter the empty ones if there are any
readLengths = filter(None, readLengths)
# Transform the lengths from string to int
readLengths = map(int, readLengths)

print("Longest Read = " + str(max(readLengths)))

#  Get coverage as a string to print in the graph's title
cov = int(sum(readLengths) / expectedGenomeSize)
print("Coverage " + str(cov) + " X")


# Bin size is percent% of Longest Read:
# Allows for the same bin size for each distributions
p = percent / (100 * 1.0)
print("percent : " + str(p))
if(p*max(readLengths) == 0):
	binSize = 1000
else:
	binSize = p * max(readLengths)

# Setting the bin size
print("Bin size = " + str(binSize))
bins = np.arange(0, max(readLengths)+1, binSize)

# Plotting options 
plt.figure(figsize=(15,8), facecolor='white')

plt.xlim([0, max(readLengths)+1])
#plt.xticks(bins)
plt.xlabel('Read Length')
plt.ylabel('Number of Reads')

plt.hist(readLengths, bins=bins, alpha=0.5, facecolor='green')

plt.suptitle("Read Lengths Distribution (Coverage " + str(cov) + " X)", fontsize = 16)
plt.title(outputName, fontsize = 12)

# Saving file to pdf
GraphFile = outputDir + "/" + outputName + "_readLengths.pdf"
print("Saving graph into " + GraphFile + "...")
plt.savefig(GraphFile, bbox_inches='tight')
print("Done")

plt.show()
