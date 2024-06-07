import os
import pandas as pd
import datetime
import sys
def typeCast(value):
    pass
    
class dataManager :
    def __init__(self, dataPath, ImageFolder, ImageColName, setTextCapital = False):
        self.ImgFolder = ImageFolder
        self.ImgCol = ImageColName
        self.setDataCapital = setTextCapital
        self.data = pd.read_excel(dataPath)
        self.data.fillna(" ", inplace=True)
        if self.data.empty:
            print("Data File Cannot be readed Exiting program fix the path for further")
            input()
            sys.exit(0)
        for i in self.data.columns:
            is_datetime = pd.api.types.is_datetime64_any_dtype(self.data[i])
            is_str = pd.api.types.is_string_dtype(self.data[i])

            if is_datetime:
                self.data[i] = self.data[i].apply(lambda x: x.strftime('%Y-%m-%d'))
                if isinstance(i, (pd.Timestamp, datetime.datetime)):
                    self.data.rename(columns={i: i.strftime('%Y-%m-%d')}, inplace=True)
                is_str = True
            if not is_str:
                # print(eval("hello"))
                self.data[i] = self.data[i].apply(lambda x: str(self.infer_type(x)))
                self.data.rename(columns={i: str(self.infer_type(i))}, inplace=True)
        self.header = list(self.data)
        self.header.remove(self.ImgCol)

    def infer_type(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            pass
        try:
            return float(value)
        except (ValueError, TypeError):
            pass
        if isinstance(value, str) and value.lower() in ['true', 'false']:
            return value.lower() == 'true'
        return value            
    
    def getHeader(self):
        return self.header
    
    def getDataByIndex(self, index):
        return list(self.data.loc[index])
    
    def getDemoImage(self):
        photo = os.listdir(self.ImgFolder)
        self.ImageExtension = photo[0].split(".")[-1]
        return f"{self.ImgFolder}/{self.data.loc[0, self.ImgCol]}.{self.ImageExtension}"
