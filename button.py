import numpy as np

class button:
    def __init__(self , x = 50 , y = 50 , h = 50, w = 50 ):
        self.x = x # x cordinate
        self.y = y # y cordinate
        self.h = h # heigth
        self.w = w # width
        self.x2 = x + w # x final cordinate
        self.y2 = y + h # y final cordinate
        self.img = np.zeros([y,x,3] , dtype=np.uint8) # image of the size mentioned
    
    # responsible for changing the position of the object
    def setPos(self, pos):
        self.x = pos[0] # change pos
        self.y = pos[1]
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h