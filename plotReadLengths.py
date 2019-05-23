#!/bin/python

import numpy as np
from matplotlib import pyplot as plt
import getopt
import sys
from subprocess import call, Popen, PIPE
import os

# Variable initialisation
outputDir = './'
fasta = None
lengthsFile = None
expectedGenomeSize = None
percent = None
verbose = 0

#===================================
#		Functions
#===================================
def usage():
	"""
	Print the usage and help 
	"""
	print("\npython plotReadLengths.py -f [sequences.fasta] -b [binGranularity] -g [estimatedGenomeSize] -o [outputDirectory] -v")
	print("")
	print("Input:")
	print("	-f: an input fasta file")
	print("	-l: a length file, which is created by this script. Can be used to run the script again, more quickly.")
	print('		/!\ If both -f and -l are specified, -l will have the priority.')
	print("	-g: the estimated genome size, will be used to compute the coverage. Optional")
	print("	-b: bin size based on the percentage of the longest sequence. Default: 5")
	print("Output:")
	print("	-o: the output directory, should already exist. Default to " + outputDir)
	print("Other:")
	print("	-v: verbose mode.")
	print("	-h: print the help and exit")


def get_lengths_from_fasta(fasta, verbose):
	"""
	Use awk to get the sequence lengths in a fasta file
	"""
	cmd = ["awk", '/^>/ {if (seqlen){print seqlen};seqlen=0;next; } { seqlen += length($0)}END{print seqlen}', fasta]
	if(verbose == 1):
		print("Calculating the sequences length for the fasta...")
		print(" ".join(cmd))
	awk_process = Popen(cmd, shell = False, stdout=PIPE)
	lengths = awk_process.communicate()[0]
	# Popen is outputing bytes, so we use "decode()" to change it to string
	lengths_decoded = lengths.decode()
	return(lengths_decoded)


def get_coverage(readLengths, expectedGenomeSize, verbose):
	"""
	Return the coverage from readLengths and expectedGenomeSize
	"""
	cov = int(sum(readLengths) / expectedGenomeSize)
	if(verbose == 1):
		print("Coverage " + str(cov) + " X")
	return(cov)


def get_N50(readLengths):
	"""
	Compute and return the N50 from lengths
	"""
	sorted_length = sorted(readLengths, reverse = True)
	total_len = sum(readLengths)

	sum_len = 0
	index = 0
	while(sum_len <= total_len/2):
		sum_len = sum_len + sorted_length[index]
		index = index + 1
	# Index - 1 to get the sequence that actually managed to achieve N50
	return(sorted_length[index-1])


def create_plot_lengths(bins, N50, expectedGenomeSize, readLengths, outputName, verbose):
	"""
	Create the plot object
	"""
	# Plotting options 
	plt.figure(figsize=(15,8), facecolor='white')

	plt.xlim([0, max(readLengths)+1])
	plt.xlabel('Read Length')
	plt.ylabel('Number of Reads')

	plt.hist(readLengths, bins=bins, alpha=0.5, facecolor='green')

	#  Get coverage as a string to print in the graph's title
	if(expectedGenomeSize != None):
		cov = get_coverage(readLengths, expectedGenomeSize, verbose)
		plt.title(" Coverage: " + str(cov) + "x (for genome size of " + str(expectedGenomeSize) + " bp)", fontsize = 12)
		
	plt.suptitle("Read Length Distribution for " + outputName + " (N50 = " + str(N50) + " bp)", fontsize = 14)

	return(plt)




#===================================
#	 			Main
#===================================
# Getting the parameters from getopt
try:
	opts, args = getopt.getopt(sys.argv[1:], "ho:f:l:g:b:v", ["help", "output=", "fasta=", "lengthsFile=", "genomeEstimate=", "binGranularity=", "verbose="])
except getopt.GetoptError as err:
	print(str(err))  # will print "option -a not recognized"
	usage()
	sys.exit(2)

for o, a in opts:
	if o in ("-f", "--fasta"):
		fasta = a
	elif o in ("-g", "--genomeSize"):
		expectedGenomeSize = int(a)
	elif o in ("-b", "--binGranularity"):
		percent = float(a)
	elif o in ("-o", "--output"):
		outputDir = a
	elif o in ("-l", "--output"):
		lengthsFile = a
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-v", "--verbose"):
		verbose = 1
	else:
		assert False, "unhandled option"


if(fasta == None and lengthsFile == None):
	print("Please provide either a fasta file as input (option -f / --fasta) or a lengthsFile (option -l / --lengthsFile)\n")
	usage()
	sys.exit()

if(fasta != None and not(os.path.isfile(fasta))):
	print(fasta + " is not detected as a file. (option -f / --fasta)")
	sys.exit()

if(lengthsFile != None and not(os.path.isfile(lengthsFile))):
	print(lengthsFile + " is not detected as a file. (option -l / --lengthsFile)")
	sys.exit()

if(not(os.path.isdir(outputDir))):
	print(outputDir + " is not a folder. (option -o / --output)")
	sys.exit()

if(percent == None):
	percent = 5
	if(verbose == 1):
		print("Defaulting bin size to " + str(percent) + "% of Longest Read.\n")
else:
	if(percent <= 0 or percent > 100):
		print("-b / --binGranularity should be > 0 and <= 100")
		usage()
		sys.exit()

# If there is no file with lengths available, we use the fasta (slower)
if lengthsFile == None:
	lengths_decoded = get_lengths_from_fasta(fasta, verbose)

	# Create the lengths file for potential future runs
	filename = outputDir + "/" + os.path.basename(fasta) + "_lengthsFile.txt"
	if(verbose == 1):
		print("Writing lengths to: " + filename + "...")
	with open(filename, "w") as len_file_writer:
		len_file_writer.write(lengths_decoded)
		if(verbose == 1):
			print("Done\n")

	outputName = os.path.basename(fasta)

# If no fasta then we use the lengths file
else:
	with open(lengthsFile, 'r') as length_file_reader:
    		lengths_decoded = length_file_reader.read()

	outputName = os.path.basename(lengthsFile)


readLengths = lengths_decoded.split("\n")
# Filter the empty ones if there are any
readLengths = filter(None, readLengths)
# Transform the lengths from string to int
# in python3 map return a generator, so we convert to "list" to avoid issues with matplotlib
readLengths = list(map(int, readLengths))

maxRead = max(readLengths)
N50 = get_N50(readLengths)
if(verbose == 1):
	print("Longest Read = " + str(maxRead))
	print("N50 = " + str(N50))
# Bin size is percent% of Longest Read:
# Allows for the same bin size for each distributions
p = percent / (100 * 1.0)
if(verbose == 1):
	print("Bin granularity : " + str(percent) + "% of longest read")
if(p*maxRead == 0):
	binSize = 1000
else:
	binSize = int(p * maxRead)

# Setting the bin size
if(verbose == 1):
	print("Bin size = " + str(binSize))
bins = np.arange(0, maxRead+1, binSize)

plt = create_plot_lengths(bins, N50, expectedGenomeSize, readLengths, outputName, verbose)

# Saving file to pdf
GraphFile = outputDir + "/" + outputName + "_readLengths.pdf"
plt.savefig(GraphFile, bbox_inches='tight')

print("Graph saved to " + GraphFile)

plt.show()
