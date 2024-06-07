import cv2
import numpy as np
from buttonsSetUpClasses.button import button
from fontAndTextSetup.fontGenerate import Writer

class staticButtons:
    def __init__(self):
        self.staticButtons = {}
        self.Button()
        
    def Button(self ):

        temp = self.createButton("Next Field", pos=(200,100), w=150, mode=4, fontSize= 25)
        self.staticButtons["next"] = temp
        
        temp = self.createButton("Up", pos=(500,400), w=80, mode=4, fontSize= 25)
        self.staticButtons["up"] = temp
        temp = self.createButton("down", pos=(500,460), w=80, mode=4, fontSize= 25)
        self.staticButtons["down"] = temp

        temp = self.createButton("Rectangle Img",pos=(450,0), mode=4,w=100, fontSize= 15)
        self.staticButtons["rectangle"] = temp
        temp = self.createButton("Square Img",pos=(450,50), mode=4,w=100, fontSize= 15)
        self.staticButtons["square"] = temp
        temp = self.createButton("Circle Img",pos=(450,100), w=100, mode=4, fontSize= 15)
        self.staticButtons["circle"] = temp
        temp = self.createButton(" ",pos=(555,0), color=(200,200,0), mode=4, w=40, h=150, fontSize= 15)
        self.staticButtons["toggle Image"] = temp
        temp = self.createButton("X",pos=(560,10), color=(20,20,140), mode=4, w=30, h=30, fontSize= 15)
        self.staticButtons["ImgToggler"] = temp
        


        temp = self.createButton("Img in Ratio :",pos=(300,180), color=(255,250,255), mode=4,w=200, fontSize= 20 , border=(255,255,255))
        self.staticButtons["description of in Ratio"] = temp
        temp = self.createButton(" ",pos=(500,180), color=(200,200,0), mode=4, w=80, h=40, fontSize= 15)
        self.staticButtons["toggle Ratio"] = temp
        temp = self.createButton("X",pos=(545,185), color=(20,20,140), mode=4,w=30, h=30, fontSize= 15)
        self.staticButtons["ratioToggler"] = temp

        

        temp = self.createButton("L",pos=(340,0), h=30 , w=30, fontSize=12)
        self.staticButtons["l"] = temp
        temp = self.createButton("C",pos=(370, 0), h=30 , w=30, fontSize=12)
        self.staticButtons["c"] = temp
        temp = self.createButton("R",pos=(400, 0),  h=30 , w=30, fontSize=12)
        self.staticButtons["r"] = temp
        temp = self.createButton(" ",pos=(340,40), color=(200,200,0), mode=4, w=90, h=30, fontSize= 15)
        self.staticButtons["toggle text"] = temp
        temp = self.createButton("X",pos=(345,45), color=(20,20,140), mode=4,w=20, h=20, fontSize= 13)
        self.staticButtons["textToggler"] = temp



        # temp = self.createButton("C", color=(100,100,100),pos=(370, 60),  h=30 , w=30, fontSize=12)
        # self.staticButtons["c"] = temp

        pass

    def createButton(self, text=" ", h = 50 , w = 50 , color = (0,200,0), pos=(0,0), fontColor=(0, 0, 0), fontSize=20, mode=4, border= (0,0,0)):
        next = self.staticButton( h = h , w = w)
        next.bgColor(color=color, border= border)
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

        def bgColor(self, color, border):
            self.img[:] = color
            cv2.rectangle(self.img, (0,0) , (self.w-1 , self.h-1) , border, 2)
        
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
            