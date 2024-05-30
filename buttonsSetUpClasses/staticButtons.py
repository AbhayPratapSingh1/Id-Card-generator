import cv2
import numpy as np
from buttonsSetUpClasses.button import button
from fontAndTextSetup.fontGenerate import Writer

class staticButtons:
    def __init__(self):
        self.staticButtons = {}
        self.Button()
        
    def Button(self ):
        temp = self.createButton("Next")
        self.staticButtons["next"] = temp
        
        temp = self.createButton("Add Font",pos=(200,0), mode=2)
        self.staticButtons["addFont"] = temp
        

        temp = self.createButton("L",pos=(490,0), h=30 , w=30, fontSize=12)
        self.staticButtons["l"] = temp

        temp = self.createButton("B",pos=(520, 0), h=30 , w=30, fontSize=12)
        self.staticButtons["b"] = temp

        temp = self.createButton("R",pos=(550, 0),  h=30 , w=30, fontSize=12)
        self.staticButtons["r"] = temp

        temp = self.createButton("C", color=(100,100,100),pos=(550, 40),  h=30 , w=30, fontSize=12)
        self.staticButtons["c"] = temp

        pass

    def createButton(self, text=" ", h = 50 , w = 50 , color = (0,200,0), pos=(0,0), fontColor=(0, 0, 0), fontSize=20, mode=4):
        next = self.staticButton( h = h , w = w)
        next.bgColor(color=color)
        next.write(text, fontColor, fontSize, mode )
        next.setPos(pos)
        return next
    
    class staticButton(button):
        def __init__(self , x = 50 , y = 50 , h = 50, w = 50 ):
            super().__init__(x=x, y=y, h=h, w=w)
            
            
        def isSelected(self,pos):
            if pos[0] >= self.x and pos[0] < self.x2 and pos[1] >= self.y and pos[1] < self.y2:
                return True
            return False
        
        def action(self):
            print("Action to be submited in each classes")

        def write(self, text, fontColor=(0, 0, 0), fontSize=20, mode=4):
            writer = Writer()
            self.img = writer.writeLineS(self.img, fontSize=fontSize, text=text, mode=mode)

        def bgColor(self, color):
            self.img[:] = color
            cv2.rectangle(self.img, (0,0) , (self.w-1 , self.h-1) , (0,0,0), 2)
        
    # class addButton(staticButton):
    #     def __init__(self):
    #         super().__init__()
    #         self.write("ADD")
        
            
    # class doneButton(staticButton):
    #     def __init__(self):
    #         super().__init__()
    #         self.img[:] = [0,255,0]
    #         cv2.rectangle(self.img, (0,0) , (self.w-1 , self.h-1) , (0,0,0), 2)
    #         self.write("Done")

    #     def writeDone(self):
    #         cv2.rectangle(self.img, (0,0) , (self.w-1 , self.h-1) , (0,0,0), 2)
    #         x,y,z = self.img.shape
            