import cv2 
import numpy as np
from buttonsSetUpClasses.button import button

class imageField(button):
    def __init__(self , path= "User_Data_Place_Here/1.png"):
        super().__init__()
        self.path = path
        self.isCircle = False
        self.isSquare = False
        self.inRatio = True
        self.resizeTO((200,200))
        
    def __resize(self, size):
        self.image = cv2.resize(self.image,size)
        
    
    def setDimension(self,size):
        self.h = size[1]
        self.w = size[0]
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h
    
    def resizeTO(self, size):
        if self.isCircle :
            self.toCircle(size)
        elif self.isSquare:
            self.toSquare(size)
        else : 
            self.toRectangle(size)
        
    def toCircle(self, size):
        self.image = cv2.imread(self.path)
        cv2.circle(self.image, (self.image.shape[1]//2,self.image.shape[0]//2), self.image.shape[0]//2 + 80 , (255,255,255), 160)
        if self.inRatio:
            size = list(size)
            size[0] = self.breadthCalculator(size[1])
            self.__resize(size)
        else : 
            self.__resize(size)
        self.setDimension(size)

    def toSquare(self,size):
        self.image = cv2.imread(self.path)
        size = list(size)
        size[0] = size[1]
        self.__resize(size)
        self.setDimension(size)

    def toRectangle(self, size):
        self.image = cv2.imread(self.path)
        if self.inRatio :
            size = list(size)
            size[0] = self.breadthCalculator(size[1])
            self.__resize(size)
        else :
            self.__resize(size)
        self.setDimension(size)

    def breadthCalculator(self, h):
        w =  ( h / self.image.shape[0] ) * self.image.shape[1]
        return int(w)
    
    def setMode(self, mode):
        # mode 1 = rectangle / original
        # mode 2 = square
        # mode 3 = circle
        # mode 4 = inRatio / toggle
        match mode:
            case 1:
                self.isCircle = False
                self.isSquare = False
            case 2 :
                self.isCircle = False
                self.isSquare = True
            case 3 :
                self.isCircle = True
                self.isSquare = False
            case 4 :
                self.inRatio = not self.inRatio

        self.resizeTO((self.w, self.h))
                
        

    def isSelected(self, pos):
        if ((pos[0] > self.x) and (pos[0] < self.x+10) and (pos[1] > self.y-10) and (pos[1] < self.y) ) or (pos[0] > self.x and pos[0]<self.x2 and pos[1] > self.y and pos[1] < self.y2 ):
            return 0
        elif (pos[0] > self.x + self.w ) and (pos[0] < self.x + self.w +5) and (pos[1] > self.y + self.h) and (pos[1] < self.y+self.w+5) :
            return 1
        return -1
    
    def action(self, tochange , pos ):
        if tochange == 0:
            self.setPos(pos)
        else : 
            x = pos[0] - self.x
            y = pos[1] - self.y
            self.resizeTO((x,y))
# a = imageField()
# a.setMode(2)