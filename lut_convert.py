#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys

# Simply specify input and output
cmap = sys.argv[1]
fout = sys.argv[2]

# Write header of LUT
f = open(fout, 'w')
f.write('%!VEST-LUT\n')
f.write('%%BeginInstance\n')
f.write('<<\n')
f.write('/SavedInstanceClassName /ClassLUT\n')
f.write('/PseudoColorMinimum 0.00\n')
f.write('/PseudoColorMaximum 1.00\n')
f.write('/PseudoColorMinControl /Low\n')
f.write('/PseudoColorMaxControl /High\n')
f.write('/PseudoColormap [\n')


colormap = matplotlib.cm.get_cmap(cmap)

n = 155.0
c0 = 0
c1 = 1
for v in np.arange(c0,1+1/n,1/n):
	c = colormap(v)
	cstring = '<-color{%.6f,%.6f,%.6f}->' % (c[0], c[1], c[2])
	f.write(cstring+'\n')

# Write last of the file
f.write(']\n')
f.write('>>\n\n')
f.write('%%EndInstance\n')
f.write('%%EOF\n')

# Done!