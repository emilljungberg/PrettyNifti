#!/usr/bin/env python 

import nibabel as nb
import numpy as np
import ggplot
import matplotlib.pyplot as plt
import seaborn as sns
from optparse import OptionParser

# Todo: Add input option for slice coverage

def parse_options():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest='filename', help='Input nii name')
	parser.add_option("-m", "--mask", dest='mask', help='Mask to restrict ROI')
	parser.add_option("-r", dest='range', nargs=2, help='Range of histogram')
	parser.add_option("-n", dest='n', help='Number of bins')
	parser.add_option('-t', action='store_true', dest='save_text', default=False, 
		help="Save text file with histogram data")
	parser.add_option('-p', action='store_true', dest='save_plot', default=False, 
		help="Save plot to image file")

	(options, args) = parser.parse_args()
	return options, args

def load_data_and_mask(qmri_fname, mask_fname, s0, s1, thr=0.5, plot=False):
    
    qmri_nii = nb.load(qmri_fname)
    mask_nii = nb.load(mask_fname)
    
    qmri_data = qmri_nii.get_data()
    mask_data = mask_nii.get_data()
    
    mask_data = np.where(mask_data > thr, 1, np.nan)
    masked_qmri = np.multiply(qmri_data, mask_data)
    
    (nx,ny,nz) = np.shape(qmri_data)
    if s1 < 0:
        s1 = nz
        
    if plot:
        pltslice = int(np.round(nz/2.0))
        plt.subplot(1,3,1)
        plt.imshow(qmri_data[:,:,pltslice],cmap='viridis')
        plt.subplot(1,3,2)
        plt.imshow(mask_data[:,:,pltslice],cmap='viridis', vmin=0, vmax=1)
        plt.subplot(1,3,3)
        plt.imshow(masked_qmri[:,:,pltslice], cmap='viridis')
        plt.show()
    
    masked_qmri = masked_qmri[:,:,s0:s1]
    flat_data = masked_qmri.flatten()
    flat_data = np.where(flat_data > 0, flat_data, np.nan)
    idx = np.isfinite(flat_data)
    flat_data = flat_data[idx]
    
    return masked_qmri, flat_data

def example_process(options, args):
	qmri_fname = options.filename
	mask_fname = options.mask
	r = options.range
	n = options.n
	save_plot = options.save_plot

	masked_qmri, flat_data = load_data_and_mask(qmri_fname, mask_fname, s0=0, s1=-1, thr=0.5, plot=False)

	sns.set_style("whitegrid", {'axes.grid' : False})
	sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 3, 'font.family': [u'sans-serif'],
	 'font.sans-serif': u'Calibri','axes.facecolor': 'white','figure.facecolor': 'white',})
	
	sns.distplot(flat_data, hist=False, bins=100, label='Data 1')
	plt.xlim([0, 0.4])
	plt.xlabel('q Metric')
	plt.legend()
	sns.despine()
	plt.ylabel('Frequency [a.u.]')
	
	if save_plot:
		plt.savefig('hist.png', dpi=300, transparent=True)
	
	plt.show()

if __name__ == "__main__":
    options, args = parse_options()
    example_process(options, args)