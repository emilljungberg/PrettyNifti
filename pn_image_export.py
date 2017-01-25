import nibabel as nb
import numpy as np
import matplotlib.pyplot as plt
import argparse


def plot_slice_nii(nii, mask_nii, imslice, echo, cmin, cmax, cbar, cmap, fname):
	# Recommended colormaps
	# viridis, inferno, magma, plasma
	nii_in = nb.load(nii)
	img = nii_in.get_data()
	hdr = nii_in.get_header()
	pixdim = hdr['pixdim']

	multi_echo = False
	if len(np.shape(img)) > 3:
		multi_echo = True


	if imslice == None:
		h = nii_in.header
		nslices = h.get_data_shape()[2] - 1
		slice_n = int(round(nslices/2))
		if multi_echo:
			s = np.s_[:,:,slice_n,echo]
		else:
			s = np.s_[:,:,slice_n]
		aspect_ratio = pixdim[1]/pixdim[2]

	else:
		slice_dim = imslice.split(',')[0]
		slice_n = int(imslice.split(',')[1])
		
		if slice_dim == 'x':
			if multi_echo:
				s = np.s_[slice_n,:,:,echo]
			else:
				s = np.s_[slice_n,:,:]

			mask_s = np.s_[slice_n,:,:]
			aspect_ratio = pixdim[2]/pixdim[3]

		elif slice_dim == 'y':
			if multi_echo:
				s = np.s_[:,slice_n,:,echo]
			else:
				s = np.s_[:,slice_n,:]

			mask_s = np.s_[:,slice_n,:]
			aspect_ratio = pixdim[1]/pixdim[3]

		elif slice_dim == 'z':
			if multi_echo:
				s = np.s_[:,:,slice_n, echo]
			else:
				s = np.s_[:,:,slice_n]

			mask_s = np.s_[:,:,slice_n]
			aspect_ratio = pixdim[1]/pixdim[2]


	if mask_nii:
		mask_in = nb.load(mask_nii)
		mask_img = mask_in.get_data()
		mask_img = np.nan_to_num(mask_img)
		#img = mask_img * img
		
		mask_slice = mask_img[mask_s]
		mask_slice = np.rot90(mask_slice,1)

	img_slice = img[s]
	img_slice = np.rot90(img_slice,1)

	if mask_nii:
		alpha_img = np.ma.masked_where(mask_slice != 1, img_slice)
		B = np.argwhere(mask_slice)
		(ystart, xstart), (ystop, xstop) = B.min(0), B.max(0) + 1 
		crop_alpha_img = alpha_img[ystart:ystop, xstart:xstop]
		img_slice = crop_alpha_img
	
	# Find robust limit to view the image
	if cmin != None:
		cmin = cmin
	else:
		cmin = np.percentile(img_slice, 0.1)

	if cmax != None:
		cmax = cmax
	else:        
		cmax = np.percentile(img_slice, 99.9)
	
	fig = plot_slice(img_slice, aspect_ratio, cmin,cmax,cmap,cbar)
	save_img(fig, fname)

def plot_slice(img,aspect_ratio,cmin,cmax,cmap,cbar):

	fig = plt.imshow(img, clim=(cmin, cmax), interpolation='none')
	print aspect_ratio
	plt.axes().set_aspect(1/aspect_ratio)
	if cbar:
		plt.colorbar()
		
	fig.set_cmap(cmap)
	plt.axis('off')
	
	return fig
	
def save_img(fig, fname):
	print 'Saving image as: %s' % (fname)
	plt.savefig(fname, dpi=300, 
		orientation='portrait', papertype=None, format=None,
		transparent=True, bbox_inches='tight', pad_inches=0.1,
		frameon=False)
	plt.close()

def main(args):
	img_nii = args.i
	mask_nii = args.m
	imslice = args.slice
	cmin = args.cmin
	cmax = args.cmax
	cmap = args.cmap
	cbar = args.cbar
	out_fname = args.o
	echo = args.echo

	plot_slice_nii(img_nii, mask_nii, imslice, echo, cmin, cmax, cbar, cmap, out_fname)

def parse_args():
	parser = argparse.ArgumentParser(description=
		"Tool to save niftis as png images. A list of colormaps can be found at http://matplotlib.org/users/colormaps.html")
	parser.add_argument("-i", metavar='input',required=True, help='Nifti input image')
	parser.add_argument('-o', metavar='output', required=True, help='Output image filename')
	parser.add_argument("-m", metavar='mask', default=None, required=False, help='Nifti mask')
	parser.add_argument("--slice", default=None, required=False, help='Slice dimension and slice number (Ex: z,10')
	parser.add_argument("--echo", default=0, required=False, type=int, help='Echo number for multi echo images')
	parser.add_argument("--cmin", default=None, required=False, type=float, help='Min intensity range')
	parser.add_argument("--cmax", default=None, required=False, type=float, help='Max intensity range')
	parser.add_argument("--cmap", default=None, required=False, help='Colormap (viridis, inferno, gray')
	parser.add_argument("--cbar", default=False, required=False, type=int, help='Boolean for colorbar')

	args = parser.parse_args()

	return args

if __name__ == "__main__":
	# execute only if run as a script
	args = parse_args()
	main(args)