#!/bin/bash
lut_converter () {
	echo Generating FSL lut: ${1}
	python lut_convert.py $1 fsl_luts/$1.lut	
}

# See http://matplotlib.org/users/colormaps.html for a full overview

# Perceptually Uniform Sequential colormaps
lut_converter viridis 
lut_converter inferno 		# Works well for BW conversion
lut_converter plasma
lut_converter magma			# Works well for BW conversion
		
# Sequential colormaps that are somewhat perceptually uniform
lut_converter Blues
lut_converter BuPu
lut_converter Greens
lut_converter Oranges
lut_converter PuBu
lut_converter YlGn
lut_converter YlOrBr
lut_converter afmhot
lut_converter bone
lut_converter gist_heat
lut_converter gray
lut_converter summer

# Diverging colormaps (Shose those that are most linear)
lut_converter BrBG
lut_converter PiYG
lut_converter PRGn			# Looks a bit darker in Purple when BW
lut_converter RdBu 			# Looks uniform in BW as well
lut_converter RdGy 			# Looks uniform in BW as well
lut_converter RdYlBu		# Looks uniform in BW but lack of contrast
lut_converter RdYlGn
lut_converter Spectral