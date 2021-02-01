# Guided-Filter
Implementation of Guided Filter- based on the paper by He et al. <br />
Guided filters are edge preserving-smoothing filters, which use an additional image called guide image which helps in filtering. 

If we have a guidance image 'I' and an input image 'p', we assume that the output image of the filter will be 'q'.  According to the paper ‘Guided Image Filtering’[He et. al], the filtering output 'I' at any pixel can be expressed as a weighted average: 

!(https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-1.png) \

The paper assumes that the guided filter is a local linear model between the images 'I' and 'q', where q is taken as a linear transform of I in window wk  centered at the pixel K:
