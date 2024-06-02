import time
import cv2
import numpy as np
def nothing(self):
    pass

cv2.namedWindow("tracebars")
cv2.createTrackbar("R" , "tracebars" , 0 , 255 , nothing )
cv2.createTrackbar("G" , "tracebars" , 0 , 255 , nothing )
cv2.createTrackbar("B" , "tracebars" , 0 , 255 , nothing )
cv2.createTrackbar("FontSize" , "tracebars" , 0 , 100 , nothing )

img = np.zeros((600,600,3),np.uint8)
while True:
    R =  cv2.getTrackbarPos("R","tracebars")# 0 means up
    G =  cv2.getTrackbarPos("G","tracebars")# 0 means up
    B =  cv2.getTrackbarPos("B","tracebars")# 0 means up
    FontSize =  cv2.getTrackbarPos("FontSize","tracebars")# 0 means up

    print("R",R)
    print("G",G)
    print("B",B)
    print("FontSize",FontSize)
    cv2.imshow("omasd",img)
    cv2.waitKey(0)
