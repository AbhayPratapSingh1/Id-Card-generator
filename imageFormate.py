import cv2 
import numpy as np

class ImageHandler:
    def __init__(self,imagePath = "1.png"):
        self.imagePath = imagePath
        self.image = cv2.imread(imagePath)
        self.isCircle = False

    def resizeImageOnHeight(self,Hnew):
        w = self.breadthCalculator(Hnew)
        self.resize(h=Hnew, w=w)

    def rectangleImage(self):
        self.image = cv2.imread(self.imagePath)

    def toSquareImage(self,h = 600):
        self.resize( x = h , w = h)
        self.image = cv2.imread(self.imagePath)

    def resize(self, x =600, y =1000): 
        self.image = cv2.imread(self.imagePath)
        if self.isCircle :
            self.toCircleImage()
        self.image =cv2.resize(self.image, (x, y))
        
    def toCircleImage(self):
        cv2.circle(self.image, (self.image.shape[1]//2,self.image.shape[0]//2), self.image.shape[0]//2 + 80 , (255,255,255), 160)

    def breadthCalculator(self, h):
        w =  ( h / self.image.shape[0] ) * self.image.shape[1]
        return int(w)
    
    def heightCalculator(self, w):
        h =  ( w / self.image.shape[1] ) * self.image.shape[0]
        return int(h)

    def show(self):
        cv2.imshow("image", self.image)
        cv2.waitKey(0)

a = ImageHandler()