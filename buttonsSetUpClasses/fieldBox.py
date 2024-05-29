
from buttonsSetUpClasses.button import button

class fieldBox(button):
    def __init__(self, x=0, y=0, h=100, w=100, i=0):
        self.id = i
        super().__init__( x = x , y = y , h = h , w = w )

    # responsible for changing dimention according to the (mouseWX) pos
    def setDimension(self, pos):
        self.w = pos[0] - self.x
        self.h = pos[1] - self.y
        if self.w<0 :
            self.w = self.x
            self.x = pos[0]
        if self.h<0 :
            self.h = self.y
            self.y = pos[1]
        self.x2 = pos[0]
        self.y2 = pos[1]
    
    # this will check if the object is in the dimension Position change area return true or false
    def isSelect(self, pos):
        # to set bewteen the box of field of 20 X 20 above the left most top corner
        if (pos[0] > self.x) and (pos[0] < self.x+10) and (pos[1] > self.y-10) and (pos[1] < self.y) :
            return 0
        elif (pos[0] > self.x + self.w ) and (pos[0] < self.x + self.w +5) and (pos[1] > self.y + self.h) and (pos[1] < self.y+self.w+5) :
            return 1
        return -1


    # this resposible for changing the dimension and the position of the field box
    def action(self, type , pos):
        if type == 0 :
            self.setPos(pos)
        elif type == 1:
            self.setDimension(pos)