# Guided-Filter
Implementation of Guided Filter- based on the paper by He et al.
Guided filters are edge preserving-smoothing filters, which use an additional image called guide image which helps in filtering. 

If we have a guidance image 'I' and an input image 'p', we assume that the output image of the filter will be 'q'.  According to the paper ‘Guided Image Filtering’[He et. al], the filtering output 'I' at any pixel can be expressed as a weighted average:
