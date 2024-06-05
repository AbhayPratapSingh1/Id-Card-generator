import cv2
from buttonsSetUpClasses.fieldBox import fieldBox
from ImageHandlingClass.ImageField import imageField
from fontAndTextSetup.fontGenerate import Writer
from  M2.HandlerStaticFields import Handler

def nothing(self):
    pass

class DetailCollector(Handler):
    def __init__(self, data, backgroundImagePath, demoPhoto):
        super().__init__()
        self.data = data ## xslx headers
        self.fieldDetails = []

        self.backgroundPath = backgroundImagePath
        self.demoPhoto = demoPhoto

        self.currentField = -1
        self.fieldSelected = False

        self.LBtnDown = False

        self.mode = 1

        self.textWriter = Writer()
        self.imgField = imageField(path=self.demoPhoto)

        self.imgField.setMode(1) # mode 2 => circle  ||   1 => square   || 0 -> Natural
        self.loadBackground()   # to load and define the copy of the card image
        self.start()
        
    def start(self):
        self.runProgram = True
        self.CreateTrackbar()
        while self.runProgram:
            if self.currentField != -1:
                self.addDataInFieldBox()
            if self.imgField != -1:
                self.mergeField(self.imgField.image, h = self.imgField.y, h2=self.imgField.y2, w=self.imgField.x, w2=self.imgField.x2, to="img")
                
            self.showWindow() # showing the image
        cv2.destroyAllWindows()

    def loadBackground(self):
        self.base = cv2.imread(self.backgroundPath)
        self.img = self.base.copy()
    
    def CreateTrackbar(self):
        cv2.imshow("Handler",self.handler)        
        cv2.createTrackbar("R" , "Handler" , 0 , 255 , nothing )
        cv2.createTrackbar("G" , "Handler" , 0 , 255 , nothing )
        cv2.createTrackbar("B" , "Handler" , 0 , 255 , nothing )
        cv2.createTrackbar("FontSize" , "Handler" , 40 , 100 , nothing )

    def showWindow(self):
        
        cv2.imshow("Card",self.img)
        cv2.setMouseCallback("Handler",self.mouse_event_check_handler)
        cv2.setMouseCallback("Card",self.mouse_event_check_card)
        self.setTrackbars()
        if cv2.waitKey(1) == 27 :
            self.runProgram = False

    def setTrackbars(self):
        self.R = cv2.getTrackbarPos("R","Handler")
        self.G = cv2.getTrackbarPos("G","Handler")
        self.B = cv2.getTrackbarPos("B","Handler")
        self.fontSize =  cv2.getTrackbarPos("FontSize","Handler")

    def createFBoxes(self, box):
        cv2.rectangle(self.img , (box.x-1 , box.y-1) , (box.x2 , box.y2) ,(0,0,0) , 1)
        cv2.rectangle(self.img , (box.x-1 , box.y-11) , (box.x+10 , box.y-1) ,(0,0,0) , -1)
        cv2.rectangle(self.img , (box.x2 , box.y2) , (box.x2+5 , box.y2+5) ,(0,0,0) , -1)
    
    def mergeBorder(self, data):
        cv2.rectangle(self.base, (data["x"],data["y"]), (data["x1"], data["y1"]), (0,0,255), 1)
    
    def mergeField(self, image, h, h2, w, w2, to):
        if to == "img" :
            del self.img
            self.img = self.base.copy()
            if self.currentField != -1:
                self.createFBoxes(self.currentField)
            else:
                h,h2,w,w2 = self.sizeNormalise(self.imgField)
                self.createFBoxes(self.imgField)

            if self.currentField == -1 and self.imgField.isCircle :
                for i in range(0, h2-h):
                    for j in range(0,w2-w):
                        if not(image[i,j, 0] == 255 and image[i, j, 1] == 255 and  image[i,j, 2] == 255) :
                            self.img[h+i,w+j] = image[i,j]
                
            elif self.img[h:h2 , w : w2].shape == image.shape:
                self.img[h:h2 , w : w2] = image
            else:
                print("Image Out of Frame")
            
        elif to == "main":
            if self.currentField != -1:
                self.createFBoxes(self.currentField)
            else:
                h,h2,w,w2 = self.sizeNormalise(self.imgField)
                self.createFBoxes(self.imgField)

            if self.imgField != -1 and self.imgField.isCircle :
                for i in range(0, h2-h):
                    for j in range(0,w2-w):
                        if not(image[i,j, 0] == 255 and image[i, j, 1] == 255 and  image[i,j, 2] == 255) :
                            self.base[h+i,w+j] = image[i,j]
                
            elif self.base[h:h2 , w : w2].shape == image.shape:
                self.base[h:h2 , w : w2] = image
            else:
                print("size error")
            
    def sizeNormalise(self, subImg):
        h , w = subImg.y , subImg.x 
        h2, w2 = subImg.y2 , subImg.x2
        if subImg.x2 > self.base.shape[1]:
            w2 = self.base.shape[1]
        if subImg.y2 > self.base.shape[0]:
            h2 = self.base.shape[0]
        return h,h2,w,w2 
                
    def addDataInFieldBox(self, to = "img"):
        if self.currentField != -1:
            h,h2,w,w2 = self.sizeNormalise(self.currentField)    
            if h2 - h > 0 and w2 - w > 0 :
                textImageBase = self.base[h : h2 , w : w2]
                textImage = self.addFont(textImageBase, self.data[0])
                self.mergeField(textImage, h, h2, w, w2, to)

    def addFont(self, image, dataString):
        image = self.textWriter.writeLineS(image=image , fontSize=self.fontSize, text=dataString, color = (self.B, self.G, self.R) , mode=self.mode)
        return image
    
    def saveData(self):
        if self.currentField == -1:
            self.mergeField(self.imgField.image, h = self.imgField.y, h2=self.imgField.y2, w=self.imgField.x, w2=self.imgField.x2, to="main")
            self.fieldDetails.append( {"id":"Image" , "x":self.imgField.x , "x1" : self.imgField.x2 ,  "y":self.imgField.y , "y1" : self.imgField.y2, "h" :self.imgField.h , "w" : self.imgField.w , "mode": self.mode} )
            self.mode = 1
        else :
            self.addDataInFieldBox(to="main")
            self.fieldDetails.append( {"id":self.data[0] , "x":self.currentField.x , "x1" : self.currentField.x2 ,  "y":self.currentField.y , "y1" : self.currentField.y2, "h" :self.currentField.h , "w" : self.currentField.w , "r":self.R, "g":self.G, "b":self.B , "fontSize": self.fontSize, "mode": self.mode  } )
            self.currentField = -1
            self.mergeBorder(self.fieldDetails[-1])
            self.data.pop(0)

    def mouse_event_check_card(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            self.LBtnDown = True
            self.isField_Selected((x,y))
            if self.imgField != -1 :
                self.isImg_Selected((x,y))
            
        if event == cv2.EVENT_MOUSEMOVE:
            # check for if the dynamic field is selected and can be move in the window
            if self.LBtnDown and self.fieldSelected:
                if self.imgField == -1 :
                    self.currentField.action(self.toChange, (x,y))        
                    self.addDataInFieldBox()

                else :
                    self.imgField.action(self.toChange, (x,y))
                    # self.mergeField(self.imgField.image, h = self.imgField.y, h2=self.imgField.y2, w=self.imgField.w, w2=self.imgField.w2, to="img")


        
        if event==cv2.EVENT_LBUTTONUP:
            # set back the selected field since the mouse button is up now
            self.LBtnDown = False # this is unnecessary i guess
            self.fieldSelected = False
            self.toChange = -1
    
    def isImg_Selected(self, pos):
        selected = self.imgField.isSelected(pos)
        if selected != -1 :
            self.fieldSelected = True
            self.toChange = selected

    # used to check if the move box or the resize box of the field is pressed or not
    def isField_Selected(self, pos):
        if self.currentField != -1:
            selected = self.currentField.isSelect(pos)  # return -1 if box is not selected and 0 if move and 1 if dimension selected
            if selected != -1:
                self.fieldSelected = True
                self.toChange = selected

    def createFieldBox(self, x=30, y=30, h=40, w=100):
        self.currentField =  fieldBox(x=x, y=y, h=h, w=w, i = 1) # new object is created