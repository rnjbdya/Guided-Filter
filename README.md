# Guided-Filter
Implementation of Guided Filter- based on the paper by He et al.
<br />
Guided filters are edge preserving-smoothing filters, which use an additional image called guide image which helps in filtering. 

If we have a guidance image 'I' and an input image 'p', we assume that the output image of the filter will be 'q'.  According to the paper ‘Guided Image Filtering’[He et. al], the filtering output 'I' at any pixel can be expressed as a weighted average:<br />
<br />
![Equation-1](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-1.png) \
<br />
The paper assumes that the guided filter is a local linear model between the images 'I' and 'q', where q is taken as a linear transform of I in window w<sub>k</sub>  centered at the pixel K:
<br />
![Equation-2](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-2.png) \
<br />
Here, a<sub>k</sub> and b<sub>k</sub> are some linear coefficients which are assumed to be constant in w<sub>k</sub>

A square window of radius ‘r’ has been used and the model ensures that the output q has an edge only when the guide image I has an edge as ∇ q = a ∇ I.

Since the motivation here is to minimize the difference between q and p, the cost function shall be given as:
<br />
![Equation-3](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-3.png)
<br />
The ε is the regularization parameter, which helps to make sure that 'a' doesn’t have more significance that needed.

Using linear regression the values of ak and bk can be found as:
<br />
![Equation-4](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-4.png) \
<br />
Applying the window to all of the pixels we can get the output q. Since a pixel maybe involved in multiple windows, we simply average out all the possible q values. The filter output is then given by:
<br />
![Equation-5](https://github.com/rnjbdya/Guided-Filter/blob/main/eqns_from_paper/eqn-5.png) \
<br />
## Algorithm:
    1. Find the mean values of I and p using the window with radius r.
    2. Find the correlation of I with itself and again between I and p using the same window of radius r.
    3. Find the variance of I and the co-variance between I and p.
    4. Find the series of values of a and b.
    5. Find the mean value of a and b.
    6. Calculate q.
    
## Results:
 Here I have implemented the guided filter in multiple scenarios as suggested in the original paper and while doing so, I have experimented with multiple values of ‘r’ and ‘ ε’.

Initially image smoothening was performed. Here we experimented values of r in the range, ‘2, 4, 8’
and  ε in the range ‘0.1<sup>2</sup>, 0.2<sup>2</sup>, 0.4<sup>2</sup>’. For smoothing purpose both the image I and p were taken as same image. As we can see from the results obtained(shown below), we can obtain a varying degree of blurring by varying the values of r and  ε. The image is more blurred when the value of r is greater.
<br />
### Input:
<br />
![Input for Image Smoothening](https://github.com/rnjbdya/Guided-Filter/blob/main/input_images/cat.bmp)
<br />
### Output:
<br />
![Smoothening-1](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed1.png)
![Smoothening-2](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed2.png)
![Smoothening-3](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed3.png)
<br />
![Smoothening-4](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed4.png)
![Smoothening-5](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed5.png)
![Smoothening-6](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed6.png)
<br />
![Smoothening-7](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed7.png)
![Smoothening-8](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed8.png)
![Smoothening-9](https://github.com/rnjbdya/Guided-Filter/blob/main/output/cat_smoothed9.png)
<br />
