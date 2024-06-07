import cv2
import numpy as np
import sys
class ToA4:
    def __init__(self, ImageName, InputPath, marginBorder, marginbetween):
        self.marginBorder = self.mmTOpx(marginBorder)
        self.marginBetween = self.mmTOpx(marginbetween)
        self.inputPath = InputPath
        self.imageName = ImageName
        self.outputPath = "Output/A4/"
        self.A4No = 1
        self.A4List = []
        self.createAllA4()

    def getA4List(self):
        return self.A4List

    def createAllA4(self):
        for i in range(0,len(self.imageName),10):
            imageList = []
            if len(self.imageName) - i < 10 :
                for j in range(i, len(self.imageName)):
                    imageList.append(self.loadImage(j))
            else :
                for j in range(i, i+10):
                    imageList.append(self.loadImage(j))
            self.createOne(imageList)
            
    def createOne(self, imageList):
        
        A4 = np.full((3508 , 2480 , 3),255,dtype = np.uint8)
        imgNo = 0
        border = self.marginBorder 
        margin = self.marginBetween
        h = imageList[0].shape[0]
        w = imageList[0].shape[1]
        Ygap = margin + h 
        Xgap = margin + w

        for i in range(0, 2):
            for j in range(0, 5):
                if imgNo == len(imageList) :
                    break
                A4[ Ygap*j + border : Ygap*j + h + border , Xgap*i + border : Xgap*i + w + border ] = imageList[imgNo]
                imgNo += 1

        self.saveA4(A4)
                
    def saveA4(self, image):
        cv2.imwrite(f"{self.outputPath}{self.A4No}.png",image)
        self.A4List.append(f"{self.A4No}.png")
        self.A4No += 1

    def loadImage(self, i):
        image = cv2.imread(f"{self.inputPath}{self.imageName[i]}.jpg")
        if not isinstance(image, np.ndarray):
            print("\n"*2, "*"*100,"\n\n")
            print("Card Images Doesn't Found please fix the code or check if card images not created or deleted")
            print("\n"*2, "*"*100)
            input()
            sys.exit(0)
        return image
    
    def mmTOpx(self, mm):
        return int(float(mm)*11.8)