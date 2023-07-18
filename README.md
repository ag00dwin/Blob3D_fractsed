# Blob3D_fractsed

This repository contains scripts with code useful for processing of Blob3D output -dat.xlsx files. This code is useful for sedimentological applications, using shape parameters to create clastsize distribution histograms and for statistically assessing clast spatial orientation.  

## Referencing

For use of this code, please cite: Goodwin A., Tartèse R., Garwood R., and Almeida N. V. (2023) A 3D Petrofabric Examination of Martian Breccia NWA 11220 via X-ray Computed Microtomography: Evidence for an Impact Lithology. Journal of Geophysical Research: Planets. *In review.*

Doi and further information will be added upon publication 

This code uses the output from free software known as [Blob3D](https://www.ctlab.geo.utexas.edu/software/blob3d/) which should be referenced as: Ketcham, R. A. (2005). Computational methods for quantitative analysis of three-dimensional features in geological specimens. Geosphere, 1(1), 32–41. https://doi.org/10.1130/GES00001.1 

Blob3D can be downloaded from: [HERE](https://www.ctlab.geo.utexas.edu/software/blob3d/)

>Blob3D is designed for efficient measurement of up to thousands of discrete features (e.g. clasts,mineral grains, porphyroblasts, voids) within a single sample. Blob3D is unique because it gives the program operator primary control over data interpretation and measurement, and all computations are carried out in 3D, rather than individually on a series of 2D slices.

### License

The project is licensed under the GNU-v3 license.

## Installation

No installation is required. Scripts are short and designed to be adapted. Python scripts can be downloaded from this repository and either imported as modules locally, copied into scripts and run as defined functions, or intergrating into pre-existing scripts where such functionality is required.

## Python Scrips

All python scripts import the -dat.xlsx generated when performing "Extract" within Blob3D. Python scripts use the heading names automatically generated. For studying orientation, shape, and shape factors a primitive ellipsoid will need to be fitted (and the equation reported) to ensure the correct coefficients. 

### _fractual_plot.py

Creates a log-log cumulative plot of the number of clasts with a diameter **d** and greater **N(>d)** against that clast diameter **d**. Values annotating linear fits are the fractal dimension '*D-value*'.

### _clastshape_zingg_plot.py

Creates a Zingg (1935) diagram that shows the relative dimensions of the long (L), short (S), and
intermediate (I) axes of a particle. 

Reference: Zingg, T. (1935). Beitrag zur schotteranalyse. ETH Zurich.

### _shape_factor_plot.py

Creates a plot of the **shape factor** as defined by Wilson and Huang (1979) against clast diameter **d**

Shape factor is defined as `(ShapeB+ShapeC)/2*ShapeA`

Reference: Wilson, L., & Huang, T. C. (1979). The influence of shape on the atmospheric settling velocity of volcanic ash particles. Earth and Planetary Science Letters, 44(2), 311–324. https://doi.org/https://doi.org/10.1016/0012-821X(79)90179-1

### _steronetplot.py

Creates a stereonet of orientation based on sphericity and minimum clast diameter. Simply plots using [mplstereonet] (https://pypi.org/project/mplstereonet/) for the parameters imported from the -dat.xlsx file. More imformation on [mplstereonet] (https://pypi.org/project/mplstereonet/) can be found [here](https://mplstereonet.readthedocs.io/en/latest/mplstereonet.html)
