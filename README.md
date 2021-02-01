# Guided-Filter
Implementation of Guided Filter- based on the paper by He et al. <br />
Guided filters are edge preserving-smoothing filters, which use an additional image called guide image which helps in filtering. 

If we have a guidance image 'I' and an input image 'p', we assume that the output image of the filter will be 'q'.  According to the paper ‘Guided Image Filtering’[He et. al], the filtering output 'I' at any pixel can be expressed as a weighted average:
![Equation-1](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-1.png) \

The paper assumes that the guided filter is a local linear model between the images 'I' and 'q', where q is taken as a linear transform of I in window w<sub>k</sub>  centered at the pixel K:
![Equation-2](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-2.png) \

Here, a<sub>k</sub> and b<sub>k</sub> are some linear coefficients which are assumed to be constant in w<sub>k</sub>

A square window of radius ‘r’ has been used and the model ensures that the output q has an edge only when the guide image I has an edge as ∇ q = a ∇ I.

Since the motivation here is to minimize the difference between q and p, the cost function shall be given as:
![Equation-3](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-3.png)

The ε is the regularization parameter, which helps to make sure that 'a' doesn’t have more significance that needed.

Using linear regression the values of ak and bk can be found as:
![Equation-4](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-4.png) \

Applying the window to all of the pixels we can get the output q. Since a pixel maybe involved in multiple windows, we simply average out all the possible q values. The filter output is then given by:
![Equation-5](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-5.png) \

Algorithm:
    1. Find the mean values of I and p using the window with radius r.
    2. Find the correlation of I with itself and again between I and p using the same window of radius r.
    3. Find the variance of I and the co-variance between I and p.
    4. Find the series of values of a and b.
    5. Find the mean value of a and b.
    6. Calculate q.
    
 Results:
