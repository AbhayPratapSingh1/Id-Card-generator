import pandas as pd

class dataManager :
    def __init__(self, data):
        self.path = data
        self.data = pd.read_excel(data)
        self.header = list(self.data)
        
    def getHeader(self):
        return self.header
    
    def getDataByIndex(self, index):
        return list(self.data.loc[index])
