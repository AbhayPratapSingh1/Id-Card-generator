import sys
import cv2
import numpy as np
from PIL import ImageFont, Image, ImageDraw


class Writer:
    textDimension = lambda self, text_box : [text_box[2] - text_box[0], text_box[3] - text_box[1]]    
    def __init__(self):
        self.font = None
        self.position = [0, 0]
        self.Lines = []

    def loadFont(self, path, size):
        try:
            font = ImageFont.truetype(path, size)
        except IOError:
            print(f"Font at location {path} doesn't found please place font there!")
            input()
            sys.exit(0)
        # Verify if the font was loaded correctly
        if font is None:
            print(f"Font at location {path} doesn't found or corrupted please place valid font there!")
            sys.exit(0)
        self.font = font
        return font
    
    def normalisePosition(self ,position, font_box):
        position[0] -= font_box[0]
        position[1] -= font_box[1]
        self.position = position
        return position

    def setTextBoxAndPosition(self, position , text, mode=1, size = 0):
        textBox = self.font.getbbox(text) # this is for getting cordinates of the box if the position taken is (0,0) [x0,y0,x1,y1]
        position = list(position)
        textSize = self.textDimension(textBox) # determininge the size of the bredth and the height of the text in the fonts
        self.normalisePosition(position, textBox) # normalising the position as per the text box x0,y0 cordinates so position given should be match
        
        if mode==1: # mode 1 for left corner in the field box
            pass
        
        elif mode==2: # mode 2 text needed to be place at the center of the field box since it is for id card posy is 0
            position[0] = size[0]//2
            position[0] = position[0] - textSize[0]//2

        elif mode==3: # mode 3 for the right corner in field box **** since it is for id card posy is right most corner
            position[0] = size[0]
            position[0] = position[0] - textSize[0]
            pass

        self.position = position

    def writeLine(self, image, fontPath = None, position = (0,0), fontSize=10, text=" ", color=(0,0,0), mode= 2 ):
        # exception Handling
        # loading the font from the file
        if self.font == None:
            self.loadFont(fontPath, fontSize)

        # set position where text needed to be placed
        self.setTextBoxAndPosition(position, text, mode, size=image.shape[:2][::-1])

        # convert np array to pil image
        image_pil = Image.fromarray(image)
        # create the image drawer for the image
        draw = ImageDraw.Draw(image_pil)
        # writing the text in the images
        draw.text(self.position, text, font=self.font, fill=color)
        # Convert PIL image back to Numpy image
        image_with_text = np.array(image_pil)
        return image_with_text

    def writeLineS(self, image, fontPath="./fontAndTextSetup/testFont.ttf", fontSize = 10, text=" ", mode = 1, heightGap = 10 ):
        self.img = image
        self.loadFont(fontPath, fontSize)
        y, x = image.shape[0:2]
        self.textBreaker((x,y), text, heightGap= heightGap)

        for eachLine, yCord in self.Lines:
            self.img = self.writeLine(text=eachLine ,image = self.img, position=(0, yCord), mode=mode)

        cv2.imshow("image", self.img)
        cv2.waitKey(0)
        cv2.imwrite("img.png", self.img)
        
    def textBreaker(self, size, text, heightGap = 10):
        st = 0
        height = 0
        for i in range(len(text)):
            textBox = self.font.getbbox(text[st: i+1])
            textSize = self.textDimension(textBox)
            if textSize[0] >= size[0]:
                self.Lines.append((text[st:i], height))
                height = height + textSize[1] + heightGap
                st = i
        self.Lines.append((text[st:i+1], height))

# for code checking and debugging
# image = np.full((500, 300, 3), 200, np.uint8)
# temp = Writer()
# temp.writeLineS(image, "./fontAndTextSetup/testFont.ttf", 50,"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ",heightGap = 10 , mode = 1)
