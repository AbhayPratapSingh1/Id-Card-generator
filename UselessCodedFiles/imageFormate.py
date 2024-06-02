import cv2 
import numpy as np
from buttonsSetUpClasses.button import button

class ImageField(button):
    def __init__(self, imagePath="1.png"):
        super().__init__( x = 20 , y = 300 , h = 10 , w = 10 )
        self.imageField(imagePath)
    
    def imageField(self, path = "1.png"):
        self.image = ImageHandler(path)
        self.image.resizeImageOnHeight(200)
        self.setPos((40,40))
        self.setDimenstion((self.image.h, self.image.w))
        self.setLastCord((40 + self.image.w ,40 + self.image.h))
        

    def setDimenstion(self,pos):
        self.h = pos[1]
        self.w = pos[0]
        self.x2 = self.w + self.x 
        self.y2 = self.h + self.y

    def isSelect(self, pos):
        # to set bewteen the box of field of 20 X 20 above the left most top corner
        if (pos[0] > self.x) and (pos[0] < self.x+10) and (pos[1] > self.y-10) and (pos[1] < self.y) :
            return 0
        elif (pos[0] > self.x + self.w ) and (pos[0] < self.x + self.w +5) and (pos[1] > self.y + self.h) and (pos[1] < self.y+self.w+5) :
            return 1
        return -1
    
    


class ImageHandler(button):
    def __init__(self,imagePath = "1.png"):
        super().__init__(x = 20, y=20, h=100, w =100)
        self.fixedRatio = True
        self.imagePath = imagePath
        self.isCircle = False
        self.isSquare = False
        self.toRectangleImage()
        self.resizeImageOnHeight(100)


    def action(self, type , pos):
        if type == 0 :
            self.setPos(pos)
        elif type == 1:
            self.resize(pos)
            self.setDimension()

    def setDimension(self):
        # it will set x2 , y2, h , w of the field 
        self.setLastCord((self.x + self.image.shape[1], self.y + self.image.shape[0]))


    def toRectangleImage(self):
        self.resizeImageOnHeight(self.h)
        self.setDimension()

    def toSquareImage(self,h = 600):
        self.imageResize( x = h , w = h)
        self.setDimension()

    def toCircleImage(self, dim):
        cv2.circle(self.image, (self.image.shape[1]//2,self.image.shape[0]//2), self.image.shape[0]//2 + 80 , (255,255,255), 160)
        if self.toSquareImage :
            self.imageResize(dim[0], dim[1])
        else :
            self.imageResize(dim[0], dim[1])
        self.setDimension()
    
    def resize(self, w = 300, h =300):
        self.w = self.w 
        self.h = self.h
        if self.isSquare :
            self.h = h
            self.w = self.h
        if self.isCircle :
            self.toCircleImage()    
        else :
            self.toRectangleImage()
        self.setDimension()
    
    def imageResize(self,x,y):
        self.image = cv2.imread(self.imagePath)
        cv2.resize(self.image , (x, y))

    def resizeImageOnHeight(self,Hnew):
        w = self.breadthCalculator(Hnew)
        self.imageResize(h=Hnew, w=w)
        self.setDimension()
    
    def resizeImageOnWidth(self,Wnew):
        h = self.heightCalculator(Wnew)
        self.imageResize(h=h, w=Wnew)
        self.setDimension()

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