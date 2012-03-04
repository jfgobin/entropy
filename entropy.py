#!/usr/bin/env python

# Import various libraries

import os,sys,getopt,math

# Variables

threshold=0.0
dirmode=0
filmode=0
objname=""


# Functions

# Prints the help page
def Usage(execname):
	print "Usage ",execname," -h | [-t Value] (-d Directory | -f Filename)"
	print "\n\n"
	print "-t <Value>       : (optional) specifies a minimal value for threshold."
	print "                   Entropies below threshold are not displayed. Ignored for a single file."
	print "-f <Filename>    : display the entropy of a single file"
	print "-d <Directory>   : recursively display the entropy of all"
	print "                   files starting at <Directory>\n\n"
	return

# Returns pr.log(pr) if pr>0, 0 otherwise
# where 0<=pr<1. There is no explicit test to check 
# that pr <= 1, but a negative number will just return 0

def prlogpr(pr):
	if pr > 0:	
		return pr*math.log(pr)
	return 0


# Compute the entropy of a given file

def ComputeFileEntropy(objname):
	entropy=0
	total=0.0;
	frequency=[]
	# Set each character's frequency to 0
	for i in range(256):
		frequency.append(0)
	FILE=open(objname,"rb")
	while FILE:
		# Read byte by byte and increase the correspoding
		# character's frequency
		byte=FILE.read(1)
		if len(byte)!=0:
			frequency[ord(byte)]=frequency[ord(byte)]+1.0;
			total=total+1.0
		else:
			break
	# If we have anything, we compute the entropy.
	# entropy=sum(i in I) -pr[i]*log(pr[i])
	if total>0.0:
		for i in range(256):
			entropy=entropy-prlogpr(frequency[i]/total)
	else:
		entropy=0
	return entropy


# Walkdir - if in dir mode, let's process each file
# The order is to descend the dir tree first and then print the files.
# The function is used recursively to walk down the tree

def WalkDir(objname,threshold):
	listofdir=[]
	listoffiles=[]
	listofentropy=[]
	# Get a list of the object in the current directory
	listofitem=os.listdir(objname)
	for item in listofitem:
		# Add the previous path to get a path relative to where the script was started
		absitem=os.path.join(objname,item)
		# If it is a file, let's add it to the list of files
		if os.path.isfile(absitem):
			listoffiles.append(absitem)
		else:
		# Otherwise, let's add this as a directory
			listofdir.append(absitem)
	# And let's go down in each subdir
	for item in listofdir:
		WalkDir(item,threshold)
	# If no more subdirectory, let's compute and print the entropy of each file
	for item in listoffiles:
		cur_entropy=ComputeFileEntropy(item)
		if cur_entropy >= threshold:
			print item, " : ", cur_entropy
	return

# Test whether a number in a string is a floating point number
# Returns True if so

def isfloat(str):
    try: float(str)
    except ValueError: return False
    return True

# Main 

def main(argv):
	if len(argv) < 2:
		Usage(argv[0])
		sys.exit(-1)
	try:
		opts,args= getopt.getopt(argv[1:], "ht:f:d:", ["help", "thresh=", "file=", "directory="])
	except:
		Usage(argv[0])
		sys.exit(-2)

	filmode=0
	dirmode=0

	if opts[0][0]=='-h':
		Usage(argv[0])
		sys.exit(0)
	if opts[0][0]=='-t':
		# A threshold value has been passed
		if isfloat(opts[0][1]):
		# Get the threshold and remove the argument
			threshold=float(opts[0][1])
			opts.pop(0)
		else:
		# Not a float ...
			print "Error: -t requires a floating point value"
			sys.exit(-1)
	if opts[0][0]=='-d':
		dirmode=1
		objname=opts[0][1]
	elif opts[0][0]=='-f':
		filmode=1
		objname=opts[0][1]
	print "\n\n"
	
	if filmode:
		entropy=ComputeFileEntropy(objname)
		print objname," : ",entropy
		sys.exit(0)
	elif dirmode:
		WalkDir(objname,threshold)
	
	return


# Go!

main(sys.argv)
	
