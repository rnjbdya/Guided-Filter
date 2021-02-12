import numpy as np
from numpy.linalg import inv
import scipy as sp
import scipy.ndimage
from skimage.color import rgb2gray
import imageio

def boxfilter(imSrc,r):
    # The function helps us find the mean of the images
    hei= imSrc[:,1].size
    wid= imSrc[1,:].size
    imDst = np.zeros([hei, wid])
    tile = [1] * imSrc.ndim
    tile[0] = r

    #cumulative sum over Y axis
    imCum = np.cumsum(imSrc, axis = 0)
    #difference over Y axis
    imDst[0:r+1, :] = imCum[r: 2*r+1, :]
    imDst[r+1:hei-r, :] = imCum[2*r+1:hei, :] - imCum[0:hei-2*r-1, :]
    imDst[hei-r:hei, :] = np.tile(imCum[hei-1, :], tile) - imCum[hei-2*r-1:hei-r-1, :]
    
    #cumulative sum over X axis
    tile = [1] * imSrc.ndim
    tile[1] = r
    imCum = np.cumsum(imDst, axis = 1)
    #difference over Y axis
    imDst[:, 0:r+1] = imCum[:, r:2*r+1]
    imDst[:, r+1:wid-r] = imCum[:, 2*r+1:wid] - imCum[:, 0:wid-2*r-1]
    a = imCum[:, wid-1]
    imDst[:, wid-r:wid] = np.tile(np.reshape(a, (a.size, -1)), tile) - imCum[:, wid-2*r-1:wid-r-1]

    return imDst
 
def guidedfilter(I, p, r, eps):
    #   GUIDEDFILTER for grayscale images

    hei = I[:, 1].size
    wid = I[1, :].size
    N = boxfilter(np.ones([hei, wid]), r)

    mean_I = boxfilter(I, r) / N
    mean_p = boxfilter(p, r) / N
    mean_Ip = boxfilter(I* p, r) / N
    cov_Ip = mean_Ip - mean_I* mean_p  # this is the covariance of (I, p) in each local patch.

    mean_II = boxfilter(I* I, r) / N
    var_I = mean_II - mean_I* mean_I

    a = cov_Ip / (var_I + eps)  # Eqn. (5) in the paper;
    b = mean_p - a* mean_I  # Eqn. (6) in the paper;

    mean_a = boxfilter(a, r) / N
    mean_b = boxfilter(b, r) / N

    q = mean_a* I + mean_b  # Eqn. (8) in the paper;
    return q

def guidedfilter_color(I, p, r, eps):
    #   GUIDEDFILTER for color images

    hei = I[:, 1, 1].size
    wid = I[1, :, 1].size
    N = boxfilter(np.ones([hei, wid]), r)
    mean_I_r = boxfilter(I[:, :, 0], r) / N
    mean_I_g = boxfilter(I[:, :, 1], r) / N
    mean_I_b = boxfilter(I[:, :, 2], r) / N

    mean_p = boxfilter(p, r) / N

    mean_Ip_r = boxfilter(I[:, :, 0]* p, r) / N
    mean_Ip_g = boxfilter(I[:, :, 1]* p, r) / N
    mean_Ip_b = boxfilter(I[:, :, 2]* p, r) / N

    # covariance of (I, p) in each local patch.
    cov_Ip_r = mean_Ip_r - mean_I_r* mean_p
    cov_Ip_g = mean_Ip_g - mean_I_g* mean_p
    cov_Ip_b = mean_Ip_b - mean_I_b* mean_p

    var_I_rr = boxfilter(I[:, :, 0]* I[:, :, 0], r) / N - mean_I_r* mean_I_r
    var_I_rg = boxfilter(I[:, :, 0]* I[:, :, 1], r) / N - mean_I_r* mean_I_g
    var_I_rb = boxfilter(I[:, :, 0]* I[:, :, 2], r) / N - mean_I_r* mean_I_b
    var_I_gg = boxfilter(I[:, :, 1]* I[:, :, 1], r) / N - mean_I_g* mean_I_g
    var_I_gb = boxfilter(I[:, :, 1]* I[:, :, 2], r) / N - mean_I_g* mean_I_b
    var_I_bb = boxfilter(I[:, :, 2]* I[:, :, 2], r) / N - mean_I_b* mean_I_b

    a = np.zeros([hei, wid, 3])
    for y in range(0, hei):
        for x in range(0, wid):
            Sigma = np.array([[var_I_rr[y, x], var_I_rg[y, x], var_I_rb[y, x]], \
                              [var_I_rg[y, x], var_I_gg[y, x], var_I_gb[y, x]], \
                              [var_I_rb[y, x], var_I_gb[y, x], var_I_bb[y, x]]])

            cov_Ip = np.array([[cov_Ip_r[y, x], cov_Ip_g[y, x], cov_Ip_b[y, x]]])

            a[y, x, :] = np.matmul(cov_Ip, inv(Sigma + eps * np.identity(3)))  
            # as per the equation obtained by linear regression

    b = mean_p - a[:, :, 0]* mean_I_r - a[:, :, 1]* mean_I_g - a[:, :, 2]* mean_I_b

    q = boxfilter(a[:, :, 0], r)* I[:, :, 0] \
        + boxfilter(a[:, :, 1], r)* I[:, :, 1] \
        + boxfilter(a[:, :, 2], r)* I[:, :, 2] \
        + boxfilter(b, r) / N
    return q

#for smoothing
cat_I = imageio.imread('/media/ranjai/extra/Course of Study/Computer Vision/guided/guided-filter-images/img_smoothing/cat.bmp').astype(np.float32) / 255
cat_I = rgb2gray(cat_I)
cat_p = cat_I #here the guide and the input image are choosen to be the same since we are only performing smoothing
#cat_r = [2, 4, 8]  # try r=2, 4, or 8
#cat_eps = [0.1**2, 0.2**2, 0.4**2] #trying eps=0.1^2, 0.2^2, 0.4^2

cat_r = 8
cat_eps = 0.4**2

cat_q = guidedfilter(cat_I, cat_p,cat_r, cat_eps) 
imageio.imwrite('cat_smoothed9.png', cat_q)

#for feathering
toy_I = imageio.imread('/media/ranjai/extra/Course of Study/Computer Vision/guided/guided-filter-images/img_feathering/toy.bmp').astype(np.float32) / 255
toy_p = imageio.imread('/media/ranjai/extra/Course of Study/Computer Vision/guided/guided-filter-images/img_feathering/toy-mask.bmp').astype(np.float32) / 255
toy_p = rgb2gray(toy_p)

feather_r = 10 # 60, 70, 10
feather_eps = 10**(-6) # 6,3,9

feather_q = guidedfilter_color(toy_I, toy_p, feather_r, feather_eps)
imageio.imwrite('feathering3.png', feather_q)

cave_I = imageio.imread('/media/ranjai/extra/Course of Study/Computer Vision/guided/guided-filter-images/img_flash/cave-flash.bmp').astype(np.float32) / 255
cave_p = imageio.imread('/media/ranjai/extra/Course of Study/Computer Vision/guided/guided-filter-images/img_flash/cavenoflash.bmp').astype(np.float32) / 255

cave_r = 10# 8, 10, 12
cave_eps = 0.00026 #0.02**2, 0.03**2, 0.04**2

cave_q = np.zeros(cave_I.shape)
cave_q[:, :, 0] = guidedfilter(cave_I[:, :, 0], cave_p[:, :, 0], cave_r, cave_eps)
cave_q[:, :, 1] = guidedfilter(cave_I[:, :, 1], cave_p[:, :, 1], cave_r, cave_eps)
cave_q[:, :, 2] = guidedfilter(cave_I[:, :, 2], cave_p[:, :, 2], cave_r, cave_eps)

imageio.imwrite('cave12.png', cave_q)

tulip_I = imageio.imread('/media/ranjai/extra/Course of Study/Computer Vision/guided/guided-filter-images/img_enhancement/tulips.bmp').astype(np.float32) / 255
tulip_p = tulip_I

tulip_r = 18 #16, 14, 18
tulip_eps = 0.3**2 #0.1**2, 0.2**2, 0.3**2

tulip_q = np.zeros(tulip_I.shape)
tulip_q[:, :, 0] = guidedfilter(tulip_I[:, :, 0], tulip_p[:, :, 0], tulip_r, tulip_eps)
tulip_q[:, :, 1] = guidedfilter(tulip_I[:, :, 1], tulip_p[:, :, 1], tulip_r, tulip_eps)
tulip_q[:, :, 2] = guidedfilter(tulip_I[:, :, 2], tulip_p[:, :, 2], tulip_r, tulip_eps)

imageio.imwrite('tulip9.png', tulip_q)
