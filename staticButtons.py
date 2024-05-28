import numpy as np
class staticButtons:
    def __init__(self):
        self.staticButtons = []
        self.Button()
        
    def Button(self , h = 50 , w= 50 , color = (0,0,255)):
        cross = self.crossButton()
        tick = self.tickButton()
        self.staticButtons.append(cross)
        self.staticButtons.append(tick)
    
    class button:
        def __init__(self , x = 50 , y = 50 , h = 50, w = 50 ):
            self.x = x
            self.y = y
            self.h = h
            self.w = w 
            self.img = np.zeros([y,x,3] , dtype=np.uint8)
            
    class crossButton(button):
        def __init__(self):
            super().__init__()
            self.img[:] = (0,0,255)
            self.createCross()
        
        def createCross(self):
            y,x,z = self.img.shape
            for i in range(y):
                for j in range(x):
                    if (i==j or i==x-j) and i>5 and i<y-5  :
                        self.img[i][j] = [0,0,0]
            
    class tickButton(button):
        def __init__(self):
            super().__init__()
            self.createTick()

        def createTick(self):
            self.img[:] = [0,255,0]
            x,y,z = self.img.shape
            # creating the tick 
            # to be fix not fixed right now!
            for i in range(y):
                for j in range(x):
                    if (i > x/2 and j-5 == (i - x/2) and j< y/2) or (i>x/3 and i == x-j + 20 and i>5 and i<y-5):
                        self.img[i][j] = [0,0,0]
