import sys
from M2.IcardFieldDetailCollector import DetailCollector
from dataHandlerClass.dataReader import dataManager
from M2.CardGenerator import Generator
from M2.A4Generator import ToA4
from ImageHandlingClass.ImageToPdf import pdfCreate
try :
    ConstDataFile = open("User_Data_Place_Here/NameSetUp.txt", "r")
except:
    print("Either file is deleted or reaname of NameSetUp.txt check for its correction and try again")
    sys.exit(0)

allData = ConstDataFile.readlines()
ConstDataFile.close()
# print(allData)
ConstData = {}
for i in allData : 
    if not i.startswith("\n") and not i.startswith("#"):
        i = i[:-1] # removing \n
        i = i.replace(" ", "")
        i = i.replace("\"", "")
        each = i.split("=")
        if len(each) == 2:
            ConstData[each[0]] = each[1]
        else:
            input("Data file includes some error exiting program")
            sys.exit(0)

## Data Handler Data
dataHandler = dataManager(dataPath = f"User_Data_Place_Here/{ConstData["dataFileName"]}", ImageFolder = f"User_Data_Place_Here/{ConstData["photoFolder"]}", ImageColName=ConstData["PhotoColumn"], setTextCapital = ConstData["setTextCapital"])

header = [i for i in  dataHandler.getHeader()]
demoPhoto = dataHandler.getDemoImage()
createModel = DetailCollector(data = header, backgroundImagePath = f"User_Data_Place_Here/{ConstData["cardBackgroundImage"]}", demoPhoto = demoPhoto)
FieldDetail = createModel.fieldDetails
extension = dataHandler.ImageExtension
cardGenerate = Generator(dataHandler.data, FieldDetail, ConstData["PhotoColumn"], ImageFolder = f"User_Data_Place_Here/{ConstData["photoFolder"]}", ImageExtension=dataHandler.ImageExtension, backgroundImagePath=f"User_Data_Place_Here/{ConstData["cardBackgroundImage"]}")
imageName, inputPath = cardGenerate.getImgPath_Name()

# print(imageName)
# print(inputPath)

a4Generate = ToA4(ImageName=imageName, InputPath=inputPath, marginbetween=ConstData["MarginBetween"], marginBorder=ConstData["MarginBorder"])
createPdf = pdfCreate(pathToSave = "Output/Pdf/" , pathToLoad ="Output/A4/" , imagesList = a4Generate.getA4List())