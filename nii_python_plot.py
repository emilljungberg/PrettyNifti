import nibabel as nb
import numpy as np
import matplotlib.pyplot as plt
import argparse


def plot_slice_nii(nii, mask_nii, zslice, cmin, cmax, cbar, cmap, fname):
    # Recommended colormaps
    # viridis, inferno, magma, plasma
    
    nii_in = nb.load(nii)
    img = nii_in.get_data()

    if zslice == None:
    	h = nii_in.header
    	nslices = h.get_data_shape()[2] - 1
    	zslice = int(round(nslices/2))
    
    if mask_nii:
        mask_in = nb.load(mask_nii)
        mask_img = mask_in.get_data()
        mask_img = np.nan_to_num(mask_img)
        #img = mask_img * img
        
        mask_slice = mask_img[:,:,zslice]
        mask_slice = np.rot90(mask_slice,1)
        
    img_slice = img[:,:,zslice]
    img_slice = np.rot90(img_slice,1)

    if mask_nii:
        alpha_img = np.ma.masked_where(mask_slice != 1, img_slice)
        B = np.argwhere(mask_slice)
        (ystart, xstart), (ystop, xstop) = B.min(0), B.max(0) + 1 
        crop_alpha_img = alpha_img[ystart:ystop, xstart:xstop]
        img_slice = crop_alpha_img
    
    # Find robust limit to view the image
    if cmin:
        cmin = int(crange[0])
    else:
        cmin = int(np.percentile(img_slice, 0.1))

    if cmax:
        cmax = int(crange[1])
    else:        
        cmax = int(np.percentile(img_slice, 99.9))
    
    fig = plot_slice(img_slice,cmin,cmax,cmap,cbar)
    save_img(fig, fname)

def plot_slice(img,cmin,cmax,cmap,cbar):

    fig = plt.imshow(img, clim=(cmin, cmax), interpolation='none')
    if cbar:
        plt.colorbar()
        
    fig.set_cmap(cmap)
    plt.axis('off')
    
    return fig
    
def save_img(fig, fname):
    plt.savefig(fname, dpi=300, 
        orientation='portrait', papertype=None, format=None,
        transparent=True, bbox_inches='tight', pad_inches=0.1,
        frameon=False)
    plt.close()

def main(args):
	img_nii = args.i
	mask_nii = args.m
	zslice = args.slice
	cmin = args.cmin
	cmax = args.cmax
	cmap = args.cmap
	cbar = args.cbar
	out_fname = args.o

	plot_slice_nii(img_nii, mask_nii, zslice, cmin, cmax, cbar, cmap, out_fname)

def parse_args():
	parser = argparse.ArgumentParser(description=
		"Tool to save niftis as png images. A list of colormaps can be found at http://matplotlib.org/users/colormaps.html")
	parser.add_argument("-i", metavar='input',required=True, help='Nifti input image')
	parser.add_argument('-o', metavar='output', required=True, help='Output image filename')
	parser.add_argument("-m", metavar='mask', default=None, required=False, help='Nifti mask')
	parser.add_argument("--slice", default=None, required=False, type=int, help='Slice to image, default middle')
	parser.add_argument("--cmin", default=None, required=False, type=int, help='Min intensity range')
	parser.add_argument("--cmax", default=None, required=False, type=int, help='Max intensity range')
	parser.add_argument("--cmap", default=None, required=False, help='Colormap (viridis, inferno, gray')
	parser.add_argument("--cbar", default=False, required=False, type=bool, help='Boolean for colorbar')

	args = parser.parse_args()

	return args

if __name__ == "__main__":
    # execute only if run as a script
    args = parse_args()
    main(args)