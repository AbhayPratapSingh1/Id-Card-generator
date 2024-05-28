import cv2
import numpy as np
import sys
from staticButtons import staticButtons
from button import button

class fieldBox(button):
    def __init__(self, x=0, y=0, h=100, w=100):
        super().__init__( x = x , y = y , h = h , w = w )

    # responsible for changing dimention according to the (mouseWX) pos
    def setDimension(self, pos):
        self.w = pos[0] - self.x
        self.h = pos[1] - self.y
        if self.w<0 :
            self.w = self.x
            self.x = pos[0]
        if self.h<0 :
            self.h = self.y
            self.y = pos[1]
        self.x2 = pos[0]
        self.y2 = pos[1]
    
    # this will check if the object is in the dimension Position change area return true or false
    def isSelect(self, pos):
        # to set bewteen the box of field of 20 X 20 above the left most top corner
        if (pos[0] > self.x) and (pos[0] < self.x+10) and (pos[1] > self.y-10) and (pos[1] < self.y) :
            return 0
        elif (pos[0] > self.x + self.w ) and (pos[0] < self.x + self.w +5) and (pos[1] > self.y + self.h) and (pos[1] < self.y+self.w+5) :
            return 1
        return -1
    
    # this resposible for changing the dimension and the position of the field box
    def action(self, type , pos):
        if type == 0 :
            self.setPos(pos)
        elif type == 1:
            self.setDimension(pos)            

class window(staticButtons):
    def __init__(self):
        super().__init__()
        self.runProgram = True
        # creation of the numpy array of the size equal to the 650(h)x1000(w) px since it can be fit in the screen ; 8bit unsigned int since it can hold value upto 255 only
        self.base = np.full((650 , 1000 , 3),255,dtype = np.uint8)
        self.mergeStaticButtons()
        self.img = self.base.copy() # create copy of main base so not change when drag
        self.name = "temperary" # name of the window of the image
        # stores the objects of the field that are created in future it is divided into two static and non static(dynamic)
        self.fields = []
        self.LeftMouseButtonDown = False
        # static buttons that are needed to be add like done or background , etc
        # remember it doesn't include dynamic field buttons which are used to fix each element in the windows
        self.selectedFieldBox = [-1, -1] # this tell which Field box is selected and the move/dimension of it is selected if the mouse button is down
        self.createFieldBox( h=50, w=100 , x= 30 , y =50)
        self.createFieldBox( h=50, w=50 , x= 500 , y =50)

        # merging the Field box with the window
        self.setFieldBoxesInWindow()
        while self.runProgram:
            self.showWindow() # showing the image
    
    def mergeStaticButtons(self):
        for i,each in enumerate(self.staticButtons):
            try :
                self.base[self.staticButtons[each].y : self.staticButtons[each].y + self.staticButtons[each].h , self.staticButtons[each].x : self.staticButtons[each].x + self.staticButtons[each].w ] = self.staticButtons[each].img
            except Exception as e:
                print("_"*100,"\nPlease Resolve error in the window -> mergeStaticButtons() :")
                print(e)
                print(f"object index is {i}\n{"_"*100}")
                sys.exit(0)
        

    def createFieldBox(self, x=0, y=0, h=100, w=100):
        self.fields.append(fieldBox(x=x, y=y, h=h, w=w)) # new object is creted and added to the field list
    
    def setFieldBoxesInWindow(self):
        for i, each in enumerate(self.fields):
            # creating boxes for each field present in the field list
            cv2.rectangle(self.img , (each.x , each.y) , (each.x2 , each.y2) ,(0,0,0) , 1)
            cv2.rectangle(self.img , (each.x , each.y-10) , (each.x+10 , each.y) ,(0,0,0) , -1)
            cv2.rectangle(self.img , (each.x2 , each.y2) , (each.x2+5 , each.y2+5) ,(0,0,0) , -1)

    
    # display the window with the callback functions
    def showWindow(self): 
        cv2.imshow(self.name,self.img)
        cv2.setMouseCallback(self.name,self.mouse_event_check)
        if cv2.waitKey(1) == 27 :
            self.runProgram = False
        
    
    # used to check if the move box or the resize box of the field is pressed or not
    def checkIfFieldIsSelected(self, pos):
        for i, each in enumerate(self.fields):
            selected = each.isSelect(pos)  # return -1 if box is not selected and 0 if move and 1 if dimension selected
            if selected != -1:
                self.selectedFieldBox[0] = i
                self.selectedFieldBox[1] = selected # 0 for the posChange and 1 for the dimensionChange
                break
    # used to check if the static button is pressed or not
    def checkIfStaticButtonIsSelected(self, pos):
        for i, each in enumerate(self.staticButtons):
            selected = self.staticButtons[each].isSelected(pos)  # return -1 if box is not selected and 0 if move and 1 if dimension selected
            if selected:
                print(f"button {i} is pressed")
                self.staticButtons[each].action()

    # callbackFunctions for the mouce in the window
    def mouse_event_check(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            self.LeftMouseButtonDown = True
            self.checkIfFieldIsSelected((x,y))
            self.checkIfStaticButtonIsSelected((x,y))
            pass
        
        if event == cv2.EVENT_MOUSEMOVE:
            # check for if the dynamic field is selected and can be move in the window
            if self.LeftMouseButtonDown and self.selectedFieldBox[0] != -1:
                self.fields[self.selectedFieldBox[0]].action(self.selectedFieldBox[1], (x,y))
                del self.img
                self.img = self.base.copy()
                print(self.fields[0].x , self.fields[0].y)
                self.setFieldBoxesInWindow()
        
        if event==cv2.EVENT_LBUTTONUP:
            # set back the selected field since the mouse button is up now
            self.selectedFieldBox[0] = -1
            self.LeftMouseButtonDown = False

a = window()

