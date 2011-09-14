# Import various libraries

import os,sys,getopt,math

# Variables

dirmode=0
filmode=0
objname=""


# Functions

# Prints the help page
def Usage(execname):
	print "Usage ",execname,": "
	print "-"*(len(execname)+10)
	print "\n"
	print "-f <Filename>    : display the entropy of a single file"
	print "-d <Directory>   : recursively display the entropy of all"
	print "                   files starting at <Directory>\n\n"
	return

# Returns pr.log(pr) if pr>0, 0 otherwise
# where 0<=pr<1

def prlogpr(pr):
	if pr==0:	
		return 0
	return pr*math.log(pr) 

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
	# If we have anything, we'll compute the entropy.
	# entropy=sum(i in I) -pr[i]*log(pr[i])
	if total>0.0:
		for i in range(256):
			entropy=entropy-prlogpr(frequency[i]/total)
	else:
		entropy=0
	return entropy

# Walkdir - if in dir mode, let's process each file
def WalkDir(objname):
	listofdir=[]
	listoffiles=[]
	listofentropy=[]
	
	listofitem=os.listdir(objname)
	for item in listofitem:
		absitem=os.path.join(objname,item)
		if os.path.isfile(absitem):
			listoffiles.append(absitem)
		else:
			listofdir.append(absitem)
	for item in listofdir:
		WalkDir(item)
	for item in listoffiles:
		print item," : ",ComputeFileEntropy(item)
	return

# Main 


def main(argv):
	if len(argv) < 2:
		Usage(argv[0])
		sys.exit(-1)
	try:
		opts,args= getopt.getopt(argv[1:], "hf:d:", ["help", "file=", "directory="])
	except:
		Usage(argv[0])
		sys.exit(-2)

	filmode=0
	dirmode=0

	if opts[0][0]=='-h':
		Usage(argv[0])
		sys.exit(0)
	elif opts[0][0]=='-d':
		dirmode=1
		objname=opts[0][1]
		print "Dir Mode"
	elif opts[0][0]=='-f':
		filmode=1
		objname=opts[0][1]
		print "File Mode"
	print "\n\n"
	
	if filmode:
		entropy=ComputeFileEntropy(objname)
		print objname," : ",entropy
		sys.exit(0)
	elif dirmode:
		WalkDir(objname)
	
	return


# Go!

main(sys.argv)
	
