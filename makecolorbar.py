#!/usr/bin/env python

import numpy as np
import nibabel as nb
import subprocess as sp
import argparse 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def make_colorbar(nii_data, min_val, max_val):
    n = nii_data.shape[1]
    cb_data = np.linspace(float(min_val), float(max_val), n)
    for i in range(0,n):
        nii_data[:,i] = cb_data[i]

def create_empty_nii(fname):

	# Create empty nii with fslcreatehd
	# Usage: fslcreatehd <xsize> <ysize> <zsize> <tsize> <xvoxsize> <yvoxsize> <zvoxsize> <tr> 
	#       <xorigin> <yorigin> <zorigin> <datatype> <headername>
	#       fslcreatehd <nifti_xml_file> <headername>
	#  Datatype values: 2=char, 4=short, 8=int, 16=float, 64=double

	xsize = 100
	ysize = 1000
	zsize = 1
	tsize = 1
	xvoxsize = 0.1
	yvoxsize = 0.1
	zvoxsize = 0.1
	tr = 1
	xorigin = yorigin = zorigin = 0
	datatype = 16 #float
	headername = fname

	cmd = ['fslcreatehd', xsize, ysize, zsize, tsize, xvoxsize, yvoxsize, 
	       zvoxsize, tr, xorigin, yorigin, zorigin, datatype, headername]
	cmd = [str(x) for x in cmd]
	cmd = ' '.join(cmd)
	sp.call(cmd, shell=True)

	# Add check for .nii ending before!
	print "created empty .nii with file name: " + fname

	return fname

def main():
	parser = argparse.ArgumentParser(description='Make a pretty colorbar')
	parser.add_argument("-f", dest="fname", help="Filename")
	parser.add_argument("-min", dest="min_val", help="Min Value Colorbar")
	parser.add_argument("-max", dest="max_val", help="Max Value Colorbar")
	parser.add_argument("-lut", dest='lut', help='fslview colorcoding')

	args = parser.parse_args()

	
	create_empty_nii(args.fname)
	
	cb_nii = nb.load(args.fname)
	cb_data = cb_nii.get_data()

	make_colorbar(cb_data, args.min_val, args.max_val)

	nb.save(cb_nii, args.fname)

	# Save as image as well
	cmd = ['slicer', args.fname]
	if args.lut:
		cmd.append('-l')
		cmd.append(args.lut)

	cmd.append('-i')
	cmd.append(args.min_val)
	cmd.append(args.max_val)
	cmd.append('-z 1')
	cmd.append('cb.png')
	
	cmd = ' '.join(cmd)
	print cmd
	sp.call(cmd, shell=True)

	print "View your result by running"
	print(bcolors.OKGREEN + "fslview -m single " + args.fname + bcolors.ENDC)

if __name__ == "__main__":
	main()


