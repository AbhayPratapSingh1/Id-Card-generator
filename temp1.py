import cv2
import numpy as np

from staticButtons import staticButtons

class box:
    def __init__(self, x=0, y=0, h=100, w=100):
        self.x = x # x cordinate
        self.y = y # y cordinate
        self.h = h # heigth
        self.w = w # width
        self.x2 = x + w # x final cordinate
        self.y2 = y + h # y final cordinate

    # responsible for changing position according to the (mouse) pos
    def setPos(self, pos):
        self.x = pos[0] # change pos
        self.y = pos[1]
        self.x2 = self.x + self.w
        self.y2 = self.y + self.h
    
    # responsible for changing dimention according to the (mouse) pos
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
    def change(self, type , pos):
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
        self.img = self.base.copy() # create copy of main base so not change when drag
        self.name = "temperary" # name of the window of the image
        # stores the objects of the field that are created in future it is divided into two static and non static(dynamic)
        self.fields = []
        self.LeftMouseButtonDown = False
        # static buttons that are needed to be add like done or background , etc
        # remember it doesn't include dynamic field buttons which are used to fix each element in the windows
        self.mergeStaticButtons()
        self.selectedFieldBox = [-1, -1] # this tell which Field box is selected and the move/dimension of it is selected if the mouse button is down
        self.createFieldBox( h=50, w=100 , x= 30 , y =50)
        self.createFieldBox( h=50, w=50 , x= 500 , y =50)
        # self.createFieldBox(w=200)
        # self.createFieldBox(h=500)
        # self.createFieldBox(w=200 , h=400)
        # self.createFieldBox(x=10,y=10)

        # merging the Field box with the window
        self.setFieldBoxesInWindow()
        # while self.runProgram:
            # self.showWindow() # showing the image
    
    def mergeStaticButtons(self):
        for i,each in enumerate(self.staticButtons):
            cv2.imshow(str(i), each.img)
            cv2.waitKey(0)
    def createFieldBox(self, x=0, y=0, h=100, w=100):
        self.fields.append(box(x=x, y=y, h=h, w=w)) # new object is creted and added to the field list
    
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
                print(selected)
                break

    # callbackFunctions for the mouce in the window
    def mouse_event_check(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            print("down")
            self.LeftMouseButtonDown = True
            self.checkIfFieldIsSelected((x,y))
            pass
        
        if event == cv2.EVENT_MOUSEMOVE:
            # check for if the dynamic field is selected and can be move in the window
            if self.LeftMouseButtonDown and self.selectedFieldBox[0] != -1:
                self.fields[self.selectedFieldBox[0]].change(self.selectedFieldBox[1], (x,y))
                del self.img
                self.img = self.base.copy()
                print(self.fields[0].x , self.fields[0].y)
                self.setFieldBoxesInWindow()
        
        if event==cv2.EVENT_LBUTTONUP:

            # set back the selected field since the mouse button is up now
            self.selectedFieldBox[0] = -1
            self.LeftMouseButtonDown = False
            print("up")

a = window()

