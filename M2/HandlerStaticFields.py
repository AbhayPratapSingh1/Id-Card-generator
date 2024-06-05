# temp 2 is responsible for the handler window in the program
import numpy as np
import cv2
import sys
from buttonsSetUpClasses.staticButtons import staticButtons

class Handler(staticButtons):
    def __init__(self):
        super().__init__()
        self.handler = np.full((600 , 600 , 3),255,dtype = np.uint8)
        self.mergeStaticButtons()

    def mergeStaticButtons(self):
        for i,each in enumerate(self.staticButtons):
            try :
                self.handler[self.staticButtons[each].y : self.staticButtons[each].y + self.staticButtons[each].h , self.staticButtons[each].x : self.staticButtons[each].x + self.staticButtons[each].w ] = self.staticButtons[each].img
            except Exception as e:
                print("_"*100,"\nPlease Resolve error in the tempb-> mergeStaticButtons() :")
                print(e)
                print(f"object index is {i}\n{"_"*100}")
                sys.exit(0)
    
    
    def checkIfStaticButtonIsSelected(self, pos):
        for each in self.staticButtons:
            selected = self.staticButtons[each].isSelected(pos)  # return -1 if box is not selected and 0 if move and 1 if dimension selected
            if selected:
                if each == "next":
                    if len(self.data) == 1 :
                        self.saveData()
                        self.runProgram = False
                    else :
                        self.saveData()
                        self.createFieldBox()
                    if self.imgField != -1 :
                        self.imgField = -1
                        
                elif each == "l":
                    if self.imgField == -1:
                        self.mode = 1
                        self.staticButtons["textToggler"].setPos((345,45))
                        self.mergeStaticButtons()
                        cv2.imshow("Handler", self.handler)
                        
                        
                elif each == "c":
                    if self.imgField == -1:
                        self.mode = 2
                        self.staticButtons["textToggler"].setPos((375,45))
                        self.mergeStaticButtons()
                        cv2.imshow("Handler", self.handler)
                        
                elif each == "r":
                    if self.imgField == -1:
                        self.mode = 3
                        self.staticButtons["textToggler"].setPos((405,45))
                        self.mergeStaticButtons()
                        cv2.imshow("Handler", self.handler)
                
                elif each == "circle":
                    if self.imgField != -1:
                        self.mode = 3
                        self.staticButtons["ImgToggler"].setPos((560,110))
                        self.imgField.setMode(self.mode)
                        self.mergeStaticButtons()
                        cv2.imshow("Handler", self.handler)
                
                elif each == "square":
                    if self.imgField != -1:
                        self.mode = 2
                        self.staticButtons["ImgToggler"].setPos((560,60))
                        self.imgField.setMode(self.mode)
                        self.mergeStaticButtons()
                        cv2.imshow("Handler", self.handler)
                
                elif each == "rectangle":
                    if self.imgField != -1:
                        self.mode = 1
                        self.staticButtons["ImgToggler"].setPos((560,10))
                        self.imgField.setMode(self.mode)
                        self.mergeStaticButtons()
                        cv2.imshow("Handler", self.handler)
                    
                elif each == "toggle Ratio":
                    if self.imgField != -1:
                        self.mode = 4
                        self.imgField.setMode(self.mode)
                        if self.imgField.inRatio :
                            self.staticButtons["ratioToggler"].setPos((545,185))
                        else :
                            self.staticButtons["ratioToggler"].setPos((505,185))
                        
                        self.mergeStaticButtons()
                        cv2.imshow("Handler", self.handler)


    def mouse_event_check_handler(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            self.checkIfStaticButtonIsSelected((x,y))