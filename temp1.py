import cv2
import numpy as np
import sys
from buttonsSetUpClasses.staticButtons import staticButtons
from buttonsSetUpClasses.fieldBox import fieldBox
from fontAndTextSetup.fontGenerate import Writer

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

        # self.writeInTheField()
        # writer for writing the text in the field box
        self.textWriter = Writer()


        # merging the Field box with the window
        self.setFieldBoxesInWindow()
        while self.runProgram:
            self.showWindow() # showing the image
    
    def placeNewFieldBox(self,text = "This is the text in the text box "):
        self.createFieldBox(h=50, w=100, x=30, y=50)
        
        pass

    # this is responsible for the merging the static buttons created in the web pages
    def mergeStaticButtons(self):
        for i,each in enumerate(self.staticButtons):
            try :
                self.base[self.staticButtons[each].y : self.staticButtons[each].y + self.staticButtons[each].h , self.staticButtons[each].x : self.staticButtons[each].x + self.staticButtons[each].w ] = self.staticButtons[each].img
            except Exception as e:
                print("_"*100,"\nPlease Resolve error in the window -> mergeStaticButtons() :")
                print(e)
                print(f"object index is {i}\n{"_"*100}")
                sys.exit(0)
    
    # font and font size neeed to be add in the future
    def writeInTheField(self, fieldId = 0, text= "hwllo world"):
        print("ues")
        x, y, h, w = self.fields[0].x , self.fields[0].y , self.fields[0].h , self.fields[0].w
        print(x,y,h,w)
        # image = self.base[x: x+ w , y: y+h]
        # print(image.shape)
        # cv2.imshow("om,age", image)
        # cv2.waitKey(0)
        pass

    def createFieldBox(self, x=0, y=0, h=100, w=100):
        self.fields.append(fieldBox(x=x, y=y, h=h, w=w, i= len(self.fields)+1)) # new object is creted and added to the field list
    
    def setFieldBoxesInWindow(self):
        for i, each in enumerate(self.fields):
            # creating boxes for each field present in the field list
            cv2.rectangle(self.img , (each.x , each.y) , (each.x2 , each.y2) ,(0,0,0) , 1)
            cv2.rectangle(self.img , (each.x , each.y-10) , (each.x+10 , each.y) ,(0,0,0) , -1)
            cv2.rectangle(self.img , (each.x2 , each.y2) , (each.x2+5 , each.y2+5) ,(0,0,0) , -1)
            # self.writeInTheField(i, "")
    
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

    def mergeFields(self):

        pass
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
                # self.mergeFields()
                # print(self.fields[0].x , self.fields[0].y)
                self.setFieldBoxesInWindow()
        
        if event==cv2.EVENT_LBUTTONUP:
            # set back the selected field since the mouse button is up now
            self.selectedFieldBox[0] = -1
            self.LeftMouseButtonDown = False

a = window()
