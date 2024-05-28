import cv2
import numpy as np
from button import button
class staticButtons:
    def __init__(self):
        self.staticButtons = {}
        self.Button()
        
    def Button(self , h = 50 , w= 50 , color = (0,0,255)):
        cross = self.crossButton()
        tick = self.tickButton()
        cross.x = 100 
        cross.y = 100
        cross.setPos((100,100))
        tick.setPos((100,200))
        self.staticButtons["cross"] = cross
        self.staticButtons["tick"] = tick

    class staticButton(button):
        def __init__(self , x = 50 , y = 50 , h = 50, w = 50 ):
            super().__init__(x=x, y=y, h=h, w=w)
            
        def isSelected(self,pos):
            if pos[0] >= self.x and pos[0] < self.x2 and pos[1] >= self.y and pos[1] < self.y2:
                return True
            return False
        
        def action(self):
            print("Action to be submited in each classes")

    class crossButton(staticButton):
        def __init__(self):
            super().__init__()
            self.img[:] = (0,0,255)
            cv2.rectangle(self.img, (0,0) , (self.w-1 , self.h-1) , (0,0,0), 2)
            self.createCross()
        
        def createCross(self):
            y,x,z = self.img.shape
            for i in range(y):
                for j in range(x):
                    if (i==j or i==x-j) and i>5 and i<y-5  :
                        self.img[i][j] = [0,0,0]
            
    class tickButton(staticButton):
        def __init__(self):
            super().__init__()
            self.img[:] = [0,255,0]
            self.createTick()

        def createTick(self):
            cv2.rectangle(self.img, (0,0) , (self.w-1 , self.h-1) , (0,0,0), 2)
            x,y,z = self.img.shape
            # creating the tick 
            # to be fix not fixed right now!
            for i in range(y):
                for j in range(x):
                    if (i > x/2 and j-5 == (i - x/2) and j< y/2) or (i>x/3 and i == x-j + 20 and i>5 and i<y-5):
                        self.img[i][j] = [0,0,0]
