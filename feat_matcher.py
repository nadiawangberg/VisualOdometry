import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img1 = cv.imread('data/im1.png')
img2 = cv.imread('data/im2.png')
gray1= cv.cvtColor(img1,cv.COLOR_BGR2GRAY)
gray2= cv.cvtColor(img2,cv.COLOR_BGR2GRAY)

#Detectors
sift = cv.xfeatures2d.SIFT_create()
orb = cv.ORB_create()

#should change params

#Detection
kp1, des1 = sift.detectAndCompute(gray1,None) #Descriptor also computed
kp2, des2 = sift.detectAndCompute(gray2,None) #Descriptor also computed

#orb for img1
kp1_o = orb.detect(gray1,None)
kp1_o, des1_o = orb.compute(gray1, kp1_o)

#orb for img2
kp2_o = orb.detect(gray2,None)
kp2_o, des2_o = orb.compute(gray2, kp2_o)

#FLANN
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params,search_params)

#SIFT
matches = flann.knnMatch(des1,des2,k=2)

#Try to only use good matches
matchesMask = [[0,0] for i in range(len(matches))]

#Ratio test (SIFT)
for i,(m,n) in enumerate(matches):
    if m.distance < 0.55*n.distance:
        matchesMask[i]=[1,0]

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)

img_sift = cv.drawMatchesKnn(gray1,kp1,gray2,kp2,matches,None,**draw_params)

plt.figure(1)
plt.subplot(211)
plt.imshow(img_sift)
#plt.imshow(img_sift),plt.show()



#ORB

#FLANN
#FLANN_INDEX_KDTREE = 1
FLANN_INDEX_LSH = 6
index_params_o= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2search_params = dict(checks=50)   # or pass empty dictionary

flann_o = cv.FlannBasedMatcher(index_params_o,search_params)

matches_o = flann_o.knnMatch(des1_o, des2_o, k=2)

matchesMask_o = [[0,0] for i in range(len(matches_o))]

#Ratio test (ORB)
for i,(m,n) in enumerate(matches_o):
    if m.distance < 0.8*n.distance:
        matchesMask_o[i]=[1,0]

draw_params_o = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask_o,
                   flags = cv.DrawMatchesFlags_DEFAULT)

img_orb = cv.drawMatchesKnn(gray1,kp1_o,gray2,kp2_o,matches_o,None,**draw_params_o)

#plt.figure(2)
plt.subplot(212)
plt.imshow(img_orb)
plt.show()
#plt.imshow(img_orb,),plt.show()

#Display images
"""
cv.imshow('fast',fast_img)
cv.imshow('sift',sift_img)
cv.imshow('original',gray1)
cv.waitKey(0)
cv.destroyAllWindows()
"""