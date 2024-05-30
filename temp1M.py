import cv2
import numpy as np
import sys
from buttonsSetUpClasses.fieldBox import fieldBox
from fontAndTextSetup.fontGenerate import Writer
from temp1b import Handler
from dataReader import dataManager

def nothing(temp):
    pass

class main(Handler):
    def __init__(self,data , image=None):
        self.data = data
        self.addedData = 0
        self.mainData = []
        super().__init__()
        self.runProgram = True
        # this is the main image other just used to add fields to the main image
        self.base = image
        # creation of the numpy array of the size equal to the 650(h)x1000(w) px since it can be fit in the screen ; 8bit unsigned int since it can hold value upto 255 only
        self.img = self.base.copy() # create copy of main base so not change when drag
        self.name = "Card" # name of the window of the image
        # stores the objects of the field that are created in future it is divided into two static and non static(dynamic)
        self.fields = []
        self.LeftMouseButtonDown = False
        # static buttons that are needed to be add like done or background , etc
        # remember it doesn't include dynamic field buttons which are used to fix each element in the windows
        self.currentField = -1
        self.toChangeField = -1
        self.fontSize = 10
        self.changeFont = False
        self.setFontInField = True
        self.mode = 1
        self.fieldSelected = False
        
        # writer for writing the text in the field box
        self.textWriter = Writer()
        cv2.imshow("Handler",self.handler)
        self.trackbar()
        while self.runProgram:
            self.showWindow() # showing the image
        cv2.destroyAllWindows()
    
    # display the window with the callback functions
    def showWindow(self): 
        self.copyFontInField()
        cv2.imshow(self.name,self.img)
        cv2.imshow("Handler",self.handler)
        cv2.setMouseCallback("Handler",self.mouse_event_check_handler)
        cv2.setMouseCallback(self.name,self.mouse_event_check_card)

        # self.R = 0
        # self.G = 0
        # self.B = 0
        self.R = cv2.getTrackbarPos("R","Handler")# 0 means up
        self.G = cv2.getTrackbarPos("G","Handler")# 0 means up
        self.B = cv2.getTrackbarPos("B","Handler")# 0 means up
        self.fontSize =  cv2.getTrackbarPos("FontSize","Handler")# 0 means up

        # self.checkFontChange()
        if cv2.waitKey(1) == 27 :
            self.runProgram = False
    
    # def checkFontChange(self):
    #     if self.PR - self.R != 0 or self.PB - self.B != 0 or self.PG - self.G != 0 or self.PFontSize - self.PFontSize != 0 :
    #         self.changeFont = True
    #         print("chande")
        

    def trackbar(self):
        cv2.createTrackbar("R" , "Handler" , 0 , 255 , nothing )
        cv2.createTrackbar("G" , "Handler" , 0 , 255 , nothing )
        cv2.createTrackbar("B" , "Handler" , 0 , 255 , nothing )
        cv2.createTrackbar("FontSize" , "Handler" , 1 , 100 , nothing )


    def mergeToBase(self, data):
        cv2.rectangle(self.base, (data["x"],data["y"]), (data["x1"], data["y1"]), (0,0,255), 1)
        pass

    def mergeFieldToImg(self, image, h, h2, w, w2, to="main"):
        if to == "temp" :
            self.img[h:h2 , w : w2] = image
        elif to == "main":
            print("yse")
            self.base[h:h2 , w : w2] = image
        pass

    def createFieldBox(self, x=30, y=30, h=40, w=100):
        self.addedData += 1
        self.currentField =  fieldBox(x=x, y=y, h=h, w=w, i = len(self.fields)+1) # new object is creted 
    
    def setFieldBoxesInWindow(self):
        del self.img
        self.img = self.base.copy()
        if self.currentField != -1:
            # creating boxes for self.currentField field present in the field list
            cv2.rectangle(self.img , (self.currentField.x , self.currentField.y) , (self.currentField.x2 , self.currentField.y2) ,(0,0,0) , 1)
            cv2.rectangle(self.img , (self.currentField.x , self.currentField.y-10) , (self.currentField.x+10 , self.currentField.y) ,(0,0,0) , -1)
            cv2.rectangle(self.img , (self.currentField.x2 , self.currentField.y2) , (self.currentField.x2+5 , self.currentField.y2+5) ,(0,0,0) , -1)
    
    def copyFontInField(self, to = "temp"):
        if self.currentField != -1 and self.setFontInField:
            h , w = self.currentField.y + 1, self.currentField.x + 1
            h2, w2 = self.currentField.y2 , self.currentField.x2

            if self.currentField.x2 > self.base.shape[1]:
                w2 = self.base.shape[1]
            if self.currentField.y2 > self.base.shape[0]:
                h2 = self.base.shape[0]
            if h2 - h > 0 and w2 - w > 0 :
                textImage = self.base[h : h2 , w : w2]
                if len(self.data) == len(self.mainData): return
                textImage = self.addFont(textImage, self.data[len(self.mainData)])
                self.mergeFieldToImg(textImage, h, h2, w, w2, to)
        

        
    def addFont(self, image, dataString):
        image = self.textWriter.writeLineS(image=image , fontSize=self.fontSize, text=dataString, color = (self.B, self.G, self.R) , mode=self.mode)
        return image
        
    # used to check if the move box or the resize box of the field is pressed or not
    def checkIfFieldIsSelected(self, pos):
        if self.currentField != -1:
            selected = self.currentField.isSelect(pos)  # return -1 if box is not selected and 0 if move and 1 if dimension selected
            if selected != -1:
                self.fieldSelected = True
                self.toChangeField = selected
        
    def mouse_event_check_card(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            self.LeftMouseButtonDown = True
            self.checkIfFieldIsSelected((x,y))
            
        if event == cv2.EVENT_MOUSEMOVE:
            # check for if the dynamic field is selected and can be move in the window
            if self.LeftMouseButtonDown and self.fieldSelected:
                self.currentField.action(self.toChangeField, (x,y))        
                self.setFieldBoxesInWindow()
        
        if event==cv2.EVENT_LBUTTONUP:
            # set back the selected field since the mouse button is up now
            self.LeftMouseButtonDown = False
            self.fieldSelected = False
            self.toChangeField = -1

    def saveData(self):
        if self.currentField == -1:
            pass
        else :
            self.copyFontInField(to="main")
            self.mainData.append( {"id":self.data[len(self.mainData)] ,  "x":self.currentField.x , "x1" : self.currentField.x2 ,  "y":self.currentField.y , "y1" : self.currentField.y2, "h" :self.currentField.h , "w" : self.currentField.w , "r":self.R, "g":self.G, "b":self.B , "fontSize": self.fontSize  } )
            self.currentField = -1
            self.mergeToBase(self.mainData[-1])

    # used to check if the static button is pressed or not
    def checkIfStaticButtonIsSelected(self, pos):
        for each in self.staticButtons:
            selected = self.staticButtons[each].isSelected(pos)  # return -1 if box is not selected and 0 if move and 1 if dimension selected
            if selected:
                # print(f"button '{each}' is pressed")
                if each == "next":
                    if self.addedData == len(self.data):
                        self.saveData()
                        self.runProgram = False
                        
                    else :
                        self.saveData()
                        self.createFieldBox()
                        self.setFieldBoxesInWindow()
                        
                elif each == "l":
                    self.mode = 1                    
                
                elif each == "b":
                    self.mode = 2

                elif each == "r":
                    self.mode = 3

                elif each == "c":
                    self.mode = 4

    def setFont(self):
        pos = self.staticButtons["size"].pos
        height, width = self.staticButtons["size"].h , self.staticButtons["size"].w 
        self.staticButtons.pop("size")
        self.staticButtons["size"] = self.createButton(str(self.fontSize), w=width , h= height , color=(100,100,100),pos=(pos), fontSize=12)
        self.mergeStaticButtons()
        pass

dataHandler = dataManager()
header = dataHandler.getHeader()
image = cv2.imread("background.jpg")
size = [400, 500]
a = main(data=header , image= image)
cv2.imshow("Final Card Image", a.base)
cv2.waitKey(0)

print( a.mainData)
print(len(a.mainData))