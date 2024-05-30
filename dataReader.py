import pandas as pd

class dataManager :
    def __init__(self):
        self.data = pd.read_excel("data.xlsx")
        self.header = list(self.data)
        
    def getHeader(self):
        return self.header
    
    def getDataByIndex(self, index):
        return list(self.data.loc[index])
