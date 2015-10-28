import random

#Handles the crops in the game
class Crop(object): 
    def __init__(self,x,y,color,type):
        self.x = x
        self.y = y
        self.r = 7
        self.type = type
        self.color = color
        self.longPrice = 100
        self.shortPrice = 50
        self.startGrow = False
        self.readyHarvest = False
        self.growthPoints = 0
        self.maxGrowthPoints = 200

    def harvestReady(self):
        return self.readyHarvest

    #Gets the color of the crop (indicates how much time left is in its growth)
    @staticmethod
    def rgbString(red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)


    def draw(self,canvas):
        gp = self.growthPoints
        if self.growthPoints > 0:
            if self.type == "longCrop":
                self.color = (Crop.rgbString(100,200-self.growthPoints,
                                200 - self.growthPoints/2))
            else:self.color = (Crop.rgbString(100,200 - self.growthPoints/4,
                                    200-self.growthPoints))
        (x,y,r) = self.x,self.y,self.r
        canvas.create_oval(x-r,y-r,x+r,y+r, fill = self.color)

    def checkType(self):
        return self.type

    def contains(self,x,y):
        return ((self.x - x)**2 + (self.y - y)**2 <= self.r**2)

