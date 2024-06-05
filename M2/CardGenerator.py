import cv2
from ImageHandlingClass.ImageField import imageField 
from fontAndTextSetup.fontGenerate import Writer
class Generator:

    def __init__(self, dataFrame, fieldDetail, ImageCol, ImageFolder, ImageExtension, backgroundImagePath):
        self.backgroundImagePath = backgroundImagePath
        self.ImageExtension = ImageExtension
        self.ImageCol = ImageCol
        self.ImageFolder = ImageFolder
        self.savePath = "Output/Cards/"
        self.dataFrame = dataFrame
        self.fieldDetail = fieldDetail
        self.images = self.dataFrame[self.ImageCol].tolist()
        print(self.images)
        self.writer = Writer()
        self.createAll()

    def createAll(self):
        
        for i in range(len(self.dataFrame)):
            # sending each row data for the creating the card
            # image = cv2.imread(f"{self.ImageFolder}/{self.images[i]}.{self.ImageExtension}")
            self.createOne(dict(self.dataFrame.loc[i]), imageName=f"{self.images[i]}",extension=f"{self.ImageExtension}")

    def getDataFromRowDict(self, dic, key):
        for each in dic:
            if each.upper() == key.upper():
                return dic[each]
    def createOne(self, data, imageName, extension):
        # Loading the background Image
        bgImage = cv2.imread(self.backgroundImagePath)
        for i, each in enumerate(self.fieldDetail):
            if i == 0:
                bgImage = self.addImage(bgImage, f"{self.ImageFolder}/{imageName}.{extension}", each)
            else:
                # dataToWrite = data[each["id"]]

                
                bgImage = self.addDetail(bgImage, each, self.getDataFromRowDict(data,each["id"]) )
        self.saveImage(image=bgImage, name=imageName)

    def addImage(self, bgImage, imagePath, details):
        # creating image creating object
        temp = imageField(path=imagePath)
        # setting the position of the x1 x2 y1 y2 and sizes for futher addition
        temp.setLastCord((details["x1"], details["y1"]))
        temp.x = details["x"]
        temp.y = details["y"]
        temp.w = details["w"]
        temp.h = details["h"]

        # calling set mode for creating the image with specific mode with resizing it as per previous values aere set
        temp.setMode(details["mode"])
        
        if temp.isCircle:
            for i in range(0,details["y1"] - details["y"]):
                for j in range(0, details["x1"] - details["x"]):
                    if not (temp.image[i,j,0] == 255 and temp.image[i,j,1] == 255 and temp.image[i,j,2] == 255):
                        bgImage[ details["y"]+i ,details["x"]+j] = temp.image[i,j]
        else:
            bgImage[ temp.y:temp.y2 , temp.x:temp.x2] = temp.image
        return bgImage

    def addDetail(self, bgImage, Details, dataToWrite):
        image = bgImage[ Details["y"]:Details["y1"] , Details["x"]:Details["x1"]]
        image = self.writer.writeLineS(image=image , fontSize=Details["fontSize"], text=dataToWrite, color = (Details["b"], Details["g"], Details["r"]) , mode=Details["mode"])
        bgImage[ Details["y"]:Details["y1"] , Details["x"]:Details["x1"]] = image
        return bgImage

    def saveImage(self,image,name):
        cv2.imwrite(f"{self.savePath}{name}.jpg", image)
        