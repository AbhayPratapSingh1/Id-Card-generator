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
        pass

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
                print(f"button {each} is pressed")
                if each == "add":
                    pass
                elif each == "next":
                    self.saveData()
                    self.createFieldBox()
                    self.setFieldBoxesInWindow()
                    pass
                elif each == "done":
                    # this will store the details of the field in the files or the memory for the future use
                    self.saveData()
                    pass
    
    
    def mouse_event_check_handler(self,event,x,y,flag,param):
        if event==cv2.EVENT_LBUTTONDOWN:
            self.checkIfStaticButtonIsSelected((x,y))
    
    
# a = Handler()