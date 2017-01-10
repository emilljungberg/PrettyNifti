#!/bin/bash
lut_converter () {
	python lut_convert.py $1 fsl_luts/$1.lut	
}

lut_converter viridis 
lut_converter inferno
lut_converter plasma
lut_converter magma
lut_converter afmhot
lut_converter bone
lut_converter summer
lut_converter RdBu
lut_converter RdGy
lut_converter Spectral