import os
import pandas as pd

class dataManager :
    def __init__(self, dataPath, ImageFolder, ImageColName, setTextCapital = False):
        self.ImgFolder = ImageFolder
        self.ImgCol = ImageColName
        self.setDataCapital = setTextCapital
        self.data = pd.read_excel(dataPath)
        if self.data.empty:
            print("Data File Cannot be readed Exiting program fix the path for further")
        self.header = list(self.data)
        self.header.remove(self.ImgCol.upper())
        
    def getHeader(self):
        return self.header
    
    def getDataByIndex(self, index):
        return list(self.data.loc[index])
    
    def getDemoImage(self):
        photo = os.listdir(self.ImgFolder)
        self.ImageExtension = photo[0].split(".")[-1]
        return f"{self.ImgFolder}/{self.data.loc[0, self.ImgCol]}.{self.ImageExtension}"
