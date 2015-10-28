from Tkinter import *
from basicAnimationClass import BasicAnimationClass
from cropClass import Crop
from FarmerClass import Farmer
import random


#Overall game that handles the interaction between the farmer and the crops
class FarmGame(BasicAnimationClass):
    def __init__(self,rows,cols):
        super(FarmGame,self).__init__(600,400)
        self.rows = rows
        self.cols = cols

    #converts the clicked coordinates into coordinates on the grid (field)
    def adjustCoords(self,x,y):
        shift = 12.5
        newEventX = ((int(x) - self.widthMargin)/self.cellDimensions *
                 self.cellDimensions + shift + self.widthMargin)
        newEventY = ((int(y)-self.heightMargin)/(self.cellDimensions) * 
                        self.cellDimensions + shift + self.heightMargin)
        return newEventX,newEventY

    def onMousePressed(self,event):
        shift = 12.5
        newEventX,newEventY = self.adjustCoords(event.x,event.y)
        #checks if crops planted are ready for harvest/watering
        for crops in reversed(self.crops):
            if self.harvest:
                if crops.harvestReady():
                    if crops.contains(newEventX,newEventY):
                        cropType = crops.checkType()
                        self.updateBalance(cropType)
                        self.crops.remove(crops)
            if self.waterCrop:
                if crops.contains(newEventX,newEventY):
                    crops.startGrow = True
                    self.waterCrop = False
        self.onMousePressedNext(event)
    
    #performs next set of checks: determining crop type and planting
    def onMousePressedNext(self,event):
        if self.plantCrop and self.isLegalClick(event.x,event.y):
            self.plantingColor = self.plantSelected(event.x,event.y)
        elif (not self.isLegalClick(event.x,event.y) and 
                        self.plantingColor != None and self.plantCrop):
                newEventX,newEventY = self.adjustCoords(event.x,event.y)
                newCrop = Crop(newEventX,newEventY,self.plantingColor,self.type)
                newCropCoords = (newEventX,newEventY)
                self.crops.append(newCrop)
                self.cropCoords.append(newCropCoords)
                (self.plantingColor,self.plantCrop) = (None,False)
        elif (event.x < self.widthMargin or 
                event.x > (self.widthMargin + self.gridLength)):
            self.error = True
        elif (event.y < self.heightMargin or 
                event.y > self.heightMargin + self.gridHeight):
            self.error = True

    def onKeyPressed(self, event):
        if event.keysym == "h" or event.char == "?": 
            (self.splash,self.nextPage,self.helpMenu) = (False,False,True)
        elif event.keysym == "b" and self.balance >0: 
            self.buyCrop = True
        elif event.keysym == "p":
            if self.seedLong > 0 or self.seedShort > 0: 
                self.plantCrop = True
            else: self.error = True
        elif event.keysym == "l": 
            if self.buyCrop: self.longCrop = True
        elif event.keysym == "s": 
            if self.buyCrop: self.shortCrop = True
        else: self.onKeyPressedNext(event)

    #extra key press conditions
    def onKeyPressedNext(self,event):
        if event.keysym == "p": self.plantCrop = True
        elif event.keysym == "w": self.waterCrop = True
        elif event.keysym == "n": 
            if self.helpMenu:
                (self.helpMenu,self.nextPage) = (False,True)
        elif event.keysym == "r": self.initAnimation()
        elif event.keysym == "e": 
            (self.helpMenu,self.splash,self.nextPage) = (False,False,False)
        elif event.keysym == "space":
            (self.splash,self.startGame) = (False,True)
        elif event.keysym == "v": 
            self.harvest =  True
            self.drawHarvestText = False

    def onTimerFired(self):
        growthFactorLong = 10
        growthFactorShort = 20
        for crops in self.crops:
            if crops.startGrow and crops.growthPoints < crops.maxGrowthPoints:
                if crops.type == "longCrop":
                    crops.growthPoints += growthFactorLong
                else: crops.growthPoints += growthFactorShort
            if crops.startGrow and crops.growthPoints == crops.maxGrowthPoints:
                crops.color = "Purple"
                self.drawHarvestText = True
                crops.startGrow = False
                crops.readyHarvest = True

    #Initialize the farmer's variables here + the environment variables
    def initAnimation(self):
        self.app.setTimerDelay(1000)
        (self.emptyColor,self.backgroundColor) = ("sienna","Yellow")
        (self.cellDimensions,widthFactor) = (25,10)
        self.gridLength = self.cellDimensions * self.cols
        self.gridHeight = self.cellDimensions * self.rows
        self.board = (FarmGame.make2dList(self,self.rows,self.cols,
                                            self.emptyColor))
        self.widthMargin= self.app.width/widthFactor
        self.heightMargin = (self.app.height-self.rows*self.cellDimensions)/2
        self.balance,self.seedLong,self.seedShort = 1000,0,0
        (self.buyCrop,self.plantCrop) = (False,False)
        (self.longCrop,self.shortCrop) = (False,False)
        (self.plantLong,self.plantShort,self.waterPlants) = (False,False,False)
        (self.crops,self.cropCoords) = ([],[])
        (self.startGrow,self.error,self.drawHarvestText) = (False,False,False)
        (self.helpMenu,self.splash,self.startGame) = (False, True,False)
        (self.plantingColor,self.type,self.nextPage) = (None,None,False)
        (self.plantCrop,self.waterCrop,self.harvest) = (False,False,False)

    #Updates balance when crops are sold
    def updateBalance(self,cropType):
        (longReturn,shortReturn) = (210,100)
        if cropType == "longCrop":
            self.balance += longReturn
        else: self.balance += shortReturn
        self.harvest = False

    #helper function: draws each individual square
    def drawGrid(self,row,col,currentColor,x,y):
        canvas = self.canvas
        canvas.create_rectangle(x,y,x+self.cellDimensions,y+self.cellDimensions,
                                    width = 2, fill = currentColor)
   
    #draws the actual field
    def drawField(self):
        canvas = self.canvas
        x,y = self.widthMargin,self.heightMargin
        for row in xrange(self.rows):
            x = self.widthMargin
            for col in xrange(self.cols):
                currentColor = self.board[row][col]
                self.drawGrid(row,col,currentColor,x,y)
                x += self.cellDimensions
            y += self.cellDimensions
    
    #calls drawing method from Crop object
    def drawCrops(self):
        canvas = self.canvas
        for crops in self.crops:
            Crop.draw(crops,canvas)
    
    #determines which crop type user selected to buy, updates seed count
    def buyCropType(self):
        longCropPrice = 100
        shortCropPrice = 50
        if self.longCrop and self.balance >= longCropPrice:
            self.balance -= longCropPrice
            self.seedLong += 1
            self.longCrop = False
            self.buyCrop = False
        elif self.shortCrop and self.balance >= shortCropPrice:
            self.balance -= shortCropPrice
            self.seedShort += 1
            self.shortCrop = False
            self.buyCrop = False
    
    #checks to see if user wants to buy 
    def buyCrops(self):
        canvas = self.canvas
        if self.buyCrop:
            (scaleX,scaleY) = (1.3,3)
            text = "Press l for long crop.\n Press s for short crop."
            canvas.create_text(self.app.width/scaleX,self.app.height/scaleY, 
                                    text = text, font = " Aerial 15")
            self.buyCropType()

    #Returns if click is inside boundary
    def isLegalClick(self,x,y):
        shortCropCoord = [15,15,50,50]
        longCropCoord = [15,81,50,116]
        if (x>shortCropCoord[0] and x<shortCropCoord[2] and
                 y>shortCropCoord[1] and y < shortCropCoord[3] and 
                 self.seedShort > 0):
            return True
        if (x>longCropCoord[0] and x<longCropCoord[2] and
                 y>longCropCoord[1] and y < longCropCoord[3] 
                    and self.seedLong > 0):
            return True
        return False    
    
    #determines which type of crop user wants to plant, returns plant color
    def plantSelected(self,x,y):
        #these are the bounds of the rectangles for the crop types and water
        shortCropCoord = [15,15,50,50]
        longCropCoord = [15,81,50,116]
        if (x>shortCropCoord[0] and x<shortCropCoord[2] and
                 y>shortCropCoord[1] and y < shortCropCoord[3] and 
                 self.seedShort > 0):
            self.seedShort -=1
            self.type = "shortCrop"
            return "green"
        if (x>longCropCoord[0] and x<longCropCoord[2] and
                 y>longCropCoord[1] and y < longCropCoord[3] 
                    and self.seedLong > 0):
            self.seedLong -=1
            self.type = "longCrop" 
            return "blue"      

    #taken from class notes
    @staticmethod
    def make2dList(self,rows,cols,value):
        a=[]
        for row in xrange(rows): a += [[value]*cols]
        return a

    #displays if crops are ready for harvest
    def drawHarvest(self):
        scale = 3
        canvas = self.canvas
        canvas.create_text(self.app.width/2,self.app.height/2,
                            text = "Incorrect Move!", font = "Aerial 20 bold")

    #draws crop selections on the left
    def drawCropTypes(self):
        (dist,scale,margin,numMoves,textShift,loops) = (4,1.2,0,6,10,3)
        canvas = self.canvas
        #loops to draw short and long crops
        for i in xrange(loops):
            (x1,y1) = (self.widthMargin/dist, self.widthMargin/dist + margin)
            (x2,y2) = (self.widthMargin/scale, self.widthMargin/scale+margin)
            if i == 2:
                pass
            else:
                colors = ["green","blue"]
                crops = ["Short","Long"]
                canvas.create_oval(x1,y1,x2,y2,fill = colors[i])
                canvas.create_text((x1+x2)/2,y2+textShift, text = crops[i])
            margin += self.app.height/numMoves
        margin = 0

    #main drawing function, calls helper functions
    def drawGame(self):
        canvas = self.canvas
        canvas.create_rectangle(0,0,self.width,self.height, 
                                    fill = self.backgroundColor)
        self.drawField()
        self.drawCropTypes()
        if self.splash:
            self.drawSplashScreen()
    
    #calls any drawing of farmer object
    def drawFarmer(self):
        canvas = self.canvas
        farmerStat = Farmer(self.balance,self.seedLong,self.seedShort)
        Farmer.drawFarmerStats(farmerStat,canvas,self.app.width)

    #part of help menu
    def drawNextText(self,margin,height,width):
        canvas = self.canvas
        sa = self.app
        (widthScale,heightScale,multiplier) = (1.3,1.55,1.1)
        shortText = "\n Short: Dark Green."
        canvas.create_text(sa.width/widthScale,sa.height/heightScale, 
                                text = shortText, font = " Aerial 13")
        harvest = "Then press v and \nclick on crop to harvest."
        canvas.create_text(sa.width/widthScale,sa.height/widthScale, 
                                text = harvest, font = " Aerial 13")
        exitMenu = "Exit before buying/planting"
        canvas.create_text(sa.width/widthScale,sa.height/multiplier, 
                                text = exitMenu, font = " Aerial 14")

    #part of help menu
    def drawNextMenu(self):
        sa = self.app
        (margin,height,multiplier,heightMult) = (10,3,4,5)
        (scale,xScale,yScale) = (1.6,1.3,1.9)
        canvas = self.canvas
        width = self.gridLength + self.widthMargin + margin
        canvas.create_rectangle(width, 2*multiplier*self.heightMargin,
            sa.width-margin,sa.height-margin, width = 2)
        (text,escText) = ("Next Page","Press e to exit menu")
        canvas.create_text(height*width/2 - margin, multiplier*height*margin, 
                                    text = text, font = "Aerial 15 bold")
        canvas.create_text(height*width/2 - margin, heightMult*height*margin, 
                                    text = escText, font = "Aerial 13 bold")
        text1 = "Press w to toggle water\nThen, click on crop."
        canvas.create_text(sa.width/xScale,sa.height/yScale, 
                                text = text1, font = " Aerial 13")
        text2  = "Done when Long: Purple"
        canvas.create_text(sa.width/xScale,sa.height/scale, 
                                text = text2, font = " Aerial 13")
        self.drawNextText(margin,height,width)

    #help menu
    def helpMenuText(self,canvas):
        sa = self.app
        (xScale,yScale,scale,finalX) = (1.3,1.38,1.9,1.1)
        text1 = "    Press b to buy.\n Then press l for long "
        text2  = "\n crops or s for short crops."
        canvas.create_text(sa.width/xScale,sa.height/scale, 
                                text = text1 + text2, font = " Aerial 13")
        plantText = "Press p to plant.\nThen, click plant type."
        plantTextNext = "\nAnd select location."
        canvas.create_text(sa.width/xScale,sa.height/yScale, 
                                text = plantText + plantTextNext, 
                                    font = " Aerial 14")
        exitMenu = "Press n for next page."
        canvas.create_text(sa.width/xScale,sa.height/finalX, 
                                text = exitMenu, font = " Aerial 14")

    def drawHelpMenu(self):
        sa = self.app
        (margin,height,xScale,yScale) = (10,3,4,5)
        canvas = self.canvas
        if self.helpMenu:
            width = self.gridLength + self.widthMargin + margin
            canvas.create_rectangle(width, 2*xScale*self.heightMargin,
                sa.width-margin,sa.height-margin, width = 2)
            (text,escText) = ("Help Menu","Press e to exit menu")
            canvas.create_text(height*width/2 - margin, xScale*height*margin, 
                                    text = text, font = "Aerial 15 bold")
            canvas.create_text(height*width/2 - margin, yScale*height*margin, 
                                    text = escText, font = "Aerial 13 bold")          
            self.helpMenuText(canvas)    
    
    #creates splash screen, resets when r is pressed
    def drawSplashScreen(self):
        (margin,height,xScale,yScale) = (10,5,7,3)
        canvas = self.canvas
        sa = self.app
        width = self.gridLength + self.widthMargin + margin
        canvas.create_rectangle(0,0,self.width,self.height, 
                                    fill = "grey")
        text= "FarmVille: Pirated Version!\nMade by Ani Ramakrishnan"
        canvas.create_text(sa.width/2,sa.width/margin, fill = "coral",
                            text = text, 
                            font = "Aerial 20 bold italic underline")
        textDir = "Press h or ? for directions\n"
        textStart = "Press space to begin!"
        canvas.create_text(sa.width/2,xScale*sa.height/(2*margin),fill = "red4", 
                        text= textDir + textStart, font = "Aerial 20 bold")
        textLegal = "Note: This game may or \nmay not be not illegal.\n"
        textWarning = " Play at your own risk!"
        canvas.create_text(sa.width/2,(yScale*sa.height)/height,
                            fill = "firebrick1", text= textLegal + textWarning, 
                                font = "Aerial 20 bold")

    def drawError(self):
        scale = 3
        sa = self.app
        canvas = self.canvas
        canvas.create_text(2*sa.width/scale,sa.height/2,
                            text = "Incorrect Move!", font = "Aerial 20 bold")
        self.error = False
        return
    
    def redrawAll(self):
        canvas = self.canvas
        canvas.delete(ALL)
        if self.drawHarvestText: 
            self.drawHarvest()
        self.drawGame()
        self.drawHelpMenu()
        if self.nextPage:
            self.drawNextMenu()
        if not self.splash:
            self.drawFarmer()
        self.buyCrops()
        self.drawCrops()
        if self.error: 
            self.drawError()


FarmGame = FarmGame(15,10)
FarmGame.run()
